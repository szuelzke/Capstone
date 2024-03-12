import '../style/TransactionsTable.css';

import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function TransactionsTable() {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let month = months[date.getMonth()];

    const maxEntries = 25;

    const [ShowTransaction, setShowTransaction] = useState(false);

    function toggleShowTransactions() {
        setShowTransaction(!ShowTransaction);
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
                </tr>
            </>
        );
    }

    function AddForm() {
        return (
            <>
                <div className='dimmer'>
                    <h2>Add Transaction</h2>
                    <div className='row card'>
                        <button className='card-x-button fa-solid fa-x' onClick={toggleShowTransactions}></button>
                        <form className='form-deco'>
                            <input
                                type='date'
                                placeholder='Date'
                                required />
                            <input
                                type='text'
                                placeholder='Title'
                                required />
                            <input
                                type='number'
                                min='0'
                                placeholder='Amount'
                                required />
                            <select>
                                <option name='category'>Category</option>
                                <option name='category'>Category</option>
                                <option name='category'>Category</option>
                                <option name='category'>Category</option>
                            </select>
                            <input type='submit' />
                        </form>
                    </div>
                </div>
            </>
        )
    };

    function placeholderData(Component, count) {
        const instances = [];
        for (let i = 0; i < count; i++) {
            instances.push(<Component date='00/00/0000' title='NULL' amount='999,999,999.000' balanceremain='999,999,999.000' category='CATEGORY' />)
        }
        return instances;
    }

    return (
        <>
            <div className='card c-700'>
                <h2>{month}'s Transactions</h2>
                <button onClick={toggleShowTransactions}>
                    <i className='fa-solid fa-plus pd-5' />
                    Add Transaction
                </button>
                <Link to=''>
                    <i className='fa-solid fa-plus pd-5' />
                    View All Transactions
                </Link>

                <table id="transactions-tbl">
                    <tr>
                        <th><i class="fa-regular fa-calendar" /></th>
                        <th><i class="fa-solid fa-building-columns" /></th>
                        <th><i class="fa-solid fa-money-bill" /></th>
                        <th><i class="fa-solid fa-money-bill" /></th>
                        <th><i class="fa-solid fa-tags" /></th>
                    </tr>

                    {placeholderData(TransactionEntry, maxEntries)}

                </table>
            </div>

            {ShowTransaction &&
                (<AddForm />)}
        </>
    );
}

export default TransactionsTable;