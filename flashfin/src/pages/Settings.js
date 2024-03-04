import TopBar from '../components/TopBar';
import '../style/Settings.css'

function Settings() {
    document.title = 'Account Settings';

    return (
        <>
            <TopBar pageTitle='Settings' />
            <div className='row'>
                <div id="my-profile-info" className='card'>
                    <h2>My Profile</h2>
                    <img src="../public/pfp_sample.jpg" />
                    <ul>
                        <li><i className='fa-solid fa-user' />Firstname Lastname</li>
                        <li><i className='fa-solid fa-envelope' />Email</li>
                        <li><i className='fa-solid fa-phone' />Phone Number</li>
                        <li><i className='fa-solid fa-calendar' />Date Account Created</li>
                    </ul>
                </div>
                <div className="card">
                    <h2>Accounts</h2>
                    <p>TODO: List accounts connected to user. Should also be able to delete/disconnect accounts</p>
                </div>

            </div>

            <h2 className='row row-title'>Edit My Profile</h2>
            <div className='row'>
                <div className='card'>
                    <form className="form-change-info">
                    <h2>Upload Profile Picture</h2>
                        <input type="file" />
                        <input type="submit" />
                    </form>
                </div>
                <div className='card'>
                    <form className="form-change-info">
                    <h2>New Name</h2>
                        <input type="input" placeholder="first name" required />
                        <input type="input" placeholder="last name" required />
                        <input type="submit" />
                    </form>
                </div>
                <div className='card'>
                    <form className="form-change-info">
                    <h2>Change Password</h2>
                        <input type="password" placeholder="current password" required />
                        <input type="password" placeholder="new password" required />
                        <input type="submit" />
                    </form>
                </div>
            </div>
        </>
    );
}

export default Settings;