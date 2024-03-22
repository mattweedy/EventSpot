import React from 'react';
import { SidebarData } from './SidebarData';
import Logout from '../Login/Logout';
import { NavLink } from 'react-router-dom';

function Sidebar() {
    return (
        <div className="sidebar">
            <ul className="sidebar-list">
                {SidebarData.map((val, key) => {
                    return (
                        <NavLink to={val.link}
                            activeClassName="active"
                            key={key}
                        >
                            <li className="row">
                                <div id="icon">{val.icon}</div>
                                <div id="title">{val.title}</div>
                            </li>
                        </NavLink>
                    )
                })}
                <li className="row">
                    <Logout />
                </li>
            </ul>
        </div>
    )
}

export default Sidebar;