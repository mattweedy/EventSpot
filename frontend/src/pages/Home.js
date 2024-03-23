import React, { useEffect, } from 'react';
import { useLocation } from 'react-router-dom';

function Home() {
    // TODO: apply this relevantly to pages that need certain heights
    const location = useLocation();

    useEffect(() => {
        const newHeight = location.pathname === '/events' ? '100vh' : '90vh';
        document.documentElement.style.setProperty('--dynamic-height', newHeight);
        console.log("Dynamic height set to:", newHeight);
    }, [location.pathname]);

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <p>This is the default home page of your application.</p>
        </div>
    );
}

export default Home;