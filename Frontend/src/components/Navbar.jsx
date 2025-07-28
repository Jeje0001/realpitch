import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  function getLinkClass(path) {
    if (location.pathname === path) {
      return "text-black font-semibold";
    } else {
      return "text-gray-500 hover:text-black";
    }
  }

  return (
    <nav className="w-full px-6 py-4 border-b bg-white">
      <div className="flex justify-center">
        <div className="flex gap-10">
          <Link to="/" className={getLinkClass("/")}>
            Home
          </Link>
          <Link to="/create" className={getLinkClass("/create")}>
            Create
          </Link>
        </div>
      </div>
    </nav>
  );
}
