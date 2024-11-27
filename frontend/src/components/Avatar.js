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
  const [selectedAvatar, setSelectedAvatar] = useState("");

  const [generatedAvatars, setGeneratedAvatars] = useState([]);

  useEffect(() => {
    generateAvatars();
  }, []);

  const generateAvatars = async () => {
    if (generatedAvatars.length >= 3) {
      return;
    }
    setLoading(true);
    setGeneratedAvatars([]);
    try {
      const response = await axios.get(`${config.backendUrl}/generate/image`);
      if (response.status === 200) {
        setGeneratedAvatars(prevAvatars => [...prevAvatars, response.data.image_url]);
      }

      const response2 = await axios.get(`${config.backendUrl}/generate/image`);
      if (response2.status === 200) {
        setGeneratedAvatars(prevAvatars => [...prevAvatars, response2.data.image_url]);
      }   

      const response3 = await axios.get(`${config.backendUrl}/generate/image`);
      if (response3.status === 200) {
        setGeneratedAvatars(prevAvatars => [...prevAvatars, response3.data.image_url]);
      }
    } catch (error) {
      console.error('Error generating avatars:', error);
    } finally {
      setLoading(false);
    }
  }

  const saveAvatar = async () => {
    setError(null);
    if (name === "" || selectedAvatar === "") {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/set/avatar`, {
          avatar: selectedAvatar,
          name: name
        });
        console.log('🚀 ~ file: Avatar.js:42 ~ saveAvatar ~ response:', response);
        
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
      <NavBar />
      { error && <ErrorAlert message={error} /> }
      <StepsIndicator currentStep={2} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          {loading && generatedAvatars.length < 3 ? (
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
                  <span className="label-text">Name that appears in your header</span>
                </div>
                <input
                  type="text"
                  placeholder="Type the name here..."
                  className="input input-bordered input-md w-full max-w-lg"
                  onChange={(e) => setName(e.target.value)}
                />
              </label>
              <div className="grid grid-cols-3 gap-4 mt-4">
                {generatedAvatars.map((imageUrl, index) => (
                  <div className="avatar" key={index} onClick={() => setSelectedAvatar(imageUrl)}>
                    <div className={`w-[120px] h-[120px] rounded-full ${selectedAvatar === imageUrl ? 'ring ring-secondary ring-offset-base-100 ring-offset-2' : ''}`}>
                      <img src={imageUrl} alt={`Generated avatar ${index + 1}`} />
                    </div>
                  </div>
                ))}
              </div>
              <button className="btn btn-primary w-full max-w-lg mt-4" onClick={saveAvatar}>Create Avatar!</button>
              <button className="btn btn-link w-full max-w-lg mt-2" onClick={generateAvatars}>Get New Images</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Avatar;
