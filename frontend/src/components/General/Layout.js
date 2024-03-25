import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "../Sidebar/Sidebar";
import LoginPage from "../../pages/LoginPage";
import { Suspense } from "react";


export default function Layout({ userProfile, isLoggedIn, accessToken, recommendedEventIds, setRecommendedEventIds, isFormSubmitted, setIsFormSubmitted }) {
    return (
        <div className="papp">
            <Header userProfile={userProfile} isLoggedIn={isLoggedIn} />
            <div className="app-content">
                {/* Conditionally render the Sidebar based on isLoggedIn */}
                {isLoggedIn && <Sidebar />}
                <main className="app-main">
                    <div className="app-body">
                        <Suspense fallback={<div>Loading...</div>}>
                            {/* Conditionally render the Outlet or Login based on isLoggedIn */}
                            {isLoggedIn ? <Outlet context={{ userProfile, recommendedEventIds, setRecommendedEventIds }} /> : <LoginPage />}
                        </Suspense>
                    </div>
                </main>
            </div>
        </div>
    );
}