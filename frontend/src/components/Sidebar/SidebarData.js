import React from "react";
import { FaHome, FaCalendarAlt, FaMusic, FaCog, FaStar } from 'react-icons/fa';

export const SidebarData = [
    {
        title: "Home",
        icon: <FaHome />,
        link: "/home",
    },
    {
        title: "Recommended Events",
        icon: <FaStar />,
        link: "/recommended-events",
    },
    {
        title: "Top Tracks",
        icon: <FaMusic />,
        link: "/top-tracks",
    },
    {
        title: "Browse All Events",
        icon: <FaCalendarAlt />,
        link: "/events",
    },
    {
        title: "Edit Preferences",
        icon: <FaCog />,
        link: "/preferences",
    },
]