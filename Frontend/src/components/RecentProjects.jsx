import React, { useEffect, useState } from "react";

export default function RecentProjects() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("recentProjects") || "[]");
    setProjects(stored);
  }, []);

  if (projects.length === 0) {
    return (
      <p className="text-center text-gray-500 mt-8">
        You haven’t created any videos yet. Click “Create A Video” above to get started.
      </p>
    );
  }

  return (
    <div className="mt-10">
      <h2 className="text-xl font-bold mb-4 text-center">🎞 Your Recent Projects</h2>
      <div className="grid gap-6 sm:grid-cols-2">
        {projects.map((proj, index) => (
          <div key={index} className="border rounded p-3 shadow bg-white">
            <img
              src={proj.thumbnail}
              alt="Thumbnail"
              className="w-full h-40 object-cover rounded"
            />
            <p className="mt-2 text-sm text-gray-600">{proj.description}</p>
            <a
              href={proj.videoUrl}
              target="_blank"
              rel="noreferrer"
              className="block mt-2 text-blue-600 underline"
            >
              ▶️ Watch Again
            </a>
            <p className="text-xs text-gray-400 mt-1">
              {new Date(proj.createdAt).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
