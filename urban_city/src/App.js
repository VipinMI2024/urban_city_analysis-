import React, { useState, useEffect } from "react";
import "./index.css";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Bar, Pie } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

export default function App() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [mlFile, setMLFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [summaryGraphs, setSummaryGraphs] = useState([]);
  const [mapUrl, setMapUrl] = useState(null);

  const [mlType, setMlType] = useState("");
  const [mlResult, setMLResult] = useState(null);

  // -------------------------
  // Fetch static insights
  // -------------------------
  const fetchInsights = async () => {
    setLoading(true);
    try {
      const endpoints = ["population", "air_quality", "traffic", "infrastructure", "economy"];
      const responses = await Promise.all(
        endpoints.map((ep) => fetch(`http://127.0.0.1:8000/${ep}`).then((res) => res.json()))
      );
      setData({
        population: responses[0],
        air_quality: responses[1],
        traffic: responses[2],
        infrastructure: responses[3],
        economy: responses[4],
      });
    } catch (err) {
      console.error("Error fetching insights:", err);
    } finally {
      setLoading(false);
    }
  };

  // -------------------------
  // File Upload
  // -------------------------
  const handleUpload = (e) => setFile(e.target.files[0]);
  const handleMLUpload = (e) => setMLFile(e.target.files[0]);

  const uploadFileToServer = async () => {
    if (!file) return alert("Please select a file first!");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://127.0.0.1:8000/upload", { method: "POST", body: formData });
      if (res.ok) alert("File uploaded successfully!");
      else alert("Upload failed!");
    } catch (err) {
      console.error("Upload error:", err);
    }
  };

  // -------------------------
  // Summary + Graphs
  // -------------------------
  const fetchSummary = async () => {
    if (!file) return alert("Upload a dataset first.");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://127.0.0.1:8000/analytics/summary", { method: "POST", body: formData });
      const result = await res.json();
      setSummary(result.summary);
      generateSummaryGraphs(result.summary);
    } catch (err) {
      console.error("Summary error:", err);
    }
  };

  const generateSummaryGraphs = (summaryData) => {
    const graphs = [];
    Object.entries(summaryData).forEach(([col, stats]) => {
      try {
        // Numeric columns
        if (
          stats.count !== undefined &&
          stats.mean !== undefined &&
          stats.min !== undefined &&
          stats.max !== undefined &&
          !isNaN(stats.mean) &&
          !isNaN(stats.min) &&
          !isNaN(stats.max)
        ) {
          graphs.push({
            col,
            type: "bar",
            data: {
              labels: ["Min", "Mean", "Max"],
              datasets: [
                {
                  label: col,
                  data: [stats.min, stats.mean, stats.max],
                  backgroundColor: ["#3b82f6", "#10b981", "#f59e0b"],
                },
              ],
            },
          });
        }

        // Categorical columns
        if (stats.top !== undefined && stats.freq !== undefined && !isNaN(stats.freq)) {
          graphs.push({
            col,
            type: "pie",
            data: {
              labels: [stats.top, `Others`],
              datasets: [
                {
                  label: col,
                  data: [stats.freq, stats.count - stats.freq || 0],
                  backgroundColor: ["#f97316", "#3b82f6"],
                },
              ],
            },
          });
        }
      } catch (err) {
        console.warn(`Skipping column ${col} due to error:`, err);
      }
    });
    setSummaryGraphs(graphs);
  };

  // -------------------------
  // Map
  // -------------------------
  const generateMap = async () => {
    if (!file) return alert("Upload a dataset with LAT & LONG columns first.");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://127.0.0.1:8000/map/folium", { method: "POST", body: formData });
      const result = await res.json();
      if (result.map_url) setMapUrl(`http://127.0.0.1:8000${result.map_url}`);
    } catch (err) {
      console.error("Map error:", err);
    }
  };

  // -------------------------
  // ML Insights
  // -------------------------
  const fetchMLResults = async () => {
    if (!mlFile || !mlType) return alert("Upload ML dataset and select insight type!");
    const formData = new FormData();
    formData.append("file", mlFile);
    formData.append("ml_type", mlType);
    try {
      const res = await fetch("http://127.0.0.1:8000/ml/insight", { method: "POST", body: formData });
      const result = await res.json();
      setMLResult(result);
    } catch (err) {
      console.error("ML error:", err);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  const isArrayOfNumbers = (arr) =>
    Array.isArray(arr) && arr.length > 0 && typeof arr[0] === "number";

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      {/* Navbar */}
      <nav className="bg-gray-800 sticky top-0 w-full shadow-md z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Urban City Analytics</h1>
          <button
            onClick={fetchInsights}
            className="px-4 py-2 bg-green-600 hover:bg-green-500 rounded-lg transition"
          >
            {loading ? "Refreshing..." : "Refresh Data"}
          </button>
        </div>
      </nav>

      <section className="bg-gray-800 rounded-lg p-6 max-w-6xl mx-auto my-10">
        <h3 className="text-2xl font-bold mb-4">Upload Dataset</h3>
        <div className="flex gap-4 mb-4">
          <input type="file" accept=".csv" onChange={handleUpload} />
          <button onClick={uploadFileToServer} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded">
            Upload
          </button>
        </div>

        <div className="flex gap-4 mb-4">
          <button onClick={fetchSummary} className="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded">
            Get Summary
          </button>
          <button onClick={generateMap} className="px-4 py-2 bg-teal-600 hover:bg-teal-500 rounded">
            Generate Map
          </button>
        </div>

        {/* Summary Graphs */}
        {summaryGraphs.length > 0 && (
          <div className="my-4 flex flex-wrap gap-4">
            {summaryGraphs.map((graph, idx) => (
              <div key={idx} className="bg-gray-700 p-4 rounded">
                <h4 className="text-lg font-bold mb-2">{graph.col}</h4>
                {graph.type === "bar" && <Bar data={graph.data} />}
                {graph.type === "pie" && <Pie data={graph.data} />}
              </div>
            ))}
          </div>
        )}

        {/* Map */}
        {mapUrl && (
          <div className="bg-gray-700 p-4 rounded my-4">
            <h4 className="text-lg font-bold mb-2">Generated Map</h4>
            <iframe src={mapUrl} title="City Map" className="w-full h-96 rounded" />
          </div>
        )}

        {/* ML Insights */}
        <div className="bg-gray-800 rounded-lg p-6 my-4">
          <h3 className="text-2xl font-bold mb-4">ML Insights</h3>
          <div className="flex gap-4 mb-4">
            <input type="file" accept=".csv" onChange={handleMLUpload} />
            <select
              value={mlType}
              onChange={(e) => setMlType(e.target.value)}
              className="px-2 py-1 bg-gray-600 rounded text-white"
            >
              <option value="">Select ML Insight</option>
              <option value="population">Population Prediction</option>
              <option value="traffic">Traffic Forecast</option>
              <option value="air_quality">Air Quality Classification</option>
              <option value="infrastructure">Infrastructure Clustering</option>
            </select>
            <button onClick={fetchMLResults} className="px-4 py-2 bg-orange-600 hover:bg-orange-500 rounded">
              Generate Insight
            </button>
          </div>

          {mlResult && (
            <div className="my-4">
              {mlResult.prediction && isArrayOfNumbers(mlResult.prediction) && (
                <Bar
                  data={{
                    labels: mlResult.prediction.map((_, i) => i + 1),
                    datasets: [{ label: mlType, data: mlResult.prediction, backgroundColor: "#3b82f6" }],
                  }}
                />
              )}
              {mlResult.clusters && (
                <div className="text-gray-300 mt-4">
                  <h4 className="text-lg font-bold mb-2">Clusters</h4>
                  <p>{mlResult.clusters.join(", ")}</p>
                </div>
              )}
              {mlResult.prediction && !isArrayOfNumbers(mlResult.prediction) && mlResult.prediction.length > 0 && (
                <div className="text-gray-300 mt-4">
                  <h4 className="text-lg font-bold mb-2">Predictions</h4>
                  <p>{mlResult.prediction.join(", ")}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      <footer className="bg-gray-800 text-gray-400 text-center py-4">
        © {new Date().getFullYear()} Urban City Analytics. All Rights Reserved.
      </footer>
    </div>
  );
}
