import { formatTimestamp } from "@/lib/time";

interface ChatMessageProps {
    role: "user" | "assistant";
    content: string;
    loading? : boolean;
    offset?: number[];
    onSeek? : (milliseconds: number) => void;
}

export default function ChatMessage({
    role,
    content,
    loading,
    offset,
    onSeek,
}: ChatMessageProps) {
    return (
            <div
              className={`mb-4 rounded-lg p-3 ${
                role === "user"
                  ? "ml-auto max-w-[80%] bg-blue-600 text-white"
                  : "mr-auto max-w-[80%] bg-gray-800"
              }`}
            >
            {loading ? (
                <div className="flex gap-1">
                    <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500"></span>
                    <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500 [animation-delay:150ms]"></span>
                    <span className="h-2 w-2 animate-bounce rounded-full bg-gray-500 [animation-delay:300ms]"></span>
                </div>
            ) : (
                content
            )}

        <div>
            {role === "assistant" &&
            offset &&
            offset.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                    {offset.map((time, index) => (
                    <button
                        key={index}
                        onClick={() => onSeek?.(time)}
                        className="rounded-full bg-slate-100 px-2 py-1 text-sm text-blue-600 hover:bg-slate-200"
                    >
                        🕒 {formatTimestamp(time)}
                    </button>
                    ))}
                </div>
            )}

        </div>


            </div>
    );
}