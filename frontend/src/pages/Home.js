import React from 'react';
import { useDynamicHeight } from '../components/General/useDynamicHeight';

function Home() {
    useDynamicHeight();

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <p>This is the default home page of your application.</p>
        </div>
    );
}

export default Home;