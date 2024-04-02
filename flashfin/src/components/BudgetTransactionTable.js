import '../style/TransactionsTable.css';
import AddTransaction from './forms/AddTransaction';
import ShareTransaction from './forms/ShareTransaction';
import EditTransaction from './forms/EditTransaction';

import React, { useState } from 'react';

function BudgetTransactionTable() {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let month = months[date.getMonth()];

    const maxEntries = 5;


    function TransactionEntry(props) {
        return (
            <>
                <tr>
                    <td>{props.date}</td>
                    <td>{props.title}</td>
                    <td>${props.amount}</td>
                    <td>${props.balanceremain}</td>
                </tr>
            </>
        );
    }

    // insert placeholder transaction
    function placeholderData(Component, count) {
        const instances = [];
        for (let i = 0; i < count; i++) {
            instances.push(<Component date='00/00/0000' title='NULL' amount='999,999,999.000' balanceremain='999,999,999.000' />)
        }
        return instances;
    }

    return (
        <>
            <div className='card'>
                <h3>Transactions</h3>
                <table id="transactions-tbl">
                    <thead>
                        <tr>
                            <th className='tooltip'><i className="fa-regular fa-calendar" /><span className='tooltiptext'>Date</span></th>
                            <th className='tooltip'><i className="fa-solid fa-building-columns" />
                                <span className='tooltiptext'>Description</span> </th>

                            <th className='tooltip'><i className="fa-solid fa-money-bill" /><span className='tooltiptext'>Amount</span></th>
                            <th className='tooltip'><i className="fa-solid fa-money-bill" /><span className='tooltiptext'>Remaining</span></th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        {placeholderData(TransactionEntry, maxEntries)}
                    </tbody>

                </table>
            </div>
        </>
    );
}

export default BudgetTransactionTable;