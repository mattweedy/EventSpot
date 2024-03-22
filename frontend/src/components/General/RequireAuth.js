import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const RequireAuth = ({ children }) => {
    const { isLoggedIn } = useAuth();

    return isLoggedIn ? children : <Navigate to="/login" replace />;
};

export default RequireAuth;
