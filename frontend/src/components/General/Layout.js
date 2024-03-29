import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "../Sidebar/Sidebar";
import LoginPage from "../../pages/LoginPage";
import { Suspense } from "react";
import { Toaster } from "react-hot-toast";

// ? this isLoading part is making the sidebar disappear too for some reason

export default function Layout({ userProfile, isLoggedIn, recommendedEventIds, setRecommendedEventIds, isLoading }) {
    return (
        <div className="papp">
            <Header userProfile={userProfile} isLoggedIn={isLoggedIn} />

            <div className="app-content">
                {/* Conditionally render the Sidebar based on isLoggedIn */}
                {isLoggedIn && <Sidebar recommendedEventIds={recommendedEventIds}/>}
                <main className="app-main">
                    {/* <div className="app-body"> */}
                        <Suspense fallback={<h2>Loading...</h2>}>
                            {/* Conditionally render the Outlet or Login based on isLoggedIn */}
                            {isLoading ? <h2>Loading...</h2> : isLoggedIn ? <Outlet context={{ userProfile, recommendedEventIds, setRecommendedEventIds }} /> : <LoginPage />}
                            <Toaster position="bottom-right" containerStyle={{ color: '#fff'}}/>
                        </Suspense>
                    {/* </div> */}
                </main>
            </div>
        </div>
    );
}