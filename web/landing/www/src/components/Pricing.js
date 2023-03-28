import React from "react";

const Pricing = () => {
  return (
    <section id="pricing">
      <h2 className="text-5xl mb-4 text-center font-black">Choose Your Plan</h2>
      <div className="pricing px-4">
        <div className="pricing__item free">
          <h2 className="font-extrabold">Free</h2>
          <p className="price font-normal">$0/m</p>
          <ul className="benefits">
            <li>Benefit 1</li>
            <li>Benefit 2</li>
            <li>Benefit 3</li>
          </ul>
          <button className="cta bg-slate-800 font-semibold">
            Get Started
          </button>
        </div>
        <div className="pricing__item premium">
          <h2 className="font-extrabold">Premium</h2>
          <p className="price font-normal">$5/m</p>
          <ul className="benefits">
            <li>Benefit 1</li>
            <li>Benefit 2</li>
            <li>Benefit 3</li>
            <li>Advanced Feature 1</li>
            <li>Advanced Feature 2</li>
          </ul>
          <button className="cta bg-gray-800 font-semibold">Get Started</button>
        </div>
      </div>
    </section>
  );
};

export default Pricing;
