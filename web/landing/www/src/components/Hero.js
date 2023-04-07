import React from "react";
import { umamiEvent } from "../util";
import ProductHuntBadge from "./ProductHuntBadge";

const Hero = () => {
  const joinNow = () => {
    const referrer = document.referrer;
    umamiEvent("JoinNow", { referrer })
    window.location.href = "https://slack-redirect.i365.tech/";
  }
  return (
    <section className="bg-white text-center">
      <div className="container mx-auto py-20">
        <ProductHuntBadge />
        <h1 className="text-5xl mb-6 font-black">myGPTReader</h1>
        <h2 className="text-4xl mb-6 font-black m-4">
          A community-driven way to read and chat with AI bots
        </h2>
        <p className="text-gray-600 leading-normal mb-8 max-w-2xl mx-auto">
          myGPTReader is a bot on Slack that can read and summarize any webpage,
          documents including ebooks, or even videos from YouTube. It can
          communicate with you through voice.
        </p>

        <a
          href='#'
          onClick={joinNow}
          className="py-3 px-6 bg-green-500 text-white font-semibold rounded-full shadow-md hover:bg-green-700 focus:outline-none focus:bg-gray-700"
        >
          Join free now!
        </a>
        <p className="mt-4 italic ml-4 mr-4">Get started in minutes, no credit card required!</p>
        <p className="text-center italic mb-8 text-lg font-bold ml-4 mr-4">
         Join our 4,000+ member community for <span className="text-blue-500">Free</span> and experience all the features now!
        </p>

        <img className="mt-12 mx-auto w-4/5" src="https://camo.githubusercontent.com/b7b1868e5ab7f73ea6473d930c06b05cbb371a189c43dcf7edfbeb30dc67c464/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d6d616461776569323639392f6d7947505452656164657226747970653d44617465" alt="myGPTReader" />
      </div>
    </section>
  );
};

export default Hero;
