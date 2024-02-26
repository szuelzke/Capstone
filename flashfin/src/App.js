import { BrowserRouter, Routes, Route } from "react-router-dom";

import './style/Main.css';

import Home from './pages/Home'
import Expenses from './pages/Expenses'
import Sign_In from "./pages/Sign_In";
import ShareSpend from "./pages/ShareSpend";
import Settings from "./pages/Settings";
import Layout from "./pages/Layout";

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Layout />}>
                        <Route index element={<Home />} />
                        <Route path="expenses" element={<Expenses />} />
                        <Route path="share_spend" element={<ShareSpend />} />
                        <Route path="settings" element={<Settings />} />
                    </Route>
                    <Route path="sign_in" element={<Sign_In />} />
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;