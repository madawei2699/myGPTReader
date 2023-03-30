import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"; // import fontawesome icon library
import { faGithub } from "@fortawesome/free-brands-svg-icons"; // import github icon

const Footer = () => {
  return (
    <footer className="bg-white px-4 md:px-20 mx-auto">
      <div className="container flex justify-between items-center py-3 lg:px-20">
        <p>©2023 i365.tech All rights reserved.</p>
        <a
          href="https://github.com/madawei2699/myGPTReader"
        >
          <FontAwesomeIcon icon={faGithub} />
        </a>
      </div>
    </footer>
  );
};

export default Footer;
