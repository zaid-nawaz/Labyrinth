"use client";

import { useState } from "react";
import { ArrowUp } from "lucide-react";

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
        className="flex-1 rounded-lg border px-4 py-2  outline-none text-gray-900 focus:ring-2 focus:ring-black"
        disabled={disabled}
      />

      <button
        type="submit"
        disabled={disabled}
        className="flex items-center rounded-full bg-black px-3 py-2 text-white hover:bg-gray-800 disabled:opacity-50"
      >
        <ArrowUp className="h-5 w-5" />
        
      </button>
    </form>
  );
}   