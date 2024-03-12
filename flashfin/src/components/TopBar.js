import '../style/TopBar.css';
import '../style/Popup.css';

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
                <div class="topbar">
                    <ul>
                        <li className="page-title">{props.pageTitle}</li>
                        <button class="fa-solid fa-power-off"></button>
                        <button onClick={toggleChatbox} className='fa-solid fa-comments' />
                        <button onClick={toggleNotifications} className='fa-solid fa-bell' />
                    </ul>
                </div>
            </div>

            {ShowChatbox && (<Chatbox />)}
            {ShowNotifications && (<Notifications />)}
            
        </>
    );
}


export default TopBar;