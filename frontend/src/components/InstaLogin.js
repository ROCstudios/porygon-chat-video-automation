import React from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import config from "../config";
import StepsIndicator from "./StepsIndicator";
import NavBar from "./NavBar";
import ErrorAlert from "./ErrorAlert";
const InstaLogin = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [code, setCode] = useState("");

  const handleTokenSend = async () => {

    const response = await axios.post(`${config.backendUrl}/instaauth`, {
      code: code
    });
    if (response.status === 200) {
      navigate("/poster")
    } else {
      setError("Failed to save auth token");
    }
  }

  return (
    <div>
      <NavBar />
      { error && <ErrorAlert message={error} /> }
      <StepsIndicator currentStep={2} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Add IG Token</h1>
            <p className="py-6">
              We'll need you to visit your app dashboard and select the "instagram api auth" option.  Once you've done that, paste the code below.
            </p>
            <input type="text" placeholder="Paste your code here" className="input input-bordered input-primary w-full max-w-xl" onChange={(e) => setCode(e.target.value)} />
            <button className="btn btn-primary mt-4 w-full" onClick={handleTokenSend} >Add Token</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InstaLogin;
