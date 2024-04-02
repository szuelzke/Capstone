import { Link } from 'react-router-dom';

function AmountOwed(props) {
    return (
        <>

            <div className="card no-bg amount-owed">
                    <h1>${props.balance}</h1>
                    <h2>{props.accountTitle}</h2>
            </div>
        </>
    );
}

export default AmountOwed;