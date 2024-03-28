function ShareTransaction(props) {
    return (
        <>
            <div className="dimmer">
                <h2>Share A Transaction</h2>
                <div className="row card">
                    <button className='card-x-button fa-solid fa-x' onClick={props.toggle}></button>
                    <p>Show transaction details
                        <hr></hr>
                    </p>
                    <form className="form-deco">
                        <input
                            type="text"
                            placeholder="Receiver ID"
                            required />
                        <input
                            type="number"
                            min="0"
                            placeholder="Receiver Amount"
                            // max="[value of total]"
                            required />
                        <input
                            type="submit" />
                    </form>

                </div>
            </div>
        </>
    )

}

export default ShareTransaction;