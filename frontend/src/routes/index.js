import React from 'react';
import PathConstants from './pathConstants';

const Home = React.lazy(() => import('../pages/Home'));
const Login = React.lazy(() => import('../pages/LoginPage'));
const Events = React.lazy(() => import('../pages/Events'));
const TopTracks = React.lazy(() => import('../pages/TopTracks'));
const Preferences = React.lazy(() => import('../pages/Preferences'));
const Recommendations = React.lazy(() => import('../pages/Recommendations'));

const routes = [
    { path: PathConstants.HOME, element: <Home /> },
    // { path: PathConstants.HOME, element: Home, requiresAuth: false },
    { path: PathConstants.LOGIN, element: <Login /> },
    { path: PathConstants.EVENTS, element: <Events /> },
    // { path: PathConstants.EVENTS, element: Events, requiresAuth: true},
    { path: PathConstants.TOP_TRACKS, element: <TopTracks />},
    // { path: PathConstants.TOP_TRACKS, element: TopTracks, requiresAuth: true},
    { path: PathConstants.PREFERENCES, element: <Preferences />},
    // { path: PathConstants.PREFERENCES, element: Preferences, requiresAuth: true},
    { path: PathConstants.RECOMMENDED_EVENTS, element: <Recommendations />},
    // { path: PathConstants.RECOMMENDED_EVENTS, element: Recommendations, requiresAuth: true},
];

export default routes;