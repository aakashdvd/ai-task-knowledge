import { useState } from "react";
import api from "../api/client";

export default function SearchPanel() {
    const [query, setQuery] = useState("");
    const [topK, setTopK] = useState(5);
    const [includeAnswer, setIncludeAnswer] = useState(false);
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState(null);
    const [error, setError] = useState("");

    const handleSearch = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError("");
        setResultData(null);

        try {
            const response = await api.post(
                `/search${includeAnswer ? "?include_answer=true" : ""}`,
                {
                    query,
                    top_k: Number(topK),
                }
            );
            setResultData(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || "Search failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <div className="section-header">
                <h2>Semantic Search</h2>
                <span className="badge">AI</span>
            </div>

            <form onSubmit={handleSearch} className="stack-form">
                <label>
                    Search Query
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="How do I complete onboarding?"
                    />
                </label>

                <label>
                    Top K
                    <input
                        type="number"
                        min="1"
                        max="10"
                        value={topK}
                        onChange={(e) => setTopK(e.target.value)}
                    />
                </label>

                <label className="checkbox-row">
                    <input
                        type="checkbox"
                        checked={includeAnswer}
                        onChange={(e) => setIncludeAnswer(e.target.checked)}
                    />
                    Include grounded Gemini answer
                </label>

                <button type="submit" disabled={loading}>
                    {loading ? "Searching..." : "Search"}
                </button>
            </form>

            {error && <p className="form-message error">{error}</p>}

            {resultData && (
                <div className="subsection">
                    <h3>Results</h3>

                    {resultData.results.length === 0 ? (
                        <p className="muted">
                            No relevant results found.
                        </p>
                    ) : (
                        <div className="list-wrap">
                            {resultData.results.map((item, index) => (
                                <div className="search-result" key={`${item.document_id}-${item.chunk_index}-${index}`}>
                                    <div className="section-header small-gap">
                                        <strong>{item.filename}</strong>
                                        <span className="pill">Score: {item.score}</span>
                                    </div>
                                    <p className="tiny-text">
                                        Document ID: {item.document_id} | Chunk: {item.chunk_index}
                                    </p>
                                    <p>{item.text}</p>
                                </div>
                            ))}
                        </div>
                    )}

                    {resultData.answer && (
                        <div className="answer-box">
                            <h3>Grounded Answer</h3>
                            <p>{resultData.answer}</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}