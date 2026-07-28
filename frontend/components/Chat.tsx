import { Message } from "@/types/chat";
import ChatInput from "./ChatInput";
import { useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";

interface ChatProps {
  messages: Message[];
  onSend: (message: string) => void;
  disabled : boolean;

}

export default function Chat({ messages, onSend, disabled }: ChatProps) {

const bottomRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  bottomRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages]);


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
            />
          ))
        )}
      </div>
      <div ref={bottomRef} />

      <ChatInput onSend={onSend} disabled={disabled}/>

    </div>
  );
}