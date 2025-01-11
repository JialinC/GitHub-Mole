import React from "react";

interface ButtonProps {
  handleAction: () => void;
  text: string;
}

const Button: React.FC<ButtonProps> = ({ handleAction, text }) => {
  return (
    <div className="mt-6">
      <button
        onClick={handleAction}
        className="w-full bg-red-600 hover:bg-red-800 text-white font-semibold py-3 rounded-lg shadow-md transition duration-200"
      >
        {text}
      </button>
    </div>
  );
};

export default Button;
