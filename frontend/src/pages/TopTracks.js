import React from 'react';

const TopTracks = () => {
    const tracks = [
        { id: 1, name: 'Track 1' },
        { id: 2, name: 'Track 2' },
        { id: 3, name: 'Track 3' },
    ];

    return (
        <div>
            <h1>Top Tracks</h1>
            <ul>
                {tracks.map(track => (
                    <li key={track.id}>{track.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default TopTracks;