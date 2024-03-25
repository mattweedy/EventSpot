import { useLocation } from 'react-router-dom';
import { useEffect } from 'react';

export function useDynamicHeight() {
    const location = useLocation();

    useEffect(() => {
        const newHeight = location.pathname === '/events' || location.pathname === '/preferences' ? '100vh' : '90vh';
        document.documentElement.style.setProperty('--dynamic-height', newHeight);
        console.log("Dynamic height set to:", newHeight);
    }, [location.pathname]);
}