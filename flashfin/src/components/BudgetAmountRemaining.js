import { Link } from 'react-router-dom';

function BudgetAmountRemaining(props) {
    return (
        <>

            <div className="card no-bg amount-owed">
                    <h1>${props.balance}</h1>
                    <h1>{props.accountTitle}</h1>
            </div>
        </>
    );
}

export default BudgetAmountRemaining;