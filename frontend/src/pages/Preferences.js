import React from 'react';
import QuizForm from '../components/Quiz/QuizForm';
import { useOutletContext } from 'react-router-dom';
import { useDynamicHeight } from '../components/General/useDynamicHeight';

function Preferences() {
    const { userProfile, setRecommendedEventIds, } = useOutletContext();

    useDynamicHeight();

    return (
        <div>
            <h1>Edit Preferences</h1>
            <p>Hitting <span>save</span> will redirect you to the recommended events page</p>
            <QuizForm
                username={userProfile.display_name}
                setRecommendedEventIds={setRecommendedEventIds} />
        </div>
    );
}

export default Preferences;