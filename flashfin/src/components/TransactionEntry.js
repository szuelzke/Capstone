function TransactionEntry(props) {
    return (
        <>
            <tr>
                <td>{props.date}</td>
                <td>{props.title}</td>
                <td>${props.amount}</td>
                <td>${props.balanceremain}</td>
                <td>{props.category}</td>
            </tr>
        </>
    );
}

export default TransactionEntry;