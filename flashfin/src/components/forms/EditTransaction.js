function EditTransaction(props) {
    return (
        <>
            <div className='dimmer'>
                <h2>Edit Transaction</h2>
                <div className='row card'>
                    <button className='card-x-button fa-solid fa-x' onClick={props.toggle}></button>
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

}

export default EditTransaction