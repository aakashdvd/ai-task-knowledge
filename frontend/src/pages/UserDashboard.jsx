import { useEffect, useState } from "react";
import api from "../api/client";
import SearchPanel from "../components/SearchPanel";
import TaskList from "../components/TaskList";
import { useAuth } from "../context/AuthContext";

export default function UserDashboard() {
    const { user, logout } = useAuth();
    const [tasks, setTasks] = useState([]);
    const [loadingTasks, setLoadingTasks] = useState(true);

    const loadTasks = async () => {
        setLoadingTasks(true);
        try {
            const response = await api.get("/tasks");
            setTasks(response.data);
        } finally {
            setLoadingTasks(false);
        }
    };

    const markComplete = async (taskId) => {
        await api.patch(`/tasks/${taskId}/status`, {
            status: "completed",
        });
        await loadTasks();
    };

    useEffect(() => {
        loadTasks();
    }, []);

    return (
        <div className="app-shell">
            <header className="topbar">
                <div>
                    <p className="eyebrow">User Workspace</p>
                    <h1>Hello, {user?.full_name}</h1>
                </div>
                <button className="secondary-button" onClick={logout}>
                    Logout
                </button>
            </header>

            <div className="dashboard-grid">
                <TaskList
                    tasks={tasks}
                    loading={loadingTasks}
                    canComplete
                    onComplete={markComplete}
                    title="My Tasks"
                />
                <SearchPanel />
            </div>
        </div>
    );
}