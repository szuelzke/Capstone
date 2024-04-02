import BudgetTransactionTable from "./BudgetTransactionTable";
import BudgetAmount from './BudgetAmount';
import BudgetAmountRemaining from './BudgetAmountRemaining';

function ViewBudget(props) {
    return (
        <>
            <div className='dimmer'>
                <div className='card card-budget'>  
                    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>  
                        <div className="card-row2">
                                    Budget Title 
                                    <br />Account, Category...
                        </div>
                        <div className="card-row2">
                                <div className='card-h3'>4 days Remaining!</div>
                        </div>
                        <div className="card-row2" style={{ display: 'flex' }}>
                            <div className='card'><BudgetAmount balance="1,000,000" accountTitle="Budget Amount" /></div>                           
                            <div className='card'><BudgetAmountRemaining balance="1,000,000" accountTitle="Amount Remaining" /></div>
                        </div>
                        <div className="card-row2">
                            <div className='card' style={{ flex: '1' }}><BudgetTransactionTable /></div>
                        </div>
                    </div>
                    <button className='card-x-button fa-solid fa-x' onClick={props.toggle}></button>
                </div>
            </div>
        </>
    )
    

}

export default ViewBudget