import React, { useState } from "react";

const FAQ = () => {
  const faqList = [
    { question: "Question 1", answer: "Answer 1" },
    { question: "Question 2", answer: "Answer 2" },
    { question: "Question 3", answer: "Answer 3" }
  ];

  const [showAnswer, setShowAnswer] = useState("");

  const handleQuestionClick = (answer) => {
    if (showAnswer === answer) {
      setShowAnswer("");
    } else {
      setShowAnswer(answer);
    }
  };

  return (
    <section className="bg-white py-10 px-5">
      <h2 className="text-4xl mb-4 text-center font-black">Questions & Answers</h2>
      <div className="container mx-auto max-w-lg">
      <ul>
        {faqList.map((item, index) => (
          <li key={index} className="mb-6">
            <div
              onClick={() => handleQuestionClick(item.answer)}
              className="rounded-lg shadow-md bg-white p-5 cursor-pointer transition-all duration-300 hover:bg-gray-50"
            >
              <p className="text-xl font-medium">{item.question}</p>
              {showAnswer === item.answer && (
                <p className="mt-4">{item.answer}</p>
              )}
            </div>
          </li>
        ))}
      </ul>
      </div>
    </section>
  );
};

export default FAQ;
