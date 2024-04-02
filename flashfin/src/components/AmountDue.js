import { Link } from 'react-router-dom';

function AmountDue(props) {
    return (
        <>

            <div className="card no-bg amount-due">
                    <h1>${props.balance}</h1>
                    <h2>{props.accountTitle}</h2>
            </div>
        </>
    );
}

export default AmountDue;