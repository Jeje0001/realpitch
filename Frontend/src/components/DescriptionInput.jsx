import React from "react";

export default function DescriptionInput({ value, setValue, error }) {
  const handleChange = (e) => {
    const input = e.target.value;

    if (input.length <= 300) {
      setValue(input);
    }
  };

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Property Description <span className="text-red-500">*</span>
      </label>

      <textarea
        value={value}
        onChange={handleChange}
        placeholder="e.g. A modern 3-bedroom apartment with rooftop access, large windows, and luxury finishes..."
        className={`w-full p-3 border rounded shadow-sm focus:outline-none focus:ring-2 ${
          error ? "border-red-500 ring-red-300" : "border-gray-300 focus:ring-blue-400"
        }`}
        rows={4}
        required
      />

      <p className="text-xs text-gray-500 mt-1">
        {300 - value.length} characters left
      </p>

      {error && (
        <p className="text-xs text-red-600 mt-1">
          Property description is required.
        </p>
      )}
    </div>
  );
}
