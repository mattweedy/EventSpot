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
            <p>These preferences will provide further context for what kind of event you are looking for, on top of your listening history.</p>
            <p><span>Note:</span> Available venues to select are based on upcoming events</p>
            <QuizForm
                username={userProfile.display_name}
                setRecommendedEventIds={setRecommendedEventIds} />
        </div>
    );
}

export default Preferences;