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
            <header>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <p style={{ display: 'flex', alignItems: 'center', position: 'absolute', top: '0', right: '0', marginRight: '5px' }}>logged out</p>

                    <h1 style={{ alignItems: 'center', marginTop: '10px', marginBottom: '0px' }}>
                        Spot<span style={{ color: '#888fff' }}>Event</span>
                    </h1>

                    <h2 style={{ marginTop: '0px' }}>
                        Music Event Discovery
                    </h2>                    
                </div>
            </header>
        );
    } else if (isLoggedIn) {
        return (
            <header style={{ margin: '0'}}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <div className="user-profile" style={{ display: 'flex', alignItems: 'center', position: 'absolute', top: '0', right: '0' }}>
                        {windowWidth > 768 && <span style={{ marginRight: '0.3em', color: '#888fff' }}>{userProfile.display_name}</span>}
                        {windowWidth > 768 && <p>logged in</p>}
                        <img src={userProfile.images[0].url} alt="user profile" style={{ borderRadius: '50%', border: '3px solid black', scale: '65%', marginRight: '0px' }}/>
                    </div>

                    <h1 style={{ alignItems: 'center', marginTop: '10px', marginBottom: '0px' }}>
                        Spot<span style={{ color: '#888fff' }}>Event</span>
                    </h1>

                    <h2 style={{ marginTop: '0px' }}>
                        Music Event Discovery
                    </h2>
                </div>
            </header>
        );
    }
}

export default Header;