import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../api/client";

const AuthContext = createContext(null);

function getStoredUser() {
    const raw = localStorage.getItem("atk_user");
    return raw ? JSON.parse(raw) : null;
}

export function AuthProvider({ children }) {
    const [token, setToken] = useState(localStorage.getItem("atk_token"));
    const [user, setUser] = useState(getStoredUser());
    const [loading, setLoading] = useState(false);

    const login = async (email, password) => {
        setLoading(true);
        try {
            const response = await api.post("/auth/login", { email, password });
            const { access_token, user: userData } = response.data;

            localStorage.setItem("atk_token", access_token);
            localStorage.setItem("atk_user", JSON.stringify(userData));

            setToken(access_token);
            setUser(userData);

            return userData;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("atk_token");
        localStorage.removeItem("atk_user");
        setToken(null);
        setUser(null);
    };

    useEffect(() => {
        const rawToken = localStorage.getItem("atk_token");
        const rawUser = getStoredUser();
        if (rawToken && rawUser) {
            setToken(rawToken);
            setUser(rawUser);
        }
    }, []);

    const value = useMemo(
        () => ({
            token,
            user,
            loading,
            isAuthenticated: Boolean(token && user),
            login,
            logout,
        }),
        [token, user, loading]
    );

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) {
        throw new Error("useAuth must be used inside AuthProvider");
    }
    return ctx;
}