import React from "react";
import axios from "axios";

export default function GenerateVideoButton(props) {
  const {
    sessionId,
    images,
    description,
    setUploadedUrls,
    setScript,
    setAudioUrl,
    setVideoUrl,
    setLoadingStep,
    validate, 
  } = props;

  const handleGenerate = async () => {
    if (typeof validate === "function" && !validate()) {
      return;
    }

    if (images.length < 5) {
      alert("Please upload at least 5 images.");
      return;
    }

    setLoadingStep("Uploading images");

    const formData = new FormData();
    images.forEach((img) => {
      formData.append("files", img);
    });
    formData.append("session_id", sessionId);

    let uploadedUrls = [];

    try {
      const response = await axios.post(
        "https://realpitch-1.onrender.com/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      uploadedUrls = response.data.uploaded_files;
      setUploadedUrls(uploadedUrls);
    } catch (error) {
      alert("Failed to upload images. Check backend.");
      console.error(error);
      return;
    }

    setLoadingStep("Generating script");

    let scriptRes;
    try {
      scriptRes = await axios.post("https://realpitch-1.onrender.com/generatescript", {
        description,
        session_id: sessionId,
      });

      setScript(scriptRes.data.script);
    } catch (error) {
      alert("Script generation failed.");
      console.error(error);
      return;
    }

    setLoadingStep("Generating voiceover");

    let voiceRes;
    try {
      voiceRes = await axios.post("https://realpitch-1.onrender.com/generateaudio", {
        script: scriptRes.data.script,
        session_id: sessionId,
      });

      setAudioUrl(voiceRes.data.audio_url);
    } catch (error) {
      alert("Voice generation failed.");
      console.error(error);
      return;
    }

    setLoadingStep("Rendering video");

    try {
      console.log("Sending request to generate video...");

      const videoRes = await axios.post("https://realpitch-1.onrender.com/generatevideo", {
        image_urls: uploadedUrls,
        script: scriptRes.data.script,
        audio_url: voiceRes.data.audio_url,
        session_id: sessionId,
      });
      console.log("✅ Video response:", videoRes.data);


      const videoUrl = videoRes.data.video_url;
      setVideoUrl(videoUrl);
      setLoadingStep(null);

      const newEntry = {
        thumbnail: uploadedUrls[0],
        videoUrl,
        description,
        createdAt: new Date().toISOString(),
      };

      const existing = JSON.parse(localStorage.getItem("recentProjects") || "[]");
      const updated = [newEntry, ...existing].slice(0, 10);
      localStorage.setItem("recentProjects", JSON.stringify(updated));
    } catch (error) {
        console.error("❌ Video generation failed:", error);
        if (error.response) {
          console.log("Status:", error.response.status);
          console.log("Data:", error.response.data);
          console.log("Headers:", error.response.headers);
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error setting up request:", error.message);
        }
      alert("Video rendering failed.");
      console.error(error);
    }
  };

  return (
    <button
      onClick={handleGenerate}
      className="w-full py-3 bg-black text-white rounded font-medium hover:bg-gray-800 transition"
    >
      🎬 Generate Video
    </button>
  );
}
