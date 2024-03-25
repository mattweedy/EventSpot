import React from 'react';
import QuizForm from '../components/Quiz/QuizForm';
import { useOutletContext } from 'react-router-dom';
import { useDynamicHeight } from '../components/General/useDynamicHeight';

function Preferences() {
    const { userProfile, recommendedEventIds, setRecommendedEventIds, } = useOutletContext();
    useDynamicHeight();

    return (
        <div>
            <h1>Edit Preferences</h1>
            <QuizForm
                username={userProfile.display_name}
                recommendedEventIds={recommendedEventIds}
                setRecommendedEventIds={setRecommendedEventIds} />
        </div>
    );
}

export default Preferences;