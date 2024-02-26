import '../style/Sidebar.css';

function Sidebar() {
    return (
        <>
            <div id="sidebar" className="sidebar">
                <div className="user-profile">
                    <h1>FlashFin</h1>
                    <img src="{{ url_for('static', filename='pfp_sample.jpg') }}"></img>
                    <h2>Firstname Lastname</h2>
                </div>
                <div class="nav">
                    <a href="/"><i className="fa-solid fa-house"></i>Dashboard</a>
                    <a href="/"><i className="fa-solid fa-share-nodes"></i>Shared Spending</a>
                    <a href="/"><i className="fa-solid fa-gear"></i>Settings</a>
                </div>
                <div className="qb">
                    <h2>My Accounts <i className="fa-solid fa-caret-down"></i></h2>
                    <div className="qb-account">
                        <h2><a href="#">PNC</a></h2>
                        <div className="qb-balance hide-text">$1,000,000</div>
                    </div>
                    <div className="qb-account">
                        <h2><a href="#">FlashCard</a></h2>
                        <div className="qb-balance hide-text">$1,000,000</div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Sidebar;
