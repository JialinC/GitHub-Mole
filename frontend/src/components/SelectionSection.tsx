import React from "react";

interface SelectionSectionProps {
  title: string;
  description: React.ReactNode;
  items: string[][];
  selectedItems: Set<string> | string;
  handleChange: (item: string) => void;
  isCheckbox: boolean;
}

const SelectionSection: React.FC<SelectionSectionProps> = ({
  title,
  description,
  items,
  selectedItems,
  handleChange,
  isCheckbox,
}) => {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-bold text-white mb-4">{title}</h3>
      <p className="text-gray-300 mb-4">{description}</p>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {items.map((chunk, chunkIndex) => (
          <div key={chunkIndex} className="space-y-2">
            {chunk.map((item) => (
              <label
                key={item}
                className="flex items-center text-gray-300 hover:text-white"
              >
                <input
                  type={isCheckbox ? "checkbox" : "radio"}
                  name={isCheckbox ? undefined : "contribution"}
                  value={item}
                  checked={
                    isCheckbox
                      ? (selectedItems as Set<string>).has(item)
                      : selectedItems === item
                  }
                  onChange={() => handleChange(item)}
                  className="w-4 h-4 mr-2 text-blue-600 bg-gray-800 border-gray-700 rounded focus:ring-blue-500"
                />
                {item}
              </label>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SelectionSection;
