"use client";

import { useState } from "react";
import VideoForm from "@/components/VideoForm";
import { api } from "@/lib/api";
import VideoPlayer from "@/components/VideoPlayer";
import { Message } from "@/types/chat";
import Chat from "@/components/Chat";
import { useRef } from "react";
import { YouTubePlayer, YouTubeProps } from "react-youtube";

export default function Home() {

const [videoId, setVideoId] = useState("");
const [loading, setLoading] = useState(false);
const [messages, setMessages] = useState<Message[]>([]);
const [isLoading, setIsLoading ] = useState(false);

const playerRef = useRef<YouTubePlayer | null>(null);

const handlePlayerReady: YouTubeProps["onReady"] = (event) => {
    console.log(playerRef.current);
    playerRef.current = event.target;
};

const handleSeek = (milliseconds: number) => {

  if(!playerRef.current) return;

  playerRef.current?.seekTo(milliseconds / 1000, true);
  playerRef.current.playVideo();
};

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

      setIsLoading(true);

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
            offset: response.data.offset,
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
      } finally {
        setIsLoading(false);
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
          <VideoPlayer videoId={videoId} onReady={handlePlayerReady} />
        ) : (
          <div className="flex h-full items-center justify-center rounded-lg border-2 border-dashed">
            <h2 className="text-2xl font-semibold text-gray-400">
              Ingest the Youtube Video
            </h2>
          </div>
        )}
      </div>
      </div>

        {/* Right Panel */}
      <div className="flex h-full w-[400px] flex-col rounded-xl border bg-white shadow">
        <Chat messages={messages} onSend={handleSend} disabled={!videoId} loading={isLoading} onSeek={handleSeek}/>
      </div>
      </div>
    </main>
  );
}
