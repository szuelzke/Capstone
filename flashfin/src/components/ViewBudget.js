import BudgetTransactionTable from "./BudgetTransactionTable";
import BudgetAmount from './BudgetAmount';
import BudgetAmountRemaining from './BudgetAmountRemaining';

function EditBudget(props) {
    return (
        <>
            <div className='dimmer'>
            <div className='card card-budget'>
                <button className='card-x-button fa-solid fa-x' onClick={props.toggle}></button>    
                <div style={{ width: '50%', float: 'left' }}>
                    <div className='card card-budget'>
                        <div className="row">
                            <div className= 'card'>Budget Title: Account, Category...</div>
                        </div>
                        <div className="row">
                                <div className='card'>
                                    <BudgetAmount balance="1,000,000" accountTitle="Budget Amount" />
                                    <BudgetAmountRemaining balance="1,000,000" accountTitle="Amount Remaining" />
                                </div>
                        </div>
                        <div className="row">
                            <BudgetTransactionTable />
                        </div>
                    </div>
                </div>

                <div style= {{ width: '50%', float: 'right' }}>
                    <div className="row">
                        <div className= 'card'>4 days Remaining!</div>
                    </div>
                    <div className="row">
                        <div className= 'card'>visualization...</div>
                    </div>
                </div>
            </div>
            </div>
        </>
    )

}

export default EditBudget