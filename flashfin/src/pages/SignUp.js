import "../style/Login.css"
import { Link } from 'react-router-dom';

function Sign_Up() {
    return (
        <>
            <div className="log-in card">
                <h1>FlashFin</h1>
                <form>
                    <input type="text" name="username" id="username" placeholder="Username" required />
                    <input type="text" name="firstname" id="firstname" placeholder="First Name" required />
                    <input type="text" name="lastname" id="lastname" placeholder="Last Name" required />
                    <input type="text" name="phone" id="phone" placeholder="Phone (optional)" optional />
                    <input type="text" name="email" id="email" placeholder="Email (optional)" optional />
                    <input type="password" name="password" id="password" placeholder="Password" required />
                    <input type="password" name="pasword2" id="password2" placeholder="Verify Password" required />
                    <button>Sign Up</button>

                    <Link to="/sign_in">Sign In?</Link><br />
                    
                </form>

            </div>


        </>
    );

}

export default Sign_Up;