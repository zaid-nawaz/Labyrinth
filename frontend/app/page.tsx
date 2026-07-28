"use client";

import { useState } from "react";
import VideoForm from "@/components/VideoForm";
import { api } from "@/lib/api";

export default function Home() {

const [videoId, setVideoId] = useState("");
const [loading, setLoading] = useState(false);

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


  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <div className="mx-auto flex h-[90vh] max-w-7xl gap-6">
        {/* Left Panel */}
      <div className="flex flex-1 flex-col rounded-xl border bg-white p-6 shadow">
        <VideoForm onIngest={handleIngest}/>

        <div className="mt-6 flex flex-1 items-center justify-center rounded-lg border-2 border-dashed">
          <h2 className="text-2xl font-semibold text-gray-400">
            Video will appear here
          </h2>
        </div>
      </div>

        {/* Right Panel */}
        <div className="flex w-[400px] items-center justify-center rounded-xl border bg-white shadow">
          <h2 className="text-2xl font-semibold">Chat Section</h2>
        </div>
      </div>
    </main>
  );
}
