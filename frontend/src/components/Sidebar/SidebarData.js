import React from "react";
// import { FaHome, FaCalendarAlt, FaMusic, FaCog, FaStar } from 'react-icons/fa';
import { FaHome, FaCalendarAlt, FaCog, FaStar } from 'react-icons/fa';
import PathConstants from "../../routes/pathConstants";

export const SidebarData = [
    {
        title: "Home",
        icon: <FaHome />,
        link: PathConstants.HOME,
    },
    {
        title: "Browse All Events",
        icon: <FaCalendarAlt />,
        link: PathConstants.EVENTS,
    },
    {
        title: "Edit Preferences",
        icon: <FaCog />,
        link: PathConstants.PREFERENCES,
    },
    {
        title: "Recommended Events",
        icon: <FaStar />,
        link: PathConstants.RECOMMENDED_EVENTS,
    },
    // {
    //     title: "Top Tracks",
    //     icon: <FaMusic />,
    //     link: PathConstants.TOP_TRACKS,
    // },
]