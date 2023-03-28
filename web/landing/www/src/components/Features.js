import React from 'react';

const Feature = ({ title, text, imageUrl }) => {
  return (
    <div className="flex items-center mb-16" id="features">
      <div className="w-1/2">
        <h3 className="text-3xl font-bold mb-4">{title}</h3>
        <p>{text}</p>
      </div>
      <div className="w-1/2">
        <img 
          className="w-full" 
          src={imageUrl} 
          alt={`Image demonstrating ${title}`}
        />
      </div>
    </div>
  );
};

const Features = () => {
  return (
    <section id="features">
      <div className="container mx-auto px-4 my-16">
        <Feature 
          title="Feature 1" 
          text="This is a description of your feature. It should be short and to the point." 
          imageUrl="path/to/image1.jpg"
        />
        <Feature 
          title="Feature 2" 
          text="This is another description of your feature. It should be short and to the point." 
          imageUrl="path/to/image2.jpg"
        />
        <Feature 
          title="Feature 3" 
          text="This is yet another description of your feature. It should be short and to the point." 
          imageUrl="path/to/image3.jpg"
        />
      </div>
    </section>
  );
};

export default Features;
