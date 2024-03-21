import React from 'react';
import { SidebarData } from './SidebarData';
import Logout from '../Login/Logout';

function Sidebar() {
    return (
        <div className="sidebar">
            <ul className="sidebar-list">
                {SidebarData.map((val, key) => {
                    return (
                        <li key={key}
                            className="row"
                            id={window.location.pathname === val.link ? "active" : ""}
                            onClick={() => {
                                window.location.pathname = val.link;
                            }}
                        >
                            <div id="icon">{val.icon}</div>
                            <div id="title">{val.title}</div>
                        </li>
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