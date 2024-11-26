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
  const [turns, setTurns] = useState(5);
  const [jsonConvos, setJsonConvos] = useState([]);

  const convoSelected = async (convo) => {
    setLoading(true);
    const response = await axios.post(`${config.backendUrl}/set/convo`, {
      convo: convo
    });
    if (response.status === 200) {
      navigate('/avatar');
    } else {
      setError("Error: " + response.data.error);
    }
    setLoading(false);
  }

  const handleGenerate = async () => {
    setError(null);
    if (topic === "" || turns === 0) {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      setJsonConvos([]);

      try {
        // Make three sequential API calls
        const response1 = await axios.post(`${config.backendUrl}/generate/convo`, {
          topic: topic,
          turns: turns,
        });
        if (response1.status === 200) {
          setJsonConvos(prevConvos => [...prevConvos, response1.data]);
        }

        const response2 = await axios.post(`${config.backendUrl}/generate/convo`, {
          topic: topic,
          turns: turns,
        });
        if (response2.status === 200) {
          setJsonConvos(prevConvos => [...prevConvos, response2.data]);
        }

        const response3 = await axios.post(`${config.backendUrl}/generate/convo`, {
          topic: topic,
          turns: turns,
        });
        if (response3.status === 200) {
          setJsonConvos(prevConvos => [...prevConvos, response3.data]);
        }
        setLoading(false);
      } catch (error) {
        console.error('Error generating content:', error);
        setError("Error: " + error.response.data.error);
      } 
    }
  };

  return (
    <div>
      <NavBar />
      <StepsIndicator currentStep={1} />
      {error && <ErrorAlert message={error} />}
      <div className="hero bg-base-200 min-h-screen -mt-16">
        {
          jsonConvos.length >= 3 && loading === false ? (
            <div className="flex flex-col justify-center items-center">
              <div className="label">
                <span className="label-text text-lg font-bold">Just click on the conversation you want to go with!</span>
              </div>
              <div className="hero-content text-center grid grid-cols-3 gap-4">
                <div className="col-span-1">
                  <div className="flex flex-col gap-2 card bg-base-100 w-96 shadow-xl px-4 py-8 mx-aut aspect-[9/16]" onClick={() => convoSelected(jsonConvos[0])}>
                    {jsonConvos[0].map((convo, index) => (
                      <div key={index} className={`chat ${convo.speaker === "Person 1" ? "chat-end" : "chat-start"}`}>
                        <div className="chat-footer">
                          <time className="text-xs opacity-50 ml-1">{convo.timestamp}</time>
                        </div>
                        <div className={`chat-bubble ${convo.speaker === "Person 1" ? "chat-bubble-primary" : "chat-bubble-success"}`}>
                          {convo.message}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="col-span-1">
                  <div className="flex flex-col gap-2 card bg-base-100 w-96 shadow-xl px-4 py-8 mx-auto aspect-[9/16]" onClick={() => convoSelected(jsonConvos[1])}>
                    {jsonConvos[1].map((convo, index) => (
                      <div key={index} className={`chat ${convo.speaker === "Person 1" ? "chat-end" : "chat-start"}`}>
                        <div className="chat-footer">
                          <time className="text-xs opacity-50 ml-1">{convo.timestamp}</time>
                        </div>
                        <div className={`chat-bubble ${convo.speaker === "Person 1" ? "chat-bubble-secondary" : "chat-bubble-info"}`}>
                          {convo.message}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="col-span-1">
                  <div className="flex flex-col gap-2 card bg-base-100 w-96 shadow-xl px-4 py-8 mx-auto aspect-[9/16]" onClick={() => convoSelected(jsonConvos[2])}>
                    {jsonConvos[2].map((convo, index) => (
                      <div key={index} className={`chat ${convo.speaker === "Person 1" ? "chat-end" : "chat-start"}`}>
                        <div className="chat-footer">
                          <time className="text-xs opacity-50 ml-1">{convo.timestamp}</time>
                        </div>
                        <div className={`chat-bubble ${convo.speaker === "Person 1" ? "chat-bubble-accent" : "chat-bubble-error"}`}>
                          {convo.message}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <button className="btn btn-primary w-full max-w-lg mt-4" onClick={() => { setJsonConvos([]) }}>Reset</button>
            </div>
          ) : (
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
                  <input type="range" min={0} max="25" value={turns} className="range mt-4" onChange={(e) => setTurns(e.target.value)} />
                  <p className="font-bold">Number of turns: {turns}</p>
                  <button className="btn btn-primary w-full max-w-lg mt-4" onClick={handleGenerate}>Generate!</button>
                </div>
              )}
            </div>
          )
        }
      </div>
    </div>
  );
};

export default Conversation;
