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
  const [selectedAvatarIndex, setSelectedAvatarIndex] = useState(-1);

  const simpleAvatarName = [
    "icons8-circled-user-female-skin-type-1-and-2-96.png",
    "icons8-circled-user-female-skin-type-1-and-2-96.png",
    "icons8-circled-user-female-skin-type-5-96.png",
    "icons8-circled-user-female-skin-type-6-96.png",
    "icons8-circled-user-female-skin-type-6-96.png",
    "icons8-circled-user-male-skin-type-1-and-2-96.png",
    "icons8-circled-user-male-skin-type-3-96.png",
    "icons8-circled-user-male-skin-type-5-96.png",
    "icons8-circled-user-male-skin-type-6-96.png",
    "icons8-male-user-96.png",
  ]

  const avatars = [
    require("../assets/icons8-circled-user-female-skin-type-1-and-2-96.png"),
    require("../assets/icons8-circled-user-female-skin-type-1-and-2-96.png"),
    require("../assets/icons8-circled-user-female-skin-type-5-96.png"),
    require("../assets/icons8-circled-user-female-skin-type-6-96.png"),
    require("../assets/icons8-circled-user-female-skin-type-6-96.png"),
    require("../assets/icons8-circled-user-male-skin-type-1-and-2-96.png"),
    require("../assets/icons8-circled-user-male-skin-type-3-96.png"),
    require("../assets/icons8-circled-user-male-skin-type-5-96.png"),
    require("../assets/icons8-circled-user-male-skin-type-6-96.png"),
    require("../assets/icons8-male-user-96.png"),
  ];

  const saveAvatar = async () => {
    setError(null);
    if (name === "" || selectedAvatarIndex === -1) {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/set/avatar`, {
          avatar: simpleAvatarName[selectedAvatarIndex],
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
                  <span className="label-text">Name that appears in your header</span>
                </div>
                <input
                  type="text"
                  placeholder="Type the name here..."
                  className="input input-bordered input-md w-full max-w-lg"
                  onChange={(e) => setName(e.target.value)}
                />
              </label>
              <div className="grid grid-cols-5 gap-4 mt-4">
                {avatars.slice(0, 10).map((avatar, index) => (
                  <div className="avatar" key={index} onClick={() => setSelectedAvatarIndex(index)}>
                    <div className={`w-24 rounded-full ${selectedAvatarIndex === index ? 'ring ring-secondary ring-offset-base-100 ring-offset-2' : ''}`}>
                      <img src={avatar} />
                    </div>
                  </div>
                ))}
              </div>
              <button className="btn btn-primary w-full max-w-lg mt-4" onClick={saveAvatar}>Create Avatar!</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Avatar;
