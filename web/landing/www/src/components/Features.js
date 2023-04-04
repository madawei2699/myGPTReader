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
          playsInline
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
              title="Web read with myGPTReader"
              text="Use myGPTReader to quickly read and understand any web content through conversations, even videos (currently only YouTube videos with subtitles are supported)."
              videoUrl="https://img.bmpi.dev/myGPTReader/1-ffmpeg.mp4"
            />
            <Feature
              title="Web read with myGPTReader (YouTube)"
              text="Use myGPTReader to quickly read and understand any web content through conversations, even videos (currently only YouTube videos with subtitles are supported)."
              videoUrl="https://img.bmpi.dev/myGPTReader/2-ffmpeg.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Document read with myGPTReader"
              text="Use myGPTReader to quickly read the content of any file, supporting eBooks, PDF, DOCX, TXT, and Markdown."
              videoUrl="https://img.bmpi.dev/myGPTReader/3-ffmpeg.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Voice chat with myGPTReader"
              text="Practice your foreign language by speaking with your voice to myGPTReader, which can be your personal tutor and supports Chinese, English, German, and Japanese."
              videoUrl="https://img.bmpi.dev/myGPTReader/4-ffmpeg.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Ask myGPTReader anything"
              text="A large number of prompt templates are built in, use them for better conversations with chatGPT."
              videoUrl="https://img.bmpi.dev/myGPTReader/5-ffmpeg.mp4"
            />
          </div>
          <div className="w-full mx-auto lg:w-4/5 px-4 mb-8">
            <Feature
              title="Hot News Today"
              text="Every day myGPTReader sends out the latest hot news and automatically generates a summary, so you can quickly learn what's hot today."
              videoUrl="https://img.bmpi.dev/my-gpt-reader-hot-news-show-1.mp4"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;
