import React from "react";

interface ButtonProps {
  handleAction: () => void;
  text: string;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ handleAction, text, disabled }) => {
  return (
    <div className="mt-6">
      <button
        {...(disabled !== undefined && { disabled })}
        onClick={handleAction}
        className="w-full bg-red-600 hover:bg-red-800 text-white font-semibold py-3 rounded-lg shadow-md transition duration-200"
      >
        {text}
      </button>
    </div>
  );
};

export default Button;
