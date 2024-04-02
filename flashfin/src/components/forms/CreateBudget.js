function CreateBudget(props) {
    return (
        <>
            <div className='dimmer'>
                <h2>Create Budget</h2>
                <div className='row card'>
                    <button className='card-x-button fa-solid fa-x' onClick={props.toggle}></button>
                    <form className='form-deco'>
                        <input
                            type='text'
                            placeholder='Title'
                            required />
                        <input
                            type='date'
                            placeholder='Start Date'
                            required />
                        <input
                            type='date'
                            placeholder='End Date'
                            required />
                        <input
                            type='number'
                            min='0'
                            placeholder='Amount'
                            required />
                        <select>
                            <option name='account'>Account</option>
                            <option name='account'>Account</option>
                            <option name='account'>Account</option>
                        </select>
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

}

export default CreateBudget