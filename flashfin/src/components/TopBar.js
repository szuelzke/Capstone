import '../style/TopBar.css';
import '../style/Popup.css';

import React, {useState} from 'react';

const Chatbox = () => {
    return (
        <ul>
            <li>Chat text</li>
            <li>Chat text</li>
            <li>Chat text</li>
            <li>Chat text</li>
        </ul>
    )
}

const PopUp = ({ component: Component }) => {
    return (
        <div className='card pop-up'>
            <h1>Title</h1>
            <Component />
        </div>
    )
};

function TopBar(props) {

    const [ShowChatbox, setShowChatbot] = useState(false);

    function toggleChatbox() {
        setShowChatbot(!ShowChatbox);
    }

    return (
        <>
            <div className="row">
                <div class="topbar">
                    <ul>
                        <li className="page-title">{props.pageTitle}</li>
                        <button onClick={toggleChatbox} className='fa-solid fa-comments' />
                    </ul>
                </div>
            </div>

            {ShowChatbox && (<PopUp component={Chatbox} />)}
            
        </>
    );
}


export default TopBar;