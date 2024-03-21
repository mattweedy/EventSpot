import React, { useState, useEffect } from 'react';

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
                    <p id="logged-out-status">logged out</p>
                    <h1 className="header-title">Spot<span>Event</span></h1>
                    <h2 className="header-subtitle">Music Event Discovery</h2>
                </div>
            </header>
        );
    } else if (isLoggedIn) {
        return (
            <header className="header">
                <div className="header-content">
                    <div className="user-profile">
                        {windowWidth > 768 && <span>{userProfile.display_name}</span>}
                        {windowWidth > 768 && <p>logged in</p>}
                        <img src={userProfile.images[0].url} alt="user profile" />
                    </div>
                    <h1 className="header-title">Spot<span>Event</span></h1>
                    <h2 className="header-subtitle">Music Event Discovery</h2>
                </div>
            </header>
        );
    }
}

export default Header;