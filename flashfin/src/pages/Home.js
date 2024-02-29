import { Link } from 'react-router-dom';
import ViewBalance from '../components/ViewBalance';
import TopBar from '../components/TopBar';

function Home() {
    return (
        <>
        <TopBar pageTitle="Dashboard"/>
        <div className="row">

            <ViewBalance balance="1,000,000" accountTitle="PNC"/>

            <ViewBalance balance="1,000,000" accountTitle="FlashCash"/>

            <ViewBalance balance="1,000,000" accountTitle="Declining Balance"/>

        </div>
            <div className="row">
                <div className="card">
                    <h1>Dashboard</h1>
                    <h2>Pages available: </h2>
                    <Link to="expenses">Expenses</Link><br />
                    <Link to="share_spend">Shared Spending</Link><br />
                    <Link to="settings">Settings</Link><br />
                    <Link to="sign_in">Sign In / Log In</Link><br />
                </div>
            </div>
        </>

    );
}

export default Home;