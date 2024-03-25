import React from 'react';
import QuizForm from '../components/Quiz/QuizForm';
import { useOutletContext } from 'react-router-dom';

function Preferences() {
    const { userProfile, recommendedEventIds, setRecommendedEventIds, isFormSubmitted, setIsFormSubmitted } = useOutletContext();

    return (
        <div>
            <QuizForm
                username={userProfile.display_name}
                recommendedEventIds={recommendedEventIds}
                setRecommendedEventIds={setRecommendedEventIds}
                setIsFormSubmitted={setIsFormSubmitted} />
        </div>
    );
}

export default Preferences;