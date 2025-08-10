import os, json, boto3
from functools import lru_cache

@lru_cache(maxsize=1)
def load_secret_string(name: str, region: str | None = None) -> str:
    sm = boto3.client("secretsmanager", region_name=region or os.getenv("AWS_REGION", "us-west-2"))
    r = sm.get_secret_value(SecretId=name)
    s = r.get("SecretString") or ""
    try:
        obj = json.loads(s)
        return obj.get("api_key") or obj.get("key") or s
    except json.JSONDecodeError:
        return s
