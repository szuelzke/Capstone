import TransactionsTable from "../../components/TransactionsTable";

function Dashboard() {
    return (
        <>
        <div className="row">
            <TransactionsTable />
            <div className="card c-f20">Current month category breakdown</div>
        </div>
        </>
    )
}

export default Dashboard;