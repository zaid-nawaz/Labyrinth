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
                  ? "ml-auto max-w-[80%] bg-gray-600 text-white"
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
                <div className="mt-3 flex flex-wrap gap-1.5">
                    {offset.map((time, index) => (
                    <button
                        key={index}
                        onClick={() => onSeek?.(time)}
                        className="group flex items-center gap-1.5 rounded-full border border-gray-700 bg-gray-900/50 px-3 py-2 text-xs font-medium text-gray-100 transition-colors hover:border-blue-500/50 hover:bg-blue-500/10 hover:text-blue-400"
                    >
                        <svg
                            className="h-3 w-3 text-gray-500 transition-colors group-hover:text-blue-400"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth={2}
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                        {formatTimestamp(time)}
                    </button>
                    ))}
                </div>
            )}
            </div>


            </div>
    );
}