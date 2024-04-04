import TransactionsTable from "../../components/TransactionsTable";
import PieChart from "../../components/PieChart";
function Dashboard() {
    return (
        <>
        <div className="row">
            <TransactionsTable />
            <div className="card c-f20">
                <PieChart/>
            </div>
            
        </div>
        </>
    )
}

export default Dashboard;