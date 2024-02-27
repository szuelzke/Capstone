function Expenses() {
    return (
        <>
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

            {

            }
        </>
    );
}

export default Expenses;