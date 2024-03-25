import React, { useState, useEffect } from 'react';
import Logout from '../Login/Logout';

function Header({ userProfile, isLoggedIn }) {
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);

    useEffect(() => {
        const handleResize = () => setWindowWidth(window.innerWidth);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    if (!isLoggedIn) {
        return (
            <header className="header">
                <div className="header-content">
                    <div className="header-title-container">
                        <h1 className="header-title">Spot<span>Event</span></h1>
                        <h2 className="header-subtitle">Music Event Discovery</h2>
                    </div>
                </div>
            </header>
        );
    } else if (isLoggedIn) {
        return (
            <header className="header">
                <div className="header-content">
                    <div className="user-profile">
                            <img src={userProfile.images[0].url} alt="user profile" />
                            {windowWidth > 940 && <span>{userProfile.display_name}</span>}
                            {windowWidth > 940 && <p>logged in</p>}
                    </div>
                    <div className="header-title-container">
                        <h1 className="header-title">Spot<span>Event</span></h1>
                        <h2 className="header-subtitle">Music Event Discovery</h2>
                    </div>
                    <div className="logout-container">
                        <Logout />
                    </div>
                </div>
            </header>
        );
    }
}

export default Header;