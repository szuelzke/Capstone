import '../style/TransactionsTable.css';
import AddTransaction from './forms/AddTransaction';
import EditTransaction from './forms/EditTransaction';

import React, { useState } from 'react';

function SharedTransactionsTable() {
    const date = new Date();

    const maxEntries = 25;

    // add new transaction form
    const [ShowTransaction, setShowTransaction] = useState(false);
    // edit transaction form
    const [ShowEditTransaction, setShowEditTransaction] = useState(false);

    function toggleShowTransactions() {
        setShowTransaction(!ShowTransaction);
    }

    function toggleShowEdit() {
        setShowEditTransaction(!ShowEditTransaction);
    }

    function TransactionEntry(props) {
        return (
            <>
                <tr>
                    <td>{props.date}</td>
                    <td>{props.title}</td>
                    <td>{props.category}</td>
                    <td>{props.sender}</td>
                    <td>{props.receiver}</td>
                    <td>${props.amount_split}</td>
                    <td>{props.is_paid}</td>
                    <td className="sharespend-button">
                        <button onClick={toggleShowEdit}><i class="fa-solid fa-pen-to-square" /> Edit</button>
                        <button><i className="fa-solid fa-trash" /> Delete</button> 
                    </td>
                </tr>
            </>
        );
    }

    // insert placeholder transaction
    function placeholderData(Component, count) {
        const instances = [];
        for (let i = 0; i < count; i++) {
            instances.push(<Component date='00/00/0000' title='NULL' category = 'CATEGORY' sender = 'sender' receiver = 'receiver' amount_split ='999.99' is_paid ='TRUE' />)
        }
        return instances;
    }

    return (
        <>
            <div className='card'>
                <h2>Shared Transactions</h2>

                <table id="transactions-tbl">
                    <thead>
                        <tr>
                            <th className='tooltip'><i className="fa-regular fa-calendar" /><span className='tooltiptext'>Date</span></th>
                            <th className='tooltip'><i className="fa-solid fa-building-columns" />
                                <span className='tooltiptext'>Description</span> </th>

                            <th className='tooltip'><i className="fa-solid fa-tags" /><span className='tooltiptext'>Category</span></th>
                            <th>Sender</th>
                            <th>Receiver</th>
                            <th>Amount Split</th>
                            <th>Is Paid?</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        {placeholderData(TransactionEntry, maxEntries)}
                    </tbody>

                </table>
            </div>

            {ShowTransaction && <AddTransaction toggle={toggleShowTransactions} />}
            {ShowEditTransaction && <EditTransaction toggle={toggleShowEdit} />}
        </>
    );
}

export default SharedTransactionsTable;