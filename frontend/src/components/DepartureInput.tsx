interface DepartureInputProps {
  value: string;
  onChange: (value: string) => void;
}

export function DepartureInput({ value, onChange }: DepartureInputProps) {
  return (
    <div className="input-group">
      <label htmlFor="departure">Departure City</label>
      <input
        id="departure"
        type="text"
        placeholder="e.g., London"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
