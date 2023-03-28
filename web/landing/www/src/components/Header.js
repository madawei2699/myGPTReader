import React from "react";
import { Link } from "react-router-dom";
import { FaGithub } from "react-icons/fa";

const Header = () => {
  return (
    <header className="bg-white shadow">
      <div className ="mx-auto container flex justify-between items-center py-4">
        <Link to="/" className="text-gray-800 font-bold text-xl">
          LOGO
        </Link>

        <div className="flex space-x-4">
          <Link
            to="/features"
            className="py-2 px-4 bg-gray-800 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700"
          >
            Features
          </Link>
          <Link
            to="/pricing"
            className="py-2 px-4 bg-gray-800 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700"
          >
            Pricing
          </Link>
          <a
            href="https://github.com/<username>/<repo>"
            target="_blank"
            rel="noreferrer"
            className="pt-2 pl-3 pr-4 border-l-2 border-gray-800 text-gray-600"
          >
            <FaGithub />
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
