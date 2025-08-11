// src/UploadAnalyzeApp.tsx
// Vite + React + TypeScript + Tailwind + shadcn/ui
// Single-file, self-contained example that you can drop into src/ and use as App.tsx
// It includes: a tiny API client, a stateful hook, and a clean UI with shadcn components.

import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { Toaster, toast } from "sonner";

// ---- Configuration ----
const API_BASE = (import.meta as any).env?.VITE_API_BASE as string;

// ---- Types ----
type ImageRecord = {
  pk: string; // image_id
  s3_key: string;
  status: "UPLOADED" | "ANALYZED" | string;
  meta?: { content_type?: string; size?: number; url?: string };
  analysis?: { provider?: string; model?: string; text?: string };
};

// ---- Minimal API client ----
const api = {
  async presignUpload(contentType: string) {
    const r = await fetch(`${API_BASE}/uploads/presign`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ content_type: contentType }),
    });
    if (!r.ok) throw new Error(`presign failed: ${r.status}`);
    return (await r.json()) as { image_id: string; s3_key: string; url: string };
  },
  putToS3(url: string, file: File, onProgress?: (pct: number) => void) {
    return new Promise<void>((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("PUT", url);
      xhr.setRequestHeader("content-type", file.type);
      xhr.upload.onprogress = (e) => {
        if (!onProgress || !e.lengthComputable) return;
        onProgress(Math.round((e.loaded / e.total) * 100));
      };
      xhr.onerror = () => reject(new Error("upload error"));
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) resolve();
        else reject(new Error(`upload failed: ${xhr.status}`));
      };
      xhr.send(file);
    });
  },
  async notifyUpload(payload: { image_id: string; s3_key: string; content_type: string }) {
    const r = await fetch(`${API_BASE}/uploads/notify`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!r.ok) throw new Error(`notify failed: ${r.status}`);
    return (await r.json()) as { enqueued: boolean };
  },
  async enqueueAnalyze(image_id: string) {
    const r = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ image_id }),
    });
    if (!r.ok) throw new Error(`analyze enqueue failed: ${r.status}`);
    return (await r.json()) as { enqueued: boolean };
  },
  async getImage(image_id: string) {
    const r = await fetch(`${API_BASE}/images/${image_id}`);
    if (!r.ok) throw new Error(`get image failed: ${r.status}`);
    return (await r.json()) as ImageRecord;
  },
};

// ---- State machine hook ----
function useUploadAnalyze() {
  const [file, setFile] = useState<File | null>(null);
  const [imageURL, setImageURL] = useState<string | null>(null); // local preview
  const [imageId, setImageId] = useState<string | null>(null);
  const [s3Key, setS3Key] = useState<string | null>(null);
  const [uploadPct, setUploadPct] = useState<number>(0);
  const [record, setRecord] = useState<ImageRecord | null>(null);
  const [busy, setBusy] = useState<boolean>(false);
  const pollRef = useRef<number | null>(null);

  useEffect(() => () => { if (pollRef.current) window.clearInterval(pollRef.current); }, []);

  const onFile = useCallback((f: File | null) => {
    setFile(f);
    setRecord(null);
    setImageId(null);
    setS3Key(null);
    setUploadPct(0);
    setImageURL(f ? URL.createObjectURL(f) : null);
  }, []);

  const canUpload = useMemo(() => !!file && !busy, [file, busy]);
  const canAnalyze = useMemo(() => !!imageId && !busy, [imageId, busy]);

  const upload = useCallback(async () => {
    if (!file) return;
    setBusy(true);
    try {
      const { image_id, s3_key, url } = await api.presignUpload(file.type);
      await api.putToS3(url, file, setUploadPct);
      await api.notifyUpload({ image_id, s3_key, content_type: file.type });
      setImageId(image_id);
      setS3Key(s3_key);
      toast.success("Upload complete");
    } catch (e: any) {
      toast.error(e?.message ?? "Upload failed");
    } finally {
      setBusy(false);
    }
  }, [file]);

  const analyze = useCallback(async () => {
    if (!imageId) return;
    setBusy(true);
    try {
      await api.enqueueAnalyze(imageId);
      toast.info("Analyze enqueued");
      // poll until ANALYZED
      if (pollRef.current) window.clearInterval(pollRef.current);
      pollRef.current = window.setInterval(async () => {
        try {
          const rec = await api.getImage(imageId);
          setRecord(rec);
          if (rec.status === "ANALYZED") {
            window.clearInterval(pollRef.current!);
            pollRef.current = null;
            toast.success("Analysis complete");
            setBusy(false);
          }
        } catch (e) {
          // keep polling; surface once via toast
        }
      }, 1500);
    } catch (e: any) {
      setBusy(false);
      toast.error(e?.message ?? "Analyze failed");
    }
  }, [imageId]);

  return {
    file,
    imageURL,
    imageId,
    s3Key,
    uploadPct,
    record,
    canUpload,
    canAnalyze,
    busy,
    onFile,
    upload,
    analyze,
  } as const;
}

// ---- UI ----
export default function App() {
  const h = useUploadAnalyze();

  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-6 bg-[radial-gradient(ellipse_at_top,_rgba(93,76,231,0.35),_transparent_60%),radial-gradient(ellipse_at_bottom,_rgba(66,133,244,0.25),_transparent_60%)]">
      <Toaster richColors position="top-right" />
      <div className="max-w-3xl mx-auto w-full">
        <Card className="shadow-md w-full">
          <CardHeader>
            <CardTitle>Image Upload & Analyze</CardTitle>
            <CardDescription>
              Select an image, upload to S3 via a presigned URL, then enqueue analysis. Polls DynamoDB-backed record until complete.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <section className="space-y-2">
              <Label htmlFor="file">Image file</Label>
              <div className="flex items-center gap-3">
                <Input id="file" type="file" accept="image/png,image/jpeg,image/webp"
                  onChange={(e) => h.onFile(e.target.files?.[0] ?? null)} />
                <Button variant="secondary" onClick={() => h.onFile(null)} disabled={!h.file}>Clear</Button>
              </div>
              {h.imageURL && (
                <div className="mt-3">
                  {/* Local preview only */}
                  <img src={h.imageURL} alt="preview" className="max-h-56 rounded-md" />
                </div>
              )}
            </section>

            <section className="flex flex-wrap gap-3">
              <Button onClick={h.upload} disabled={!h.canUpload}>Upload</Button>
              <Button
                onClick={h.analyze}
                disabled={!h.canAnalyze}
                className="bg-gradient-to-r from-[#4285F4] via-[#9b72cb] to-[#d96570] text-white hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Analyze
              </Button>
            </section>

            {h.uploadPct > 0 && h.uploadPct < 100 && (
              <section>
                <Label>Uploading… {h.uploadPct}%</Label>
                <Progress className="mt-2" value={h.uploadPct} />
              </section>
            )}

            <Separator />

            <section className="space-y-2">
              <Label>Result</Label>
              <div className="text-sm text-muted-foreground">
                {h.imageId ? (
                  <div className="space-y-1">
                    <div><span className="font-medium">image_id:</span> {h.imageId}</div>
                    <div><span className="font-medium">status:</span> {h.record?.status ?? "—"}</div>
                    {h.record?.analysis?.text && (
                      <div className="mt-3 space-y-2">
                        <span className="inline-flex items-center gap-1 rounded-full bg-secondary/30 px-2 py-1 text-[10px] font-medium text-secondary-foreground uppercase tracking-wide">
                          AI generated
                        </span>
                        <div className="whitespace-pre-wrap text-foreground">
                          {h.record.analysis.text}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <span>Upload a file to begin.</span>
                )}
              </div>
            </section>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
