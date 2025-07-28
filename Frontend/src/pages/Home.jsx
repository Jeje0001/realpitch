import { Link } from "react-router-dom";
import RecentProjects from "../components/RecentProjects";

export default function HomePage() {
  const steps = [
    {
      icon: "🖼️",
      title: "Upload Photos",
      desc: "Add 5–10 high-quality property images.",
    },
    {
      icon: "✏️",
      title: "Write a Description",
      desc: "Just 1–2 sentences describing the home.",
    },
    {
      icon: "🗣️",
      title: "Let AI Narrate",
      desc: "Voiceover, and more generated instantly.",
    },
    {
      icon: "📽️",
      title: "Get Your Video",
      desc: "Download a vertical, agent-branded reel.",
    },
  ];

  return (
    <>
      <div className="bg-gradient-to-br from-blue-100 to-white py-20 px-4 text-center">
        <h1 className="text-5xl font-extrabold text-gray-900 mb-4">
          Create Stunning Real Estate Videos with AI
        </h1>
        <p className="text-lg text-gray-700 max-w-xl mx-auto mb-8">
          Upload photos, write a short description, and let RealPitch turn it
          into a polished, narrated listing video.
        </p>
        <Link to="/create">
          <button className="px-8 py-3 bg-black text-white rounded-full text-lg hover:bg-gray-900 transition">
            🎬 Create A Video
          </button>
        </Link>
      </div>

      <div className="max-w-6xl mx-auto mt-20 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 px-6">
        {steps.map((step, index) => (
          <div
            key={index}
            className="bg-white rounded-xl shadow-md p-6 text-center"
          >
            <div className="text-4xl mb-4">{step.icon}</div>
            <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
            <p className="text-sm text-gray-600">{step.desc}</p>
          </div>
        ))}
      </div>

     
        <div className="max-w-4xl mx-auto mt-20 px-6">
        <h2 className="text-2xl font-bold mb-4">Your Recent Projects</h2>
        <RecentProjects sessionId={sessionStorage.getItem("session_id")} />
        </div>



      
    </>
  );
}
