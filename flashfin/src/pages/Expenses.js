import TopBar from '../components/TopBar';
import TransactionsTable from '../components/TransactionsTable';
import '../style/Expenses.css';
import ViewBalance from '../components/ViewBalance';

function Expenses() {
    return (
        <>
            <TopBar pageTitle="Account" />

            <div className="row">
                <div className="card acc-button">
                    <i class="fa-solid fa-plus"></i>
                    <h3>Add a Transaction</h3>
                </div>
                <div className="card acc-button">
                    <i class="fa-solid fa-list"></i>
                    <h3>All Transactions</h3>
                </div>
                <div className="card acc-button">
                    <i class="fa-solid fa-file"></i>
                    <h3>Spending Report</h3>
                </div>
            </div>

            <div className="row">
                <ViewBalance balance="1,000,000" accountTitle="PNC" />
                <div className="card">
                    <h2>This month's breakdown</h2>
                    <span className="placeholder">Pie chart of current month's income broken down into their categories</span>
                </div>
            </div>

            <hr></hr>

            <div className="row">
                <div className="card">
                    <h2>Add a transaction</h2>
                    <form>
                        <input type="date" placeholder="Date" required></input>
                        <input type="number" placeholder="Amount" min="0" required></input>
                        <select id="category" name="Category">
                            <option value="Rent">Rent</option>
                            <option value="Food">Food</option>
                            <option value="Entertainment">Entertainment</option>
                            <option value="Groceries">Groceries</option>
                        </select>
                        <input type="submit"></input>
                    </form>
                </div>
            </div>

            <div className="row">
                <TransactionsTable />
                <div className="card" style={{flex:"33%"}}>
                    <h2>Budget Goals</h2>
                </div>
            </div>

        </>
    );
}

export default Expenses;