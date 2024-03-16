import TopBar from '../components/TopBar.js';
import TransactionsTable from '../components/TransactionsTable';
import ViewBalance from '../components/ViewBalance';

import { Button } from 'semantic-ui-react'

import '../style/Expenses.css';

function Expenses() {
    document.title = 'Account';

    return (
        <>
            <TopBar pageTitle="Account" />

            <div className="row">
                <ViewBalance balance="1,000,000" accountTitle="PNC" />
                <div className="card">
                    <h2>This month's breakdown</h2>
                    <span className="placeholder">Pie chart of current month's income broken down into their categories</span>
                </div>
            </div>

            <div className="row">
                <Button className='card acc-button'>
                    <i className="fa-solid fa-list"></i>
                    <h2>Account Budgeting</h2>
                </Button>

                <Button className='card acc-button'>
                    <i class="fa-solid fa-file"></i>
                    <h2>Spending Report</h2>
                </Button>
                <Button className='card acc-button'>
                    <i class="fa-solid fa-plus"></i>
                    <h2>View Transactions</h2>
                </Button>
            </div>

            <hr></hr>

            <div className="row">
                <TransactionsTable />
                <div className="card" style={{ flex: "33%" }}>
                    <h2>Budget Goals</h2>
                </div>
            </div>
        </>
    );
}

export default Expenses;