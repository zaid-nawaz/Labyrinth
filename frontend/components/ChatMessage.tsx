

interface ChatMessageProps {
    role: "user" | "assistant";
    content: string;
}

export default function ChatMessage({
    role,
    content,
}: ChatMessageProps) {
    return (
            <div
              className={`mb-4 rounded-lg p-3 ${
                role === "user"
                  ? "ml-auto max-w-[80%] bg-blue-600 text-white"
                  : "mr-auto max-w-[80%] bg-gray-800"
              }`}
            >
              {content}
            </div>
    );
}