function ViewBalance(props) {
    return (
        <>
            <div className="card no-bg view-balance">
                <div className="">
                    <h1 className="hide-text">${props.balance}</h1>
                    <h2>{props.accountTitle}</h2>
                </div>
            </div>
        </>
    );
}

export default ViewBalance;