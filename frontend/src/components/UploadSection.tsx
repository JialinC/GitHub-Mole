import React from "react";

interface UploadSectionProps {
  demoImage: string;
  handleFileChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  title: string;
  description: React.ReactNode;
}

const UploadSection: React.FC<UploadSectionProps> = ({
  demoImage,
  handleFileChange,
  title,
  description,
}) => {
  return (
    <div>
      <h3 className="text-lg font-bold text-white mb-4">{title}</h3>
      <p className="text-gray-300 mb-4">{description}</p>
      <div className="mb-6">
        <img
          src={demoImage}
          alt="Example file"
          className="rounded-lg shadow-md border border-gray-700"
        />
      </div>
      <label className="block mb-4">
        <span className="block text-sm font-medium text-gray-400 mb-2">
          Upload CSV File
        </span>
        <input
          type="file"
          id="file"
          accept=".csv"
          onChange={handleFileChange}
          className="w-full p-3 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:ring-2 focus:ring-blue-500"
        />
      </label>
    </div>
  );
};

export default UploadSection;
