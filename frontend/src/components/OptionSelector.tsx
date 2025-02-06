import React from "react";

interface OptionSelectorProps {
  queryOption: string;
  handleOptionChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  optionValue: string;
  labelText: string;
}

const OptionSelector: React.FC<OptionSelectorProps> = ({
  queryOption,
  handleOptionChange,
  optionValue,
  labelText,
}) => {
  return (
    <div className="mb-4">
      <label className="text-md font-bold text-white mb-4">
        <input
          type="radio"
          name="queryOption"
          value={optionValue}
          checked={queryOption === optionValue}
          onChange={handleOptionChange}
          className="mr-2"
        />
        {labelText}
      </label>
    </div>
  );
};

export default OptionSelector;
