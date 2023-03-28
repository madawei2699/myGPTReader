import React from "react";

const Hero = () => {
  return (
    <section className="bg-gray-100">
      <div className="container mx-auto flex items-center justify-between py-20">
        <div className="flex-1">
          <h1 className="font-bold text-3xl md:text-5xl leading-tight mb-4">
            The Best Productivity App In The Market
          </h1>
          <p className="text-gray-600 leading-normal mb-8">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus
            cursus vehicula mattis.
          </p>
          <a
            href="#slack-channel"
            className="py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:bg-gray-700"
          >
            Join our Slack channel!
          </a>
        </div>
        <img
          className="w-1/2"
          src="https://images.unsplash.com/photo-1475274118587-6c9475b27252"
          alt="Hero"
        />
      </div>
    </section>
  );
};

export default Hero;
