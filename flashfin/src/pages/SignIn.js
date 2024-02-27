import "../style/Login.css"

function Sign_In() {
    return (
        <>
            <div className="log-in card">
                <h1>FlashFin</h1>
                <form>
                    <input type="text" name="username" id="username" placeholder="Username" required />
                    <input type="password" name="username" id="password" placeholder="Password" required />
                    <button>Log In</button>


                    <input type="checkbox" name="rememberuser" id="rememberuser" />
                    <label for="rememberuser">Remember Me</label>

                    <a href="">Forgot Password?</a>

                </form>

            </div>


        </>
    );

}

export default Sign_In;