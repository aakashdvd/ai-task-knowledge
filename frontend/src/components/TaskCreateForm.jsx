import { useState } from "react";
import api from "../api/client";

const initialState = {
    assigned_to: 2,
    title: "",
    description: "",
    due_date: "",
};

export default function TaskCreateForm({ onSuccess }) {
    const [formData, setFormData] = useState(initialState);
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState("");

    const updateField = (key, value) => {
        setFormData((prev) => ({ ...prev, [key]: value }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setSubmitting(true);
        setMessage("");

        try {
            await api.post("/tasks", {
                assigned_to: Number(formData.assigned_to),
                title: formData.title,
                description: formData.description || null,
                due_date: formData.due_date
                    ? new Date(formData.due_date).toISOString()
                    : null,
            });

            setMessage("Task created successfully.");
            setFormData(initialState);
            onSuccess?.();
        } catch (error) {
            setMessage(error.response?.data?.detail || "Task creation failed.");
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="card">
            <div className="section-header">
                <h2>Create Task</h2>
                <span className="badge">Admin</span>
            </div>

            <form onSubmit={handleSubmit} className="stack-form">
                <label>
                    Assigned User ID
                    <input
                        type="number"
                        value={formData.assigned_to}
                        onChange={(e) => updateField("assigned_to", e.target.value)}
                    />
                </label>

                <label>
                    Title
                    <input
                        type="text"
                        value={formData.title}
                        onChange={(e) => updateField("title", e.target.value)}
                        placeholder="Complete onboarding checklist"
                    />
                </label>

                <label>
                    Description
                    <textarea
                        rows="4"
                        value={formData.description}
                        onChange={(e) => updateField("description", e.target.value)}
                        placeholder="Read the uploaded document and complete the setup task."
                    />
                </label>

                <label>
                    Due Date
                    <input
                        type="datetime-local"
                        value={formData.due_date}
                        onChange={(e) => updateField("due_date", e.target.value)}
                    />
                </label>

                <button type="submit" disabled={submitting}>
                    {submitting ? "Creating..." : "Create Task"}
                </button>
            </form>

            <p className="muted">
                Seeded demo user is usually ID 2.
            </p>

            {message && <p className="form-message">{message}</p>}
        </div>
    );
}