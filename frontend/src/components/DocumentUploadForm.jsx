import { useState } from "react";
import api from "../api/client";

export default function DocumentUploadForm({ onSuccess }) {
    const [file, setFile] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            setMessage("Please choose a .txt file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        setSubmitting(true);
        setMessage("");

        try {
            await api.post("/documents", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setMessage("Document uploaded and indexed successfully.");
            setFile(null);
            event.target.reset();
            onSuccess?.();
        } catch (error) {
            setMessage(
                error.response?.data?.detail || "Document upload failed."
            );
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="card">
            <div className="section-header">
                <h2>Upload Document</h2>
                <span className="badge">.txt</span>
            </div>

            <form onSubmit={handleSubmit} className="stack-form">
                <input
                    type="file"
                    accept=".txt,text/plain"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                />
                <button type="submit" disabled={submitting}>
                    {submitting ? "Uploading..." : "Upload"}
                </button>
            </form>

            {message && <p className="form-message">{message}</p>}
        </div>
    );
}