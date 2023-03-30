import React from "react";
import { Link } from "react-router-dom";
import { umamiEvent, gtagEvent } from "../util";

const Header = () => {
  const scrollToFeatures = () => {
    document.getElementById("features").scrollIntoView({
      block: "start",
      behavior: "smooth",
    });
  };

  const scrollToPricing = () => {
    document.getElementById("pricing").scrollIntoView({
      block: "start",
      behavior: "smooth",
    });
  };

  const goToGitHub = () => {
    const referrer = document.referrer;
    umamiEvent("GitHubFromMenu", { referrer })
    gtagEvent("GitHubFromMenu")
    window.location.href = "https://github.com/madawei2699/myGPTReader";
  }

  return (
    <header className="bg-white shadow">
      <div className="mx-auto container flex justify-between items-center py-4 px-4 md:px-20">
        <Link to="/">
          <img src="/logo.png" alt="LOGO" width="40" height="40" />
        </Link>

        <div className="flex space-x-4">
          <Link
            onClick={scrollToFeatures}
            to="#"
            className="py-2 px-4 bg-gray-800 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700"
          >
            Features
          </Link>
          <Link
            onClick={scrollToPricing}
            to="#"
            className="py-2 px-4 bg-gray-800 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700"
          >
            Pricing
          </Link>
          <a
            href="#"
            onClick={goToGitHub}
            className="github-link ml-4 flex items-center justify-center w-10 h-10 rounded-full bg-gray-800 text-white font-semibold shadow-md hover:bg-gray-700 focus:outline-none focus:bg-gray-700"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              style={{ width: "28px", height: "28px" }} // added this
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 2C6.47 2 2 6.477 2 12c0 4.41 2.865 8.138 6.839 9.465.5.09.682-.217.682-.48s0-.994 0-1.945c-2.789.523-3.369-1.34-3.369-1.34-.454-1.155-1.109-1.464-1.109-1.464-.908-.62.068-.608.068-.608 1.002.074 1.528 1.028 1.528 1.028.89 1.522 2.335 1.084 2.902.829.091-.645.352-1.085.64-1.334-2.245-.252-4.598-1.118-4.598-4.982 0-1.104.393-2.004 1.029-2.71-.105-.253-.447-1.284.097-2.675 0 0 .853-.272 2.788 1.036a9.516 9.516 0 012.454-.333c.833 0 1.67.112 2.454.333 1.935-1.308 2.787-1.036 2.787-1.036.545 1.391.204 2.422.1 2.675.634.706 1.027 1.606 1.027 2.71 0 3.874-2.355 4.727-4.608 4.975.362.312.687.927.687 1.866 0 1.352-.012 2.44-.012 2.773 0 .267.18.574.688.476a10.098 10.098 0 006.445-9.466c0-5.523-4.469-10-10-10z"
              ></path>
            </svg>
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
