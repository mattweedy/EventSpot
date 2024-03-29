// import React from 'react';
import React from 'react';
import { SidebarData } from './SidebarData';
import { NavLink } from 'react-router-dom';

function Sidebar({ recommendedEventIds }) {
    return (
        <div className="sidebar">
            <ul className="sidebar-list">
                {SidebarData.map((val, key) => {
                    if (val.link === '/recommended-events' && (!recommendedEventIds || recommendedEventIds.length === 0)) {
                        return null;
                    }
                    return (
                        <NavLink to={val.link} key={key} className={({ isActive }) => isActive ? 'active' : ''}>
                            <li className="row">
                                <div id="icon">{val.icon}</div>
                                <div id="title">{val.title}</div>
                            </li>
                        </NavLink>
                    )
                })}
            </ul>
        </div>
    )
}

export default Sidebar;