import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";

function Layout() {
    return (
        <>

        <Sidebar />

        <div id="main-content"className="main">
            <Outlet />
        </div>
        
        </>
    );

}

export default Layout; 