import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please choose an image");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {   // 🔴 replace with your Flask backend URL
        method: "POST",
        body: formData,
      });

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
      <button onClick={handleUpload}>Analyze</button>

      {loading && <p>Analyzing...</p>}

      {result && (
        <div>
          <h2>Freshness Score: {result.freshness}/100</h2>
          <p>Spots Detected: {result.spots}</p>
          <p>Brightness: {result.brightness}</p>
        </div>
      )}
    </div>
  );
}

export default App;
