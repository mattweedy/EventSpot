import React from "react";
import { FaHome, FaCalendarAlt, FaMusic, FaCog, FaStar } from 'react-icons/fa';
import PathConstants from "../../routes/pathConstants";

export const SidebarData = [
    {
        title: "Home",
        icon: <FaHome />,
        // link: "/",
        link: PathConstants.HOME,
    },
    {
        title: "Recommended Events",
        icon: <FaStar />,
        // link: "/recommended-events",
        link: PathConstants.RECOMMENDED_EVENTS,
    },
    {
        title: "Top Tracks",
        icon: <FaMusic />,
        // link: "/top-tracks",
        link: PathConstants.TOP_TRACKS,
    },
    {
        title: "Browse All Events",
        icon: <FaCalendarAlt />,
        // link: "/events",
        link: PathConstants.EVENTS,
    },
    {
        title: "Edit Preferences",
        icon: <FaCog />,
        // link: "/preferences",
        link: PathConstants.PREFERENCES,
    },
]