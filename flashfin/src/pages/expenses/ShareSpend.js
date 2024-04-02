import TopBar from '../../components/TopBar';
import SharedTransactionsTable from "../../components/sharedtransaction";
import AmountOwed from '../../components/AmountOwed';
import AmountDue from '../../components/AmountDue';


function ShareSpend() {
    return (
        
        <>
        <div className="row">
            <div className="row-title">
                <h2>Shared Expenses</h2>
            </div>
        </div>
        <div className='row'>           
            <div className='card'>
                <AmountOwed balance="1,000,000" accountTitle="Amount Owed To Others" />
            </div>
            <div className='card'>
                <AmountDue balance="1,000,000" accountTitle="Amount Others Owe You" />
            </div>
        </div>
        <div className="row">
            <SharedTransactionsTable />
        </div>
        </>

    );
}

export default ShareSpend;