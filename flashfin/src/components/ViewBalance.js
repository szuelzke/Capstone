import '../style/ViewBalance.css'

function ViewBalance(props) {
    return (
        <>
            <div className="card view-balance">
                <div className="acc-balance hide-text">
                    ${props.balance}
                </div>
                <h2 className="acc-title">{props.accountTitle}</h2>
            </div>
        </>
    );
}

export default ViewBalance;