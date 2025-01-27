import React, { useState, useEffect } from "react";

interface PromptProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (name: string) => void;
  errorMessage: string | null;
}

const Prompt: React.FC<PromptProps> = ({
  isOpen,
  onClose,
  onSave,
  errorMessage,
}) => {
  const [datasetName, setDatasetName] = useState("");

  useEffect(() => {
    if (!isOpen) {
      setDatasetName(""); // Clear the datasetName when the modal is closed
    }
  }, [isOpen]);

  const handleSave = () => {
    onSave(datasetName);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-gray-900 text-white rounded-lg shadow-lg p-8 w-96">
        <h2 className="text-3xl font-bold mb-6 text-center">Save Dataset</h2>
        <input
          type="text"
          value={datasetName}
          onChange={(e) => setDatasetName(e.target.value)}
          className="w-full px-3 py-2 mb-4 border border-gray-700 rounded bg-gray-800 text-white"
          placeholder="Enter dataset name"
        />
        <div className="flex justify-between">
          <button
            onClick={onClose}
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded w-1/2 mr-2"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-1/2 ml-2"
          >
            Save
          </button>
        </div>
        {errorMessage && (
          <div className="text-red-500 text-xs mt-4">{errorMessage}</div>
        )}
      </div>
    </div>
  );
};

export default Prompt;
