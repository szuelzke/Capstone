import '../style/TopBar.css';
import '../style/Popup.css';

import { Link } from 'react-router-dom';
import React, {useState} from 'react';
import Chatbox from './Chatbox';
import Notifications from './Notifications';

function TopBar(props) {

    const [ShowChatbox, setShowChatbot] = useState(false);
    const [ShowNotifications, setShowNotifications] = useState(false);

    function toggleChatbox() {
        if (ShowNotifications) {
            toggleNotifications();
        }
        setShowChatbot(!ShowChatbox);
    }

    function toggleNotifications() {
        if (ShowChatbox) {
            toggleChatbox();
        }
        setShowNotifications(!ShowNotifications);
    }

    return (
        <>
            <div className="row">
                <div className="topbar">
                    <ul>
                        <Link to="."><li className="page-title">{props.pageTitle}</li></Link>
                        <button className='fa-solid fa-power-off'/>
                        <button onClick={toggleChatbox} className='fa-solid fa-comments' />
                        <button onClick={toggleNotifications} className='fa-solid fa-bell' />
                    </ul>
                </div>
            </div>

            {ShowChatbox && (<Chatbox toggle={toggleChatbox}/>)}
            {ShowNotifications && (<Notifications />)}
            
        </>
    );
}


export default TopBar;