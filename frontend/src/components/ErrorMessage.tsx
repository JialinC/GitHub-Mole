import React from "react";

interface ErrorMessageProps {
  error: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ error }) => {
  return (
    <div className="mt-2 text-sm text-red-500">
      <span className="font-medium">Error:</span> {error}
    </div>
  );
};

export default ErrorMessage;
