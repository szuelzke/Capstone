import { Link } from 'react-router-dom';

function Home() {
    return (
        <>
            <div className="card">
                <h1>Dashboard</h1>
                <h2>Pages available: </h2>
                <Link to="expenses">Expenses</Link><br />
                <Link to="share_spend">Shared Spending</Link><br />
                <Link to="settings">Settings</Link><br />
                <Link to="sign_in">Sign In / Log In</Link><br />
            </div>
        </>

    );
}

export default Home;