import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function defaultRouteForRole(roleName) {
    return roleName === "admin" ? "/admin" : "/user";
}

export default function ProtectedRoute({ children, allowedRoles }) {
    const { isAuthenticated, user } = useAuth();

    if (!isAuthenticated || !user) {
        return <Navigate to="/login" replace />;
    }

    const roleName = user.role?.name?.toLowerCase();
    if (!allowedRoles.includes(roleName)) {
        return <Navigate to={defaultRouteForRole(roleName)} replace />;
    }

    return children;
}