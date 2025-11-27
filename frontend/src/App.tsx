import { useState } from 'react';
import { DepartureInput } from './components/DepartureInput';
import { DestinationsInput } from './components/DestinationsInput';
import { Results } from './components/Results';
import './App.css';

interface OptimizeRequest {
  from_city: string;
  to_cities: string[];
}

interface OptimizeResponse {
  destination: string;
  price_per_km: number;
  price_usd?: number;
  distance_km?: number;
  airport_from?: string;
  airport_to?: string;
}

function App() {
  const [fromCity, setFromCity] = useState<string>("");
  const [toCities, setToCities] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<OptimizeResponse | null>(null);

  const handleSubmit = async () => {
    if (!fromCity.trim()) {
      setError("Please enter a departure city");
      return;
    }

    if (toCities.length === 0) {
      setError("Please enter at least one destination city");
      return;
    }

    // Reset state
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      const requestBody: OptimizeRequest = {
        from_city: fromCity.trim(),
        to_cities: toCities,
      };

      const response = await fetch('/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to optimize flights');
      }

      const data: OptimizeResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>✈️ Flight Optimizer</h1>
        <p>Find the most cost-efficient destination by price per kilometer</p>
      </header>

      <main>
        <div className="form-container">
          <DepartureInput value={fromCity} onChange={setFromCity} />
          <DestinationsInput value={toCities} onChange={setToCities} />
          
          <button 
            onClick={handleSubmit} 
            disabled={loading}
            className="submit-button"
          >
            {loading ? 'Searching...' : 'Find Best Flight'}
          </button>
        </div>

        <Results result={result} loading={loading} error={error} />
      </main>

      <footer>
        <p>Powered by Kiwi.com Tequila API</p>
      </footer>
    </div>
  );
}

export default App;
