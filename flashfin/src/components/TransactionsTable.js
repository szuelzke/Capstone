import '../style/TransactionsTable.css'
import TransactionEntry from './TransactionEntry';

function TransactionsTable() {
    return (
        <>
            <div className="card">
                <h2>Transactions</h2>
                <table id="transactions-tbl">
                    <tr>
                        <th><i class="fa-regular fa-calendar" /></th>
                        <th><i class="fa-solid fa-building-columns" /></th>
                        <th><i class="fa-solid fa-money-bill" /></th>
                        <th><i class="fa-solid fa-money-bill" /></th>
                        <th><i class="fa-solid fa-tags" /></th>
                    </tr>

                    <TransactionEntry date="2/1" title="Apartment Complex" amount="1,000" balanceremain="161.80" category="Rent" />

                    <TransactionEntry date="1/29" title="Netflix" amount="20.99" balanceremain="1,161.8" category="Subscription" />

                    <TransactionEntry date="1/28" title="BP" amount="54.75" balanceremain="1,182.79" category="Subscription" />

                </table>
            </div>
        </>
    );
}

export default TransactionsTable;