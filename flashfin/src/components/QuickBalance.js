function QuickBalance(props) {
    return (
        <>
        <div className="qb-account">
            <h2><a href="#">{props.accName}</a></h2>
            <div className="qb-balance hide-text">${props.accBalance}</div>
        </div>
        </>

    );

}

export default QuickBalance;