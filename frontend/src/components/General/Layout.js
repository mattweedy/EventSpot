import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "../Sidebar/Sidebar";
import LoginPage from "../../pages/LoginPage";
import { Suspense } from "react";
import { Toaster } from "react-hot-toast";
import Loading from "./Loading";


export default function Layout({ userProfile, isLoggedIn, recommendedEventIds, setRecommendedEventIds, isLoading }) {
    return (
        <div className="papp">
            <Header userProfile={userProfile} isLoggedIn={isLoggedIn} />

            <div className="app-content">
                {/* Conditionally render the Sidebar based on isLoggedIn */}
                {isLoggedIn && <Sidebar recommendedEventIds={recommendedEventIds}/>}
                <main className="app-main">
                        <Suspense fallback={<Loading />}>
                            {/* Conditionally render the Outlet or Login based on isLoggedIn */}
                            {isLoading ? <Loading /> : isLoggedIn ? <Outlet context={{ userProfile, recommendedEventIds, setRecommendedEventIds }} /> : <LoginPage />}
                            <Toaster position="bottom-right" containerStyle={{ color: '#fff' }}/>
                        </Suspense>
                </main>
            </div>
        </div>
    );
}