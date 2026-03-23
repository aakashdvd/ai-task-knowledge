import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function routeByRole(roleName) {
    return roleName === "admin" ? "/admin" : "/user";
}

export default function LoginPage() {
    const { login, loading } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState("admin@example.com");
    const [password, setPassword] = useState("Admin@123");
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError("");

        try {
            const user = await login(email, password);
            navigate(routeByRole(user.role.name), { replace: true });
        } catch (err) {
            setError(err.response?.data?.detail || "Login failed.");
        }
    };

    return (
        <div className="auth-shell">
            <div className="auth-card">
                <p className="eyebrow">AI Task & Knowledge Management System</p>
                <h1>Welcome back</h1>
                <p className="muted">
                    Login as admin or user to test the full assignment flow.
                </p>

                <form onSubmit={handleSubmit} className="stack-form">
                    <label>
                        Email
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </label>

                    <label>
                        Password
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </label>

                    <button type="submit" disabled={loading}>
                        {loading ? "Signing in..." : "Login"}
                    </button>
                </form>

                {error && <p className="form-message error">{error}</p>}

                <div className="demo-credentials">
                    <p><strong>Admin:</strong> admin@example.com / Admin@123</p>
                    <p><strong>User:</strong> user@example.com / User@123</p>
                </div>
            </div>
        </div>
    );
}