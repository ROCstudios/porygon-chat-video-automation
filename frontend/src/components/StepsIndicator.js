import React from 'react';

const StepsIndicator = ({ currentStep }) => {
  const steps = ['', '', '', ''];
  
  return (
    <div className="flex justify-center p-4">
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
