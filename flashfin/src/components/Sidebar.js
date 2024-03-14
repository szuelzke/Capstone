import '../style/Sidebar.css'
import { Link } from 'react-router-dom';
import picture from '../img/pfp_sample.jpg'

function Sidebar() {
    return (
        <>
            <div id="sidebar" className="sidebar">
                <h1>FlashFin</h1>
                <div className='profile-img'>
                    <img src={picture}></img>
                    <button className='log-out-button'><i className='fa-solid fa-power-off'/>
                    <span>Logout</span></button>

                </div>
                <h2>Firstname Lastname</h2>

                <div className="nav">
                    <Link to="/"><i className="fa-solid fa-house pd-5"></i>Homepage</Link>
                    <Link to="user-settings"><i className="fa-solid fa-gear pd-5"></i>Settings</Link>
                </div>

                <div className="nav">
                    <h2>Personal</h2>
                    <Link to="/">
                        <i className="fa-solid fa-credit-card pd-5"></i>
                        PNC
                    </Link>
                    <h2>Student</h2>
                    <Link to="/">
                        <i className="fa-solid fa-id-card pd-5"></i>
                        FlashCash
                    </Link>
                    <Link to="/">
                        <i className="fa-solid fa-wallet pd-5"></i>
                        Declining Balance
                    </Link>
                </div>
            </div>
        </>
    );
}

export default Sidebar;
