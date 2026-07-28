"use client";

import { useState } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled : boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    onSend(input);
    setInput("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t p-4 flex gap-2"
    >
      <input
        type="text"
        placeholder={
            disabled
                ? "Ingest a video first..."
                : "Ask about the video..."
        }
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="flex-1 rounded-lg border px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        disabled={disabled}
      />

      <button
        type="submit"
        className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        Send
      </button>
    </form>
  );
}   