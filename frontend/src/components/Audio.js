import React from "react";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import StepsIndicator from "./StepsIndicator";
import NavBar from "./NavBar";
import config from "../config";
import ErrorAlert from "./ErrorAlert";

const Audio = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [audio, setAudio] = useState(null);

  const handleGenerate = async () => {
    setError(null);
    if (audio === null) {
      setError("Please upload an audio file");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/set/audio`, {
          audio: audio,
        });
        console.log('🚀 ~ file: Dashboard.js:34 ~ handleGenerate ~ response:', response.data);

        if (response.data.status === 'success') {
          navigate('/dashboard');
        }
      } catch (error) {
        console.error('Error generating content:', error);
        setError("Error: " + error.response.data.error);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <NavBar />
      { error && <ErrorAlert message={error} /> }
      <StepsIndicator currentStep={5} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-full">
              <p className="text-xl">Please wait...</p>
              <span className="loading loading-dots loading-lg"></span>
            </div>
          ) : (
            <div className="max-w-lg">
              <h1 className="text-5xl font-bold">Upload your tunes</h1>
            <p className="py-6">
            </p>
            <label className="flex flex-col items-center px-4 py-6 bg-white text-blue rounded-lg shadow-lg tracking-wide uppercase border border-blue cursor-pointer hover:bg-blue hover:text-white transition duration-300 ease-in-out">
              <svg className="w-8 h-8" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
              </svg>
              <span className="mt-2 text-base leading-normal">Select an audio file</span>
              <input type='file' className="hidden" accept="audio/*" onChange={(e) => setAudio(e.target.files[0])} />
            </label>
            <button className="btn btn-primary w-full max-w-lg mt-4" onClick={handleGenerate}>Generate!</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Audio;