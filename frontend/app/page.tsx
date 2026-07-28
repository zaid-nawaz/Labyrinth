"use client";

import { useState } from "react";
import VideoForm from "@/components/VideoForm";
import { api } from "@/lib/api";
import VideoPlayer from "@/components/VideoPlayer";
import { Message } from "@/types/chat";
import Chat from "@/components/Chat";

export default function Home() {

const [videoId, setVideoId] = useState("");
const [loading, setLoading] = useState(false);
const [messages, setMessages] = useState<Message[]>([]);

    const handleIngest = async (url: string) => {
      try {
        setLoading(true);

        const response = await api.post("/ingest", {
          url,
        });

        setVideoId(response.data.video_id);

        console.log(response.data);
      } catch (error) {
        console.error(error);
        alert("Failed to ingest video.");
      } finally {
        setLoading(false);
      }
    };

    const handleSend = async (message: string) => {
      if (!videoId) return;

      // Immediately show the user's message
      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: message,
        },
      ]);

      try {
        const response = await api.post("/query", {
          video_id: videoId,
          query: message,
        });

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: response.data.content,
          },
        ]);

        console.log(response.data.offset);
      } catch (err) {
        console.error(err);

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Something went wrong.",
          },
        ]);
      }
    };


  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <div className="mx-auto flex h-[90vh] max-w-7xl gap-6">
        {/* Left Panel */}
      <div className="flex flex-1 flex-col rounded-xl border bg-white p-6 shadow">
        <VideoForm onIngest={handleIngest} loading={loading}/>

      <div className="mt-6 flex-1">
        {videoId ? (
          <VideoPlayer videoId={videoId} />
        ) : (
          <div className="flex h-full items-center justify-center rounded-lg border-2 border-dashed">
            <h2 className="text-2xl font-semibold text-gray-400">
              Video will appear here
            </h2>
          </div>
        )}
      </div>
      </div>

        {/* Right Panel */}
      <div className="w-[400px] rounded-xl border bg-white shadow">
        <Chat messages={messages} onSend={handleSend} disabled={!videoId} />
      </div>
      </div>
    </main>
  );
}
