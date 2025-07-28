import React from "react";

export default function UploadZone({ images, setImages }) {
  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);

    const validImages = selectedFiles.filter((file) => {
      return file.type.startsWith("image/");
    });

    const combinedImages = [...images, ...validImages].slice(0, 10);

    setImages(combinedImages);
  };

  const handleRemoveImage = (indexToRemove) => {
    const updated = images.filter((_, index) => index !== indexToRemove);
    setImages(updated);
  };

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Upload 5–10 property images
      </label>

      <input
        type="file"
        multiple
        accept="image/*"
        onChange={handleFileChange}
        className="block w-full p-2 border rounded"
      />

      <div className="mt-4 flex flex-wrap gap-4">
        {images.map((img, index) => {
          const previewUrl = URL.createObjectURL(img);

          return (
            <div key={index} className="relative">
              <img
                src={previewUrl}
                alt={`preview-${index}`}
                className="w-24 h-24 object-cover rounded shadow"
              />

              <button
                onClick={() => handleRemoveImage(index)}
                className="absolute top-0 right-0 bg-red-600 text-white rounded-full w-6 h-6 text-xs flex items-center justify-center hover:bg-red-700"
              >
                ×
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
