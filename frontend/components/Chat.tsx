import { Message } from "@/types/chat";
import ChatInput from "./ChatInput";
import { useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";
import { formatTimestamp } from "@/lib/time";

interface ChatProps {
  messages: Message[];
  onSend: (message: string) => void;
  disabled : boolean;
  loading : boolean;
  onSeek : (milliseconds : number) => void;

}

export default function Chat({ messages, onSend, disabled, loading, onSeek }: ChatProps) {
 
const bottomRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  bottomRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages, loading]);


  return (
    <div className="flex h-full flex-col">
<div className="flex flex-1 flex-col justify-end overflow-y-auto p-4">
        {messages.length === 0 ? (
          <p className="text-center text-gray-400">
            Ask me anything about the video.
          </p>
        ) : (
          messages.map((message, index) => (
            <ChatMessage
            key={index}
            role={message.role}
            content={message.content}
            offset={message.offset}
            onSeek={onSeek}
            />
          ))


        )}

        {loading && (
            <ChatMessage
                role="assistant"
                content=""
                loading
            />
        )}
      <div ref={bottomRef} />
      </div>

      <ChatInput onSend={onSend} disabled={disabled}/>

    </div>
  );
}