"use client";

import { useState } from "react";

interface VideoFormProps {
  onIngest: (url: string) => void;
  loading : boolean;
}

export default function VideoForm({ onIngest, loading }: VideoFormProps) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!url.trim()) return;

    onIngest(url);
    setUrl("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        placeholder="Paste YouTube URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="flex-1 rounded-lg border px-4 py-2 text-gray-900 outline-none focus:ring-2 focus:ring-black"
      />

    <button
      type="submit"
      disabled={loading}
      className="rounded-lg bg-black px-5 py-2 text-white disabled:opacity-50"
    >
      {loading ? "Ingesting..." : "Ingest"}
    </button>
    </form>
  );
}