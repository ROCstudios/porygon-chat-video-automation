import React from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import config from "../config";
import StepsIndicator from "./StepsIndicator";
import NavBar from "./NavBar";
import ErrorAlert from "./ErrorAlert";
const Login = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const handleLogin = async () => {

    // TODO We need to have seperate conditional logic for the Instagram token logic.
    // Instagram can be automated but we'll need  a more explicit approach since TikTok expires quickly
    // Research their docs.

    const response = await axios.get(`${config.backendUrl}/tiktokauth`);
    const authUrl = response.data.url;
    if (response.status === 200) {
      window.location.href = authUrl; 
    } else {
      setError("Failed to get authentication URL");
    }
  };

  return (
    <div>
      <NavBar />
      { error && <ErrorAlert message={error} /> }
      <StepsIndicator currentStep={1} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Login</h1>
            <p className="py-6">
              Let's get you generating your content!  We'll redirect you to get your instagram token after you verify your account and then we'll send you to the main page.  If you've already verified your account, just click the button below.
            </p>
            <button className="btn btn-primary mt-4 w-full" onClick={handleLogin}>Access Generator!</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
