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
        <h2 className="text-4xl mb-6 font-black">
          A new way to read with AI bot
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
          Join Now
        </a>
        <p className="mt-4 italic text-gray-400">with more than 4000+ members to experience all these features for free.</p>
        <img className="mt-12 mx-auto w-4/5" src="/hero.jpg" alt="Hero" />
      </div>
    </section>
  );
};

export default Hero;
