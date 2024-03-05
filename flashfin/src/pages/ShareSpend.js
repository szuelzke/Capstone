import TopBar from '../components/TopBar';

function ShareSpend() {
    return (
        
        <>
        <TopBar pageTitle="Shared Spending" />
        <div className='row'>
            <div className='card'>
                Amount Owed To Others
            </div>
            <div className='card'>
                Amount Others Owe You
            </div>
        </div>
        <div className='row'>
            <div className='card'>
                List of all of user's shared transactions (ongoing and paid)
            </div>
        </div>
        </>

    );
}

export default ShareSpend;