import '../style/Chatbox.css';

function Chatbox() {
    return (
        <>
            <div id="chat-popup" className="topbar-popup chatbox">
                <div className="message-history">
                    <p className="bot-text">
                        <i className="fa-solid fa-robot bot-icon" />
                        How can I help you?
                    </p>
                    <p className="user-text">
                        <i className="fa-solid fa-user user-icon" />
                        I'd like to know more about this topic
                    </p>
                </div>
                <div className="type-in">
                    <form>
                        <input type="submit" />
                        <input type="text" placeholder="Say something..." />
                    </form>
                    
                </div>
            </div>
        </>
    );
}

export default Chatbox;