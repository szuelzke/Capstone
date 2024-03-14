import { Link } from 'react-router-dom';
import { Outlet } from "react-router-dom";

/* components */
import TopBar from '../../components/TopBar';
import ViewBalance from '../../components/ViewBalance';
import Sidebar from '../../components/Sidebar';

function Expenses() {
    document.title = 'Account';
    return (
        <>
            <TopBar pageTitle="Dashboard" />

            <div className="row">
                <ViewBalance balance="1,000,000" accountTitle="Available Balance" />

                <Link to="budget" className="card card-link c-f20"><i className='fa-solid fa-circle-dollar-to-slot' />View/Edit Budget</Link>

                <Link to="transactions" className="card card-link c-f20"><i className='fa-solid fa-file-invoice' />View All Transactions</Link>

                <Link to="share_spend" className="card card-link c-f20"><i className='fa-solid fa-share-nodes' />Shared Expenses</Link>

                <Link to="settings" className="card card-link c-f20"><i className='fa-solid fa-gear' />Account Settings</Link>
            </div>

            <hr></hr>

            <Outlet />

        </>
    );
}

export default Expenses;