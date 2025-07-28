import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import UploadZone from "../components/UploadZone";
import DescriptionInput from "../components/DescriptionInput";
import GenerateVideoButton from "../components/GenerateVideoButton";
import { getSessionId } from '../utils/session';

export default function CreatePage() {
  const [sessionId, setSessionId] = useState("");
  const [images, setImages] = useState([]);
  const [description, setDescription] = useState("");
  const [uploadedUrls, setUploadedUrls] = useState([]);
  const [script, setScript] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [loadingStep, setLoadingStep] = useState(null);
  const [descriptionError, setDescriptionError] = useState(false);

  useEffect(() => {
    const storedSessionId = getSessionId();
    setSessionId(storedSessionId);
  }, []);

  const handleGenerateClick = () => {
    if (!description.trim()) {
      setDescriptionError(true);
      return;
    }
    setDescriptionError(false);

   
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Create a RealPitch Video</h1>

      <UploadZone images={images} setImages={setImages} />
      <DescriptionInput
        value={description}
        setValue={setDescription}
        error={descriptionError}
      />

      <GenerateVideoButton
        sessionId={sessionId}
        images={images}
        description={description}
        setUploadedUrls={setUploadedUrls}
        setScript={setScript}
        setAudioUrl={setAudioUrl}
        setVideoUrl={setVideoUrl}
        setLoadingStep={setLoadingStep}
        validate={() => {
          if (!description.trim()) {
            setDescriptionError(true);
            return false;
          }
          setDescriptionError(false);
          return true;
        }}
      />

      {loadingStep && (
        <p className="text-center mt-4 text-gray-600">⏳ {loadingStep}...</p>
      )}

      {videoUrl && (
        <div className="mt-10">
          <h2 className="text-xl font-semibold mb-4 text-center">🎬 Preview</h2>

          <div className="bg-white border border-gray-200 rounded-xl shadow-md overflow-hidden max-w-2xl mx-auto">
            <div className="aspect-w-16 aspect-h-9 bg-black">
              <video
                controls
                className="w-full h-full object-cover"
                src={videoUrl}
                poster={uploadedUrls[0]}
              ></video>
            </div>

            <div className="p-3 border-t text-center">
              <a
                href={videoUrl}
                download
                className="text-blue-600 hover:underline text-sm"
              >
                ⬇️ Download Video
              </a>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
