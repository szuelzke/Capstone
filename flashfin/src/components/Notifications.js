import '../style/Notifications.css'

function Notifications() {
    return (
        <div className='card pop-up'>
            <div className="notification">
                <div className='timestamp'>
                    11/2/23
                    <i className='fa-regular fa-clock pd-5' />
                </div>
                <li className='title'>[Account] Alert</li>
                <li className='desc'>Your balance is over the threshold by $233.00</li>
            </div>

            <div className="notification">
                <div className='timestamp'>
                    11/2/23
                    <i className='fa-regular fa-clock pd-5' />
                </div>
                <li className='title'>Share request from [user]</li>
                <li className='desc'>You'll owe: $53.53 out of $124.25</li>
                <li><button>Accept</button> <button>Deny</button></li>
            </div>

            <div className="notification">
                <div className='timestamp'>
                    11/2/23
                    <i className='fa-regular fa-clock pd-5' />
                </div>
                <li className='title'>Upcoming payment</li>
                <li className='desc'>Rent is due in 3 days!</li>
            </div>
        </div>
    )

}

export default Notifications;