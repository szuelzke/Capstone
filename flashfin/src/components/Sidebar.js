import '../style/Sidebar.css'
import { Link } from 'react-router-dom';

function Sidebar() {
    return (
        <>
            <div id="sidebar" className="sidebar">
                <div className="user-profile">
                    <h1>FlashFin</h1>
                    <img src="../public/pfp_sample.jpg"></img>
                    <h2>Firstname Lastname</h2>
                </div>
                <div className="nav">
                    <Link to="/"><i className="fa-solid fa-house"></i>Dashboard</Link>
                    <Link to="share_spend"><i className="fa-solid fa-share-nodes"></i>Shared Spending</Link>
                    <Link to="settings"><i className="fa-solid fa-gear"></i>Settings</Link>
                </div>

                <div className="nav">
                    <h2>Personal</h2>
                    <a href=""><i className="fa-solid fa-credit-card"></i>PNC</a>
                    <h2>Student</h2>
                    <a href=""><i className="fa-solid fa-id-card"></i>FlashCash</a>
                    <a href=""><i className="fa-solid fa-wallet"></i>Declining Balance</a>
                </div>
            </div>
        </>
    );
}

export default Sidebar;
