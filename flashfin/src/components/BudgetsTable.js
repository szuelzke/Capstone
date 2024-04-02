import '../style/TransactionsTable.css';
import CreateBudget from './forms/CreateBudget';
import EditBudget from './forms/EditBudget';
import ViewBudget from './ViewBudget';


import React, { useState } from 'react';

function BudgetsTable() {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const date = new Date();
    let month = months[date.getMonth()];

    const maxEntries = 25;

    // add new budget form
    const [ShowBudget, setShowBudget] = useState(false);
    // edit budget form
    const [ShowEditBudget, setShowEditBudget] = useState(false);

    // view budget
    const [ShowViewBudget, setShowViewBudget] = useState(false);

    function toggleShowBudget() {
        setShowBudget(!ShowBudget);
    }

    function toggleShowEdit() {
        setShowEditBudget(!ShowEditBudget);
    }

    function toggleShowView() {
        setShowViewBudget(!ShowViewBudget);
    }

    function BudgetEntry(props) {
        return (
            <>
                <tr>
                    <td>{props.title}</td>
                    <td>{props.account}</td>
                    <td>{props.category}</td>
                    <td>{props.startdate}</td>
                    <td>{props.enddate}</td>
                    <td>${props.amount}</td>
                    <td>${props.remaining}</td>
                    <td className="sharespend-button">
                        <button onClick={toggleShowView}><i class="fa-solid fa-pen-to-square" /> View</button>
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
            instances.push(<Component title='NULL' account='ACCOUNT' category='CATEGORY' startdate='00/00/0000' enddate='00/00/0000' amount='999,999,999.000' remaining='999,999,999.000' />)
        }
        return instances;
    }

    return (
        <>
            <div className='card'>
            <h2>Budget</h2>
                <button onClick={toggleShowBudget} className='transtbl-nav tooltip'>
                    <i className='fa-solid fa-plus pd-5' />
                    <span className='tooltiptext'>Create Budget</span>
                </button>

                <table id="transactions-tbl">
                    <thead>
                        <tr>
                            <th className='tooltip'><i className="fa-solid fa-building-columns" />
                                <span className='tooltiptext'>Title</span> </th>
                            <th className='tooltip'><i className="fa-solid fa-tags" /><span className='tooltiptext'>Account</span></th>
                            <th className='tooltip'><i className="fa-solid fa-tags" /><span className='tooltiptext'>Category</span></th>
                            <th className='tooltip'><i className="fa-regular fa-calendar" /><span className='tooltiptext'>Start Date</span></th>
                            <th className='tooltip'><i className="fa-regular fa-calendar" /><span className='tooltiptext'>End Date</span></th>
                            <th className='tooltip'><i className="fa-solid fa-money-bill" /><span className='tooltiptext'>Amount</span></th>
                            <th className='tooltip'><i className="fa-solid fa-money-bill" /><span className='tooltiptext'>Remaining</span></th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        {placeholderData(BudgetEntry, maxEntries)}
                    </tbody>

                </table>
            </div>

            {ShowBudget && <CreateBudget toggle={toggleShowBudget} />}
            {ShowEditBudget && <EditBudget toggle={toggleShowEdit} />}
            {ShowViewBudget && <ViewBudget toggle={toggleShowView} />}
        </>
    );
}

export default BudgetsTable;