import { BrowserRouter, Routes, Route } from "react-router-dom";

import './style/Main.css';
import './style/Card.css';

import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Home from './pages/Home'
import UserSettings from "./pages/UserSettings";

import ShareSpend from "./pages/expenses/ShareSpend";

/* Templates */
import Layout from "./pages/Layout";
import Expenses from './pages/expenses/Expenses'

/* Expense Account Pages */
import Budget from "./pages/expenses/Budget";
import Transactions from "./pages/expenses/Transactions";
import AccountSettings from "./pages/expenses/AccountSettings";

import Dashboard from "./pages/expenses/Dashboard";

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Layout />}>
                        <Route index element={<Home />} />
                        <Route path="user-settings" element={<UserSettings />} />
                        <Route path="account" element={<Expenses />}>
                            <Route index element={<Dashboard />} />
                            <Route path="budget" element={<Budget />} />
                            <Route path="transactions" element={<Transactions />} />
                            <Route path="share_spend" element={<ShareSpend />} />
                            <Route path="settings" element={<AccountSettings />} />
                        </Route>
                    </Route>
                    <Route path="sign_in" element={<SignIn />} />
                    <Route path="sign_up" element={<SignUp />} />
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;