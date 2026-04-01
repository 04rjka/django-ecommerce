import React from 'react'
import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import logo from "../assets/vite.svg"

export default function MainNavbar() {
    const [isOpen,setIsOpen] = useState(false)
        
  return (
    <nav className="sticky top-0 relative shadow-lg flex justify-between items-center bg-linear-to-r from-purple-800 to-purple-500 mx-auto h-20 p-1">
        <div className="p-2 rounded-md flex items-center gap-2">
            <div className=" text-xl rounded-md  text-center max-w-12 object-cover overflow-hidden shrink-0"><img src={logo} alt="logo"/>
            </div>
            <p className="font-semibold text-white">ECOM</p>
        </div>
        <ul id="nav-items"
            className={`${isOpen? 'flex' : 'hidden'} text-center flex-col absolute top-20 right-0 left-0 bg-slate-400 p-2 md:bg-transparent md:static md:flex md:flex-row gap-2`}>
            <li className="border p-2 border-white rounded-md md:rounded-2xl font-semibold text-white bg-blue-300 md:bg-transparent hover:bg-white hover:text-black cursor-pointer">
                <NavLink to={"/"}>Home</NavLink></li>
            <li className="border p-2 border-white rounded-md md:rounded-2xl font-semibold text-white bg-blue-300 hover:bg-white md:bg-transparent hover:text-black cursor-pointer">About</li>
            <li className="border p-2 border-white rounded-md md:rounded-2xl font-semibold text-white bg-blue-300 hover:bg-white md:bg-transparent hover:text-black cursor-pointer">Contact Us</li>
        </ul>
        <div className="m-2">
            <button className="hidden md:block bg-white p-2 rounded-md">Login</button>
        </div>
        <div className=" md:hidden m-2">
            <button onClick={()=> setIsOpen(!isOpen)} id="menu-btn" className=" p-2 text-lg rounded-md bg-purple-600 text-white shadow-lg/20 w-10">{isOpen? "X" : "☰"}</button>
        </div>
    </nav>
  )
}
