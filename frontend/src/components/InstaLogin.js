import React from "react";
import axios from "axios";
import { igSaveToken, igSetToken, getRefreshToken, igSaveRefreshToken } from "../util/TokenService";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import config from "../config";

const InstaLogin = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [code, setCode] = useState("");

  const handleTokenSend = async () => {

    const response = await axios.post(`${config.backendUrl}/instaauth`, {
      code: code
    });
    if (response.status === 200) {
      navigate("/dashboard")
    } else {
      setError("Failed to save auth token");
    }
  }

  return (
    <div>
      <div className="navbar bg-base-100">
        <div className="navbar-start">
          <div className="dropdown">
            <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h7" />
              </svg>
            </div>
            <ul
              tabIndex={0}
              className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
              <li><a href="/">Login</a></li>
              <li><a href="/instaauth">Instagram Auth</a></li>
              <li><a href="/redirect">Callback Handler</a></li>
              <li><a href="/dashboard">Dashboard</a></li>
            </ul>
          </div>
        </div>
        <div className="navbar-center">
          <a className="btn btn-ghost text-xl">AI Content Generator</a>
        </div>
        <div className="navbar-end">
        </div>
      </div>
      {error && <div role="alert" className="alert alert-error">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 shrink-0 stroke-current"
            fill="none"
            viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{error}</span>
        </div>
      }
      <div className="flex justify-center bg-base-200 p-4">
        <ul className="steps">
          <li className="step">TikTok Auth</li>
          <li className="step step-secondary">Instagram Auth</li>
          <li className="step">Generate!</li>
        </ul>
      </div>
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
