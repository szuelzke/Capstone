import '../style/TopBar.css';
import Chatbox from './Chatbox';
import Notifications from './Notifications';

import { Popup, Button } from 'semantic-ui-react';


function TopBar(props) {
    return (
        <>
            <div className="row">
                <div class="topbar">
                    <ul>
                        <li className="page-title">{props.pageTitle}</li>
                        <Popup 
                            trigger={<Button className="fa-solid fa-comments" />}
                            content={<Chatbox />}
                            on='click'
                        />
                        <Popup 
                            trigger={<Button className="fa-solid fa-bell" />}
                            content={<Notifications />}
                            on='click'
                        />

                    </ul>
                </div>

            </div>




        </>
    );
}


export default TopBar;