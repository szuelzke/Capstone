import '../style/Sidebar.css';
import { Link } from 'react-router-dom';
import QuickBalance from './QuickBalance';

function Sidebar() {
    return (
        <>
            <div id="sidebar" className="sidebar">
                <div className="user-profile">
                    <h1>FlashFin</h1>
                    <img src="../public/pfp_sample.jpg"></img>
                    <h2>Firstname Lastname</h2>
                </div>
                <div class="nav">
                    <Link to="/"><i className="fa-solid fa-house"></i>Dashboard</Link>
                    <Link to="share_spend"><i className="fa-solid fa-share-nodes"></i>Shared Spending</Link>
                    <Link to="settings"><i className="fa-solid fa-gear"></i>Settings</Link>
                </div>
                <div className="qb">
                    <h2>My Accounts <i className="fa-solid fa-caret-down"></i></h2>

                    <QuickBalance accName="PNC" accBalance="1000"/>

                    <QuickBalance accName="Flashcard" accBalance="20,000"/>

                </div>
            </div>
        </>
    );
}

export default Sidebar;
