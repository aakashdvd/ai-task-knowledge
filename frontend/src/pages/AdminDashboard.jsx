import { useEffect, useState } from "react";
import api from "../api/client";
import AnalyticsPanel from "../components/AnalyticsPanel";
import DocumentList from "../components/DocumentList";
import DocumentUploadForm from "../components/DocumentUploadForm";
import TaskCreateForm from "../components/TaskCreateForm";
import TaskList from "../components/TaskList";
import { useAuth } from "../context/AuthContext";

export default function AdminDashboard() {
    const { user, logout } = useAuth();

    const [analytics, setAnalytics] = useState(null);
    const [documents, setDocuments] = useState([]);
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadDashboard = async () => {
        setLoading(true);
        try {
            const [analyticsRes, documentsRes, tasksRes] = await Promise.all([
                api.get("/analytics"),
                api.get("/documents"),
                api.get("/tasks"),
            ]);

            setAnalytics(analyticsRes.data);
            setDocuments(documentsRes.data);
            setTasks(tasksRes.data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDashboard();
    }, []);

    return (
        <div className="app-shell">
            <header className="topbar">
                <div>
                    <p className="eyebrow">Admin Dashboard</p>
                    <h1>Hello, {user?.full_name}</h1>
                </div>
                <button className="secondary-button" onClick={logout}>
                    Logout
                </button>
            </header>

            <div className="dashboard-grid">
                <AnalyticsPanel analytics={analytics} loading={loading} />

                <DocumentUploadForm onSuccess={loadDashboard} />
                <TaskCreateForm onSuccess={loadDashboard} />

                <DocumentList documents={documents} loading={loading} />
                <TaskList tasks={tasks} loading={loading} title="All Tasks" />
            </div>
        </div>
    );
}