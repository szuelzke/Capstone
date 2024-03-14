import TopBar from '../components/TopBar';
import '../style/UserSettings.css'

function UserSettings() {
    document.title = 'Account Settings';

    return (
        <>
            <TopBar pageTitle='Settings' />
            <div className='row'>
                <div className='card'>
                    <h2>My Profile</h2>
                    <img src="" alt='pfp'/>
                    <ul>
                        <li><i className='fa-solid fa-user pd-5' />Firstname Lastname</li>
                        <li><i className='fa-solid fa-envelope pd-5' />Email</li>
                        <li><i className='fa-solid fa-phone pd-5' />Phone Number</li>
                        <li><i className='fa-solid fa-calendar pd-5' />Date Account Created</li>
                    </ul>
                </div>
                <div className="card connected-acc">
                    <h2>Accounts</h2>
                    <div>
                        <h3>ACCOUNT NAME</h3>
                        <button>Edit</button>
                        <button>Delete</button>
                    </div>
                    <div>
                        <h3>ACCOUNT NAME</h3>
                        <button>Edit</button>
                        <button>Delete</button>
                    </div>
                    <div>
                        <h3>ACCOUNT NAME</h3>
                        <button>Edit</button>
                        <button>Delete</button>
                    </div>
                    <div>
                        <h3>ACCOUNT NAME</h3>
                        <button>Edit</button>
                        <button>Delete</button>
                    </div>
                </div>

            </div>

            <h2 className='row row-title'>Edit My Profile</h2>
            <div className='row'>
                <div className='card'>
                    <h2>Upload Profile Picture</h2>
                    <form className="form-deco">
                        <input type="file" />
                        <input type="submit" />
                    </form>
                </div>
                <div className='card'>
                    <h2>Social Name</h2>
                    <form className="form-deco">
                        <input type="input" placeholder="first name" required />
                        <input type="password" placeholder="current password" required />
                        <input type="submit" />
                    </form>
                </div>
                <div className='card'>
                    <h2>Change Password</h2>
                    <form className="form-deco">
                        <input type="password" placeholder="current password" required />
                        <input type="password" placeholder="new password" required />
                        <input type="submit" />
                    </form>
                </div>
            </div>
        </>
    );
}

export default UserSettings;