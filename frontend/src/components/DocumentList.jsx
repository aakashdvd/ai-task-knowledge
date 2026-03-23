export default function DocumentList({ documents, loading }) {
    return (
        <div className="card">
            <div className="section-header">
                <h2>Uploaded Documents</h2>
                <span className="badge">{documents.length}</span>
            </div>

            {loading ? (
                <p>Loading documents...</p>
            ) : documents.length === 0 ? (
                <p className="muted">No documents uploaded yet.</p>
            ) : (
                <div className="list-wrap">
                    {documents.map((doc) => (
                        <div className="list-row" key={doc.id}>
                            <div>
                                <strong>{doc.original_filename}</strong>
                                <p className="muted">
                                    Status: {doc.upload_status} | Chunks: {doc.total_chunks}
                                </p>
                            </div>
                            <span className="pill">{doc.mime_type || "text/plain"}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}