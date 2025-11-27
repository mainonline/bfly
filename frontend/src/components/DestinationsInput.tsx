import { useState } from 'react';

interface DestinationsInputProps {
  value: string[];
  onChange: (value: string[]) => void;
}

export function DestinationsInput({ value, onChange }: DestinationsInputProps) {
  const [inputValue, setInputValue] = useState<string>("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const input = e.target.value;
    setInputValue(input);
    
    // Parse comma-separated cities
    const cities = input
      .split(",")
      .map(c => c.trim())
      .filter(c => c.length > 0);
    
    onChange(cities);
  };

  return (
    <div className="input-group">
      <label htmlFor="destinations">Destination Cities (comma-separated)</label>
      <input
        id="destinations"
        type="text"
        placeholder="e.g., Paris, Berlin, Madrid"
        value={inputValue}
        onChange={handleChange}
      />
      {value.length > 0 && (
        <div className="city-tags">
          {value.map((city, index) => (
            <span key={index} className="city-tag">
              {city}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
