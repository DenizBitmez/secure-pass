import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Generator from './pages/Generator';
import TwoFactorSetup from './pages/TwoFactorSetup';
import Share from './pages/Share';
import ShareView from './pages/ShareView';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white font-sans">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Private Routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/generator"
            element={
              <PrivateRoute>
                <Generator />
              </PrivateRoute>
            }
          />
          <Route
            path="/2fa"
            element={
              <PrivateRoute>
                <TwoFactorSetup />
              </PrivateRoute>
            }
          />
          <Route
            path="/share"
            element={
              <PrivateRoute>
                <Share />
              </PrivateRoute>
            }
          />

          {/* Public Routes */}
          <Route path="/share/:uuid" element={<ShareView />} />

          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </div>
    </Router>
  );
}
