import '../style/TransactionsTable.css';
import AddTransaction from './forms/AddTransaction';
import ShareTransaction from './forms/ShareTransaction';
import EditTransaction from './forms/EditTransaction';

import React, { useState } from 'react';

function TransactionsTable() {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let month = months[date.getMonth()];

    const maxEntries = 25;

    // add new transaction form
    const [ShowTransaction, setShowTransaction] = useState(false);
    // edit transaction form
    const [ShowEditTransaction, setShowEditTransaction] = useState(false);
    // share transaction form
    const [ShowShareTransaction, setShowShareTransaction] = useState(false);

    function toggleShowTransactions() {
        setShowTransaction(!ShowTransaction);
    }

    function toggleShowEdit() {
        setShowEditTransaction(!ShowEditTransaction);
    }

    function toggleShowShare() {
        setShowShareTransaction(!ShowShareTransaction);
    }

    function TransactionEntry(props) {
        return (
            <>
                <tr>
                    <td>{props.date}</td>
                    <td>{props.title}</td>
                    <td>${props.amount}</td>
                    <td>${props.balanceremain}</td>
                    <td>{props.category}</td>
                    <td className="sharespend-button">
                        <button onClick={toggleShowEdit}><i class="fa-solid fa-pen-to-square" /> Edit</button>
                        <button><i className="fa-solid fa-trash" /> Delete</button> 
                        <button onClick={toggleShowShare}><i className="fa-solid fa-share" /> Share</button>   
                    </td>
                </tr>
            </>
        );
    }

    // insert placeholder transaction
    function placeholderData(Component, count) {
        const instances = [];
        for (let i = 0; i < count; i++) {
            instances.push(<Component date='00/00/0000' title='NULL' amount='999,999,999.000' balanceremain='999,999,999.000' category='CATEGORY' />)
        }
        return instances;
    }

    return (
        <>
            <div className='card'>
                <h2>{month}'s Transactions</h2>
                <button onClick={toggleShowTransactions} className='transtbl-nav tooltip'>
                    <i className='fa-solid fa-plus pd-5' />
                    <span className='tooltiptext'>Add Transaction</span>
                </button>

                <table id="transactions-tbl">
                    <thead>
                        <tr>
                            <th className='tooltip'><i className="fa-regular fa-calendar" /><span className='tooltiptext'>Date</span></th>
                            <th className='tooltip'><i className="fa-solid fa-building-columns" />
                                <span className='tooltiptext'>Description</span> </th>

                            <th className='tooltip'><i className="fa-solid fa-money-bill" /><span className='tooltiptext'>Amount</span></th>
                            <th>Balance</th>
                            <th className='tooltip'><i className="fa-solid fa-tags" /><span className='tooltiptext'>Category</span></th>
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
            {ShowShareTransaction && <ShareTransaction toggle={toggleShowShare} />}
        </>
    );
}

export default TransactionsTable;