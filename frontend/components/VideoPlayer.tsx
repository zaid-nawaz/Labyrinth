"use client";

import YouTube, { YouTubeProps } from "react-youtube";

interface VideoPlayerProps {
  videoId: string;
  onReady: YouTubeProps["onReady"];
}

export default function VideoPlayer({ videoId, onReady }: VideoPlayerProps) {
  const opts: YouTubeProps["opts"] = {
  
    playerVars: {
      autoplay: 0,
    },
  };

  return (
    <div className="aspect-video w-full overflow-hidden rounded-xl">
      <YouTube
        videoId={videoId}
        opts={opts}
        onReady={onReady}   
    className="h-full w-full"
    iframeClassName="h-full w-full rounded-xl"
      />
    </div>
  );
}