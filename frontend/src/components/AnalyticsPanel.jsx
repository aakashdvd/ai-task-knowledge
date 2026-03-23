export default function AnalyticsPanel({ analytics, loading }) {
    if (loading) {
        return <div className="card">Loading analytics...</div>;
    }

    if (!analytics) {
        return <div className="card">No analytics available yet.</div>;
    }

    return (
        <div className="card">
            <div className="section-header">
                <h2>Analytics Overview</h2>
                <span className="badge">Admin</span>
            </div>

            <div className="stats-grid">
                <div className="stat-box">
                    <span>Total Tasks</span>
                    <strong>{analytics.total_tasks}</strong>
                </div>
                <div className="stat-box">
                    <span>Completed Tasks</span>
                    <strong>{analytics.completed_tasks}</strong>
                </div>
                <div className="stat-box">
                    <span>Pending Tasks</span>
                    <strong>{analytics.pending_tasks}</strong>
                </div>
                <div className="stat-box">
                    <span>Total Documents</span>
                    <strong>{analytics.total_documents}</strong>
                </div>
                <div className="stat-box">
                    <span>Total Searches</span>
                    <strong>{analytics.total_searches}</strong>
                </div>
            </div>

            <div className="subsection">
                <h3>Top Searches</h3>
                {analytics.top_searches?.length ? (
                    <ul className="simple-list">
                        {analytics.top_searches.map((item) => (
                            <li key={item.query_text}>
                                <span>{item.query_text}</span>
                                <strong>{item.count}</strong>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="muted">No searches recorded yet.</p>
                )}
            </div>
        </div>
    );
}