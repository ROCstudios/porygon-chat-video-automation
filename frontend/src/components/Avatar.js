import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";
import NavBar from "./NavBar";
import StepsIndicator from "./StepsIndicator";
import ErrorAlert from "./ErrorAlert";

const Avatar = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [name, setName] = useState("");
  const [generatedAvatar, setGeneratedAvatar] = useState("");

  useEffect(() => {
    generateAvatars();
  }, []);

  const generateAvatars = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${config.backendUrl}/generate/image`);
      if (response.status === 200) {
        setGeneratedAvatar(response.data.image_url);
      }
    } catch (error) {
      console.error('Error generating avatars:', error);
    } finally {
      setLoading(false);
    }
  }

  const saveAvatar = async () => {
    setError(null);
    if (name === "" || generatedAvatar === "") {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/set/avatar`, {
          avatar: generatedAvatar,
          name: name
        });
          
        if (response.status === 200) {
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
      <NavBar index={2} />
      {error && <ErrorAlert message={error} />}
      <StepsIndicator currentStep={2} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          <div className="max-w-lg">
            <h1 className="text-5xl font-bold">Who are you?</h1>
            <p className="py-6">
            </p>
            <label>
              <div className="label">
                <span className="label-text">Name that appears in your header</span>
              </div>
              <input
                type="text"
                placeholder="Type the name here..."
                className="input input-bordered input-md w-full max-w-lg"
                onChange={(e) => setName(e.target.value)}
              />
            </label>
            {loading ? (
              <div className="flex flex-col justify-center items-center h-full mt-4">
                <p className="text-xl">Getting avatars. Please wait...</p>
                <span className="loading loading-dots loading-lg"></span>
              </div>
            ) : (
              <div className="flex flex-col justify-center items-center h-full mt-4">
                <div className="w-[120px] h-[120px] rounded-full">
                  <img src={generatedAvatar} alt="Generated avatar" />
                </div>
              </div>
            )}
            <button className="btn btn-primary w-full max-w-lg mt-4" onClick={saveAvatar}>Continue with this avatar</button>
            <button className="btn btn-link w-full max-w-lg mt-2 text-[#0000EE]" onClick={generateAvatars}>Get a new avatar</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Avatar;
