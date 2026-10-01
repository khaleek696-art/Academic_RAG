import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Loader2 } from 'lucide-react';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-slate-950 text-indigo-400 font-mono text-xs gap-2">
        <Loader2 className="w-5 h-5 animate-spin" /> Verifying Authentication Status...
      </div>
    );
  }

  if (!user) {
    // Redirect to /login if not logged in, keeping target path in state
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
