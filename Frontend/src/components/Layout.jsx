import { Outlet } from "react-router-dom";
import Navbar from './Navbar'

function Layout(){
    return (
        <>
        <Navbar/>
        <div className="min-h-screen bg-white">
            <Outlet />
        </div>
        
        
        </>
    )
}

export default Layout