import "../style/Login.css"
import { useState } from 'react';
import { Link } from 'react-router-dom';


function Sign_In() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent default form submission behavior

        // Make HTTP POST request to Flask backend
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                // Handle successful login (e.g., redirect user to dashboard)
                console.log('Login successful');
            } else {
                // Handle failed login (e.g., display error message)
                console.error('Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <>
            <div className="log-in card">
                <h1>FlashFin</h1>
                <form onSubmit={handleSubmit}>
                    <input type="text" name="username" id="username" placeholder="Username" required value={username} onChange={(event) => setUsername(event.target.value)} />
                    <input type="password" name="username" id="password" placeholder="Password" required value={password} onChange={(event) => setPassword(event.target.value)} />
                    <button type="submit">Log In</button>


                    <input type="checkbox" name="rememberuser" id="rememberuser" />
                    <label htmlfor="rememberuser">Remember Me</label><br />

                    <a href="">Forgot Password?</a><br />
                    <Link to="/sign_up">New User?</Link><br />

                </form>

            </div>


        </>
    );

}

export default Sign_In;