import { Link } from 'react-router-dom';

function ViewBalance(props) {
    return (
        <>

            <div className="card no-bg view-balance">
                <Link to=".">
                    <h1 className="hide-text">${props.balance}</h1>
                    <h2>{props.accountTitle}</h2>
                </Link>
            </div>
        </>
    );
}

export default ViewBalance;