import React from 'react';
import { useDynamicHeight } from '../components/General/useDynamicHeight';

function Home() {
    useDynamicHeight();

    // TODO: add code to route user to edit preferences page
    // TODO: pretty up the home page and the buttons (maybe div with different colors, etc.)

    return (
        <div className="home-page">
            <h1 className="home-page-title">Welcome to the Home Page</h1>
            {/* TODO : make the preferences a link (?) */}
            <h2 className="home-page-text">If you're new here, it is best to setup your <span>preferences</span>.</h2>
            <p className="home-page-text">Don't worry, you can change these at any time.</p>

            <button className="edit-preferences-button" id="preferences-form-button" onClick={() => { /* code to route user to edit preferences page */ }}>
                Edit Preferences
            </button>
        </div>
    );
}

export default Home;