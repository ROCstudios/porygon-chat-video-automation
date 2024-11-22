import React from 'react';

const StepsIndicator = ({ currentStep }) => {
  const steps = ['TikTok', 'Instagram', 'Convo', 'Avatar', 'Audio', 'Post'];
  
  return (
    <div className="flex justify-center bg-base-200 p-4">
      <ul className="steps">
        {steps.map((step, index) => (
          <li 
            key={index} 
            className={`step ${index + 1 <= currentStep ? 'step-secondary' : ''}`}
          >
            {step}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StepsIndicator;
