import React from 'react';
import { SidebarData } from './SidebarData';
import Logout from '../Login/Logout';
import { Link } from 'react-router-dom';
import PathConstants from '../../routes/pathConstants';


function Sidebar() {
    return (
        <div className="sidebar">
            <ul className="sidebar-list">
                {SidebarData.map((val, key) => {
                    return (
                        <Link to={val.link}>
                            <li key={key}
                                className="row"
                                // id={window.location.pathname === val.link ? "active" : ""}
                                // onClick={() => {
                                    // window.location.pathname = val.link;
                                // }}
                            >
                                    <div id="icon">{val.icon}</div>
                                    <div id="title">{val.title}</div>
                            </li>
                        </Link>
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