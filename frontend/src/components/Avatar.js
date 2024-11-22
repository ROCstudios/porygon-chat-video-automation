import React from "react";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";
import NavBar from "./NavBar";
import StepsIndicator from "./StepsIndicator";
import ErrorAlert from "./ErrorAlert";

const Avatar = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [name, setName] = useState("");
  const [avatar, setAvatar] = useState("");

  const saveAvatar = async () => {
    setError(null);
    if (name === "" || avatar === "") {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/save/avatar`, {
          avatar: avatar,
          name: name
        });

        if (response.data.status === 'success') {
          navigate('/audio');
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
      <StepsIndicator currentStep={4} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-full">
              <p className="text-xl">Please wait...</p>
              <span className="loading loading-dots loading-lg"></span>
            </div>
          ) : (
            <div className="max-w-lg">
              <h1 className="text-5xl font-bold">Who are you?</h1>
              <p className="py-6">

              </p>
              <label>
                <div className="label">
                  <span className="label-text">Name that appears above the chat bubbles</span>
                </div>
                <input
                  type="text"
                  placeholder="Type the name here..."
                  className="input input-bordered input-md w-full max-w-lg"
                  onChange={(e) => setName(e.target.value)}
                />
              </label>
              <button className="btn btn-primary w-full max-w-lg mt-4" onClick={saveAvatar}>Generate!</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Avatar;
