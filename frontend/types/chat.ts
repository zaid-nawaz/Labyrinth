export interface Message {
  role: "user" | "assistant";
  content: string;
  offset?: number[];
}