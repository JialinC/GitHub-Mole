import React from "react";

interface ModalProps {
  title: string;
  message: string;
  onClose: () => void;
}

const Modal: React.FC<ModalProps> = ({ title, message, onClose }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-gray-900 text-white rounded-lg shadow-lg p-8 w-1/3">
        <h2 className="text-3xl font-bold mb-6">{title}</h2>
        <p className="mb-6">{message}</p>
        <button
          onClick={onClose}
          className="bg-green-500 text-white font-bold py-2 px-6 rounded hover:bg-green-700 transition duration-150"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default Modal;
