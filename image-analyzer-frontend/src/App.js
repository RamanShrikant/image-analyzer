import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please choose an image");

    const formData = new FormData();
    formData.append("image", file);

    setLoading(true);
    try {
      const response = await fetch(
        "https://image-analyzer-production-f217.up.railway.app/analyze-freshness",
        { method: "POST", body: formData }
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Error analyzing image");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getColor = (label) => {
    if (label === "Fresh") return "🟢";
    if (label === "Slightly Aging") return "🟡";
    return "🔴";
  };

  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <h1>Image Analyzer</h1>
      <p>Upload an image to check freshness.</p>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Status: {getColor(result.status)} {result.status}</h2>
          <p>Confidence: {result.confidence?.toFixed(2)}%</p>
          <h3>Model Predictions:</h3>
          <div style={{ width: "300px", margin: "auto", textAlign: "left" }}>
            {Object.entries(result.predictions).map(([label, value]) => (
              <div key={label} style={{ margin: "0.5rem 0" }}>
                <strong>{label}</strong>
                <div
                  style={{
                    height: "10px",
                    width: `${value * 3}px`,
                    background:
                      label === "Fresh"
                        ? "#00cc66"
                        : label === "Slightly Aging"
                        ? "#ffcc00"
                        : "#ff4444",
                  }}
                ></div>
                <span>{value.toFixed(2)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
