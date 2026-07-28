import VideoForm from "@/components/VideoForm";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <div className="mx-auto flex h-[90vh] max-w-7xl gap-6">
        {/* Left Panel */}
      <div className="flex flex-1 flex-col rounded-xl border bg-white p-6 shadow">
        <VideoForm />

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
