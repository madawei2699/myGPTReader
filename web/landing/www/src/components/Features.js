import React from "react";
import PropTypes from "prop-types";

const Feature = ({ title, text, videoUrl }) => {
  return (
    <div className="mb-16">
      <div
        style={{
          paddingBottom: "56.25%",
          position: "relative",
          borderRadius: "0.5rem",
          overflow: "hidden",
        }}
      >
        <video
          src={videoUrl}
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            height: "100%",
            width: "100%",
            objectFit: "cover",
            borderRadius: "0.5rem",
          }}
          autoPlay
          loop
          muted
        ></video>
      </div>
      <div className="px-4 py-6 bg-white shadow-md -mt-12 relative z-10">
        <h3 className="text-3xl font-bold mb-4">{title}</h3>
        <p>{text}</p>
      </div>
    </div>
  );
};

Feature.propTypes = {
  title: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  imageUrl: PropTypes.string,
  videoUrl: PropTypes.string,
};

const Features = () => {
  return (
    <section id="features">
      <h2 className="text-4xl mb-4 text-center font-black">
        Features
      </h2>
      <div className="container mx-auto px-4 my-16">
        <div className="flex flex-wrap -mx-4">
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Feature 1"
              text="This is a description of your feature. It should be short and to the point."
              videoUrl="path/to/video1.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Feature 2"
              text="This is another description of your feature. It should be short and to the point."
              videoUrl="path/to/video2.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Feature 3"
              text="This is yet another description of your feature. It should be short and to the point."
              videoUrl="path/to/video3.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Feature 4"
              text="This is a description of your fourth feature. It should be short and to the point."
              videoUrl="path/to/video4.mp4"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;
