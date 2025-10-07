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
    <div
      style={{
        fontFamily: "Poppins, sans-serif",
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #f9fafb 0%, #e6f7f4 40%, #e8f0ff 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        color: "#333",
        padding: "1rem",
      }}
    >
      <div
        style={{
          background: "white",
          borderRadius: "20px",
          padding: "2rem 3rem",
          boxShadow: "0 8px 24px rgba(0,0,0,0.1)",
          textAlign: "center",
          width: "400px",
          maxWidth: "90%",
        }}
      >
        <h1 style={{ fontSize: "1.8rem", marginBottom: "0.5rem" }}>
          🍎 Image Analyzer
        </h1>
        <p style={{ marginBottom: "1.5rem", color: "#555" }}>
          Upload an image to check its freshness.
        </p>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "6px",
            marginRight: "10px",
          }}
        />
        <button
          onClick={handleUpload}
          disabled={loading}
          style={{
            background: "#4caf50",
            color: "white",
            border: "none",
            padding: "8px 15px",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        {result && (
          <div
            style={{
              marginTop: "2rem",
              borderTop: "1px solid #eee",
              paddingTop: "1.5rem",
              textAlign: "left",
            }}
          >
            <h2 style={{ textAlign: "center" }}>
              Status: {getColor(result.status)}{" "}
              <span style={{ color: "#111" }}>{result.status}</span>
            </h2>
            <p style={{ textAlign: "center", color: "#555" }}>
              Confidence: {result.confidence?.toFixed(2)}%
            </p>

            <h3 style={{ marginTop: "1.2rem", marginBottom: "0.5rem" }}>
              Model Predictions:
            </h3>

            {Object.entries(result.predictions).map(([label, value]) => (
              <div key={label} style={{ marginBottom: "0.7rem" }}>
                <strong>{label}</strong>
                <div
                  style={{
                    background: "#eee",
                    height: "10px",
                    borderRadius: "5px",
                    overflow: "hidden",
                    marginTop: "4px",
                    marginBottom: "2px",
                  }}
                >
                  <div
                    style={{
                      height: "10px",
                      width: `${value}%`,
                      background:
                        label === "Fresh"
                          ? "#00cc66"
                          : label === "Slightly Aging"
                          ? "#ffcc00"
                          : "#ff5555",
                      borderRadius: "5px",
                      transition: "width 0.6s ease",
                    }}
                  ></div>
                </div>
                <span style={{ fontSize: "0.9rem", color: "#555" }}>
                  {value.toFixed(2)}%
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
