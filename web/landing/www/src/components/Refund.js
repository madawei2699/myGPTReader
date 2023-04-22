import React, { useState } from "react";

const Refund = () => {
  const [showDisclaimer, setShowDisclaimer] = useState(false)
  return (
    <div className='mx-auto max-w-6xl mb-10'>
      <h2 className='text-4xl mb-4 text-center font-black'>Refund Policy</h2>
      <div className="mx-4 sm:mx-32">
      <p>Thank you for choosing myGPTReader! We strive to provide high-quality services to our customers.
         However, if you are not satisfied with our product, we offer a refund policy that ensures your rights as a customer.</p>

      <ul className='list-disc ml-5'>
        <li>You have purchased myGPTReader within the last 30 days.</li>
        <li>You have encountered technical issues or problems with our product that we are unable to resolve within a reasonable time frame.</li>
        <li>You have not violated our terms of service or engaged in fraudulent activity.</li>
      </ul>

      {!showDisclaimer && (
          <button onClick={() => setShowDisclaimer(true)} className='bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 mt-5 rounded cursor-pointer'>Read more</button>
      )}

      {showDisclaimer && (
          <>
              <div className='mt-5'>
                  <h3 className='text-lg font-semibold text-gray-700 mb-3'>Refund process:</h3>
                  <p>To request a refund, please contact us at <span className='text-gray-700'>me@myreader.io</span> within 30 days of your purchase. We may ask you to provide additional information or documentation to support your refund request.</p>
                  <p>Once we receive your refund request, we will review your case and respond within 7 business days. If your refund request is approved, we will issue a refund to the original payment method you used to purchase myGPTReader.</p>
              </div>

              <div className='mt-5'>
                <h3 className='text-lg font-semibold text-gray-700 mb-3'>Limitations:</h3>
                <ul className='list-disc ml-5'>
                    <li>We do not offer refunds for any purchases made outside of our website or authorized resellers.</li>
                    <li>We reserve the right to refuse a refund request if we suspect fraudulent activity or violation of our terms of service.</li>
                    <li>We do not offer refunds for purchases made more than 30 days ago.</li>
                </ul>
              </div>

              <div className='mt-5 text-gray-700'>
                  <p>If you have any questions or concerns regarding our refund policy, please contact us at <span className='text-gray-700'>me@myreader.io</span>.</p>
              </div>
          </>
      )}
      </div>
    </div>
  );
};

export default Refund;
