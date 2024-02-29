import '../style/TopBar.css';
import Chatbox from './Chatbox';


function TopBar(props) {
    function toggleChat() {
        var x = document.getElementById("chat-popup");
        if (x.style.display === "none") {
          x.style.display = "block";
        } else {
          x.style.display = "none";
        }
    }
    return (
        <>
            <div className="row">
                <div class="topbar">
                    <ul>
                        <li className="page-title">{props.pageTitle}</li>
                        <button onClick={toggleChat} id="chatbox-button" className="fa-solid fa-comments"></button>
                        <button id="notification-button" className="fa-solid fa-bell"></button>
                    </ul>
                </div>

            </div>

            <Chatbox />



        </>
    );
}


export default TopBar;