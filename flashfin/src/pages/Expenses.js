import { Link } from 'react-router-dom';

/* components */
import TopBar from '../components/TopBar';
import TransactionsTable from '../components/TransactionsTable';
import ViewBalance from '../components/ViewBalance';

function Expenses() {
    document.title = 'Account';

    return (
        <>
            <TopBar pageTitle="Account" />

            <div className="row">
                <ViewBalance balance="1,000,000" accountTitle="Available Balance" />

                <Link className="card card-link"><i className='fa-solid fa-scroll' />View/Edit Budget</Link>

                <Link className="card card-link"><i className='fa-solid fa-scroll' />Account Settings</Link>
            </div>

            <hr></hr>

            <div className="row">
                <TransactionsTable />
                <div className="card" style={{ flex: "50%" }}>
                    <h2>Budget Goals</h2>
                    <span className='placeholder'>Breakdown visualization of category expenses</span>
                </div>
            </div>
        </>
    );
}

export default Expenses;