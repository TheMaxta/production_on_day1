from constructs import Construct
from aws_cdk import (
    Stack, CfnOutput,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_apigatewayv2 as apigw2,
    aws_apigatewayv2_integrations as apigw2_i,
    aws_secretsmanager as secretsmanager, 
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
import aws_cdk as cdk

class GenAiStack(Stack):
    def __init__(self, scope: Construct, id: str, **kw):
        super().__init__(scope, id, **kw)

        # --- Storage ---
        bucket = s3.Bucket(
            self, "AppBucket",
            cors=[s3.CorsRule(
                allowed_methods=[s3.HttpMethods.PUT, s3.HttpMethods.GET],
                allowed_origins=["*"], allowed_headers=["*"]
            )]
        )

        table = ddb.Table(
            self, "ImagesTable",
            partition_key=ddb.Attribute(name="pk", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
        )

        # --- Queues ---
        upload_q  = sqs.Queue(
            self, "UploadQueue",
            visibility_timeout=cdk.Duration.seconds(300)  # >= 60s
        )
        analyze_q = sqs.Queue(
            self, "AnalyzeQueue",
            visibility_timeout=cdk.Duration.seconds(300)  # >= 60s
        )
        
        # Common Lambda env
        common_env = {
            "APP_BUCKET": bucket.bucket_name,
            "APP_TABLE": table.table_name,
            "UPLOAD_QUEUE_URL": upload_q.queue_url,
            "ANALYZE_QUEUE_URL": analyze_q.queue_url,
        }

        # --- API Lambda (FastAPI via Mangum) ---
        api_fn = PythonFunction(
            self, "ApiLambda",
            entry="../src",                          # include whole src so shared modules import cleanly
            index="micro_services/api/handler.py",   # file
            handler="handler",                       # symbol
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment=common_env,
            timeout=cdk.Duration.seconds(30),
            memory_size=512,
        )

        # --- Workers ---
        upload_fn = PythonFunction(
            self, "UploadWorker",
            entry="../src",
            index="micro_services/upload_worker/lambda_handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment=common_env,
            timeout=cdk.Duration.seconds(60),
            memory_size=512,
        )
        analyze_fn = PythonFunction(
            self, "AnalyzeWorker",
            entry="../src",
            index="micro_services/analyze_worker/lambda_handler.py",
            handler="handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment=common_env,
            timeout=cdk.Duration.seconds(60),
            memory_size=512,
        )

        # Secret: reference existing by name and grant only analyze_fn
        openai_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "OpenAISecret", "openai/api_key"
        )
        openai_secret.grant_read(analyze_fn)
        analyze_fn.add_environment("OPENAI_SECRET_NAME", openai_secret.secret_name)

        # --- Event source mappings ---
        upload_fn.add_event_source(SqsEventSource(upload_q))
        analyze_fn.add_event_source(SqsEventSource(analyze_q))

        # --- Permissions ---
        bucket.grant_read_write(upload_fn)
        bucket.grant_read(analyze_fn)
        bucket.grant_write(api_fn)
        table.grant_read_write_data(upload_fn)
        table.grant_read_write_data(analyze_fn)
        upload_q.grant_send_messages(api_fn)
        analyze_q.grant_send_messages(api_fn)

        # --- HTTP API Gateway (Lambda proxy) ---
        http_api = apigw2.HttpApi(self, "HttpApi")
        http_api.add_routes(
            path="/{proxy+}",
            integration=HttpLambdaIntegration("ApiIntegration", api_fn),
        )

        # --- Outputs ---
        CfnOutput(self, "ApiBaseUrl", value=http_api.api_endpoint)
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "TableName", value=table.table_name)
        CfnOutput(self, "UploadQueueUrl", value=upload_q.queue_url)
        CfnOutput(self, "AnalyzeQueueUrl", value=analyze_q.queue_url)
