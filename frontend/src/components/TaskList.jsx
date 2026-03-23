export default function TaskList({
    tasks,
    loading,
    canComplete = false,
    onComplete,
    title = "Tasks",
}) {
    return (
        <div className="card">
            <div className="section-header">
                <h2>{title}</h2>
                <span className="badge">{tasks.length}</span>
            </div>

            {loading ? (
                <p>Loading tasks...</p>
            ) : tasks.length === 0 ? (
                <p className="muted">No tasks found.</p>
            ) : (
                <div className="list-wrap">
                    {tasks.map((task) => (
                        <div className="list-row task-row" key={task.id}>
                            <div className="task-main">
                                <strong>{task.title}</strong>
                                <p className="muted">{task.description || "No description"}</p>
                                <p className="tiny-text">
                                    Assigned To: {task.assigned_to} | Status: {task.status}
                                </p>
                            </div>

                            <div className="task-actions">
                                <span className={`pill ${task.status === "completed" ? "pill-success" : ""}`}>
                                    {task.status}
                                </span>

                                {canComplete && task.status !== "completed" && (
                                    <button onClick={() => onComplete(task.id)}>Mark Complete</button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}