interface OptimizeResponse {
  destination: string;
  price_per_km: number;
  price_usd?: number;
  distance_km?: number;
  airport_from?: string;
  airport_to?: string;
}

interface ResultsProps {
  result: OptimizeResponse | null;
  loading: boolean;
  error: string | null;
}

export function Results({ result, loading, error }: ResultsProps) {
  if (loading) {
    return (
      <div className="results loading">
        <div className="spinner"></div>
        <p>Searching for the best flights...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results error">
        <h3>Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="results success">
      <h2>Best Destination</h2>
      <div className="result-card">
        <div className="destination-name">{result.destination}</div>
        <div className="price-per-km">
          ${result.price_per_km.toFixed(2)}/km
        </div>
        {result.price_usd && (
          <div className="detail">
            <span className="label">Price:</span>
            <span className="value">${result.price_usd.toFixed(2)}</span>
          </div>
        )}
        {result.distance_km && (
          <div className="detail">
            <span className="label">Distance:</span>
            <span className="value">{result.distance_km.toFixed(0)} km</span>
          </div>
        )}
        {result.airport_from && result.airport_to && (
          <div className="detail">
            <span className="label">Route:</span>
            <span className="value">{result.airport_from} → {result.airport_to}</span>
          </div>
        )}
      </div>
    </div>
  );
}
