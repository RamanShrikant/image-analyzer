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
      const response = await fetch("https://image-analyzer-production-f217.up.railway.app/analyze-freshness", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze image");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Error analyzing image");
    }
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <h1>Image Analyzer</h1>
      <p>Upload an image to get started.</p>

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
    <h2>Freshness Score: {result.freshness_score}/100</h2>
    <p>Spots Detected: {result.spots_detected}</p>
    <p>Brightness: {result.brightness}</p>
    <h3>
      Status:{" "}
      {result.status === "Fresh" ? "🟢 Fresh" :
       result.status === "Slightly Aging" ? "🟡 Slightly Aging" :
       "🔴 Expiring Soon"}
    </h3>
  </div>
)}

    </div>
  );
}

export default App;
