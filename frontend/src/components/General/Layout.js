import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "../Sidebar/Sidebar";
import Login from "../Login/Login";
import { Suspense } from "react";

export default function Layout({ userProfile, isLoggedIn, accessToken, isLoading}) {
    return (
        <div className="papp">
            <Header userProfile={userProfile} isLoggedIn={isLoggedIn} />
            <div className="app-content">
                {/* Conditionally render the Sidebar based on isLoggedIn */}
                {isLoggedIn && <Sidebar />}
                <main className="app-main">
                    <div className="app-body">
                        <Suspense fallback={<div>Loading...</div>}>
                            <Outlet context={{ isLoggedIn, userProfile, accessToken }} />
                        </Suspense>
                    </div>
                </main>
            </div>
        </div>
    );

    // console.log({ isLoggedIn, accessToken, userProfile, isLoading });

    // if (isLoggedIn) {
    //     if (accessToken && userProfile && !isLoading) {
    //         return (
    //             <>
    //                 <div className="papp">
    //                     <Header userProfile={userProfile} isLoggedIn={isLoggedIn} />
    //                     <div className="app-content">
    //                         <Sidebar />
    //                         <main className="app-main">
    //                             <div className="app-body">
    //                                 <Suspense fallback={<div>Loading...</div>}>
    //                                     <Outlet />
    //                                 </Suspense>
    //                             </div>
    //                         </main>
    //                     </div>
    //                 </div>
    //             </>
    //         );
    //     }
    // } else {
    //     return (
    //         <div className="app">
    //             <Header isLoggedIn={isLoggedIn} />
    //             <div className="app-content">
    //                 <main className="app-main">
    //                     <Login />
    //                 </main>
    //             </div>
    //         </div>
    //     );
    // }
}