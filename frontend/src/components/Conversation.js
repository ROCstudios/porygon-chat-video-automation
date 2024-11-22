import React from "react";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";
import StepsIndicator from "./StepsIndicator";
import NavBar from "./NavBar";
import ErrorAlert from "./ErrorAlert";

const Conversation = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [topic, setTopic] = useState("");
  const [caption, setCaption] = useState("");
  const [turns, setTurns] = useState(5);
  const [convoImages, setConvoImages] = useState([]);

  const convoSelected = (convo) => {
    // backend call to save the convo
    navigate('/avatar');
  }

  const handleGenerate = async () => {
    setError(null);
    if (topic === "" || turns === 0 || turns > 10) {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/generate/convo`, {
          topic: topic,
          turns: turns,
        });
        console.log('🚀 ~ file: Dashboard.js:34 ~ handleGenerate ~ response:', response.data);

        if (response.data.status === 'success') {
          // setConvoImages(response.data.convo_images);
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
      <StepsIndicator currentStep={3} />
      { error && <ErrorAlert message={error} /> }
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-full">
              <p className="text-xl">Please wait...</p>
              <span className="loading loading-dots loading-lg"></span>
            </div>
          ) : (
            <div className="max-w-lg">
              <h1 className="text-5xl font-bold">Let's Get This Chat Started! 🎉</h1>
            <p className="py-6">
            </p>
            <label>
              <div className="label">
                <span className="label-text">Topic of the conversation that AI will generate</span>
              </div>
              <textarea
                placeholder="Type your chat here..."
                className="textarea textarea-bordered textarea-lg w-full max-w-lg"
                onChange={(e) => setTopic(e.target.value)}
                >
              </textarea>
            </label>
            <div className="label">
                <span className="label-text">Number of chat bubbles</span>
              </div>
            <input type="range" min={0} max="10" value={turns} className="range mt-4" onChange={(e) => setTurns(e.target.value)} />
            <p className="font-bold">Number of turns: {turns}</p> 
            <button className="btn btn-primary w-full max-w-lg mt-4" onClick={handleGenerate}>Generate!</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Conversation;
