import React from "react";
import axios from "axios";
import { igSaveToken, igSetToken, getRefreshToken, igSaveRefreshToken } from "../util/TokenService";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import config from "../config";

const Login = () => {
  const navigate = useNavigate();
  const [simpleText, setSimpleText] = useState("");

  const handleLogin = async () => {

    // TODO We need to have seperate conditional logic for the Instagram token logic.
    // Instagram can be automated but we'll need  a more explicit approach since TikTok expires quickly
    // Research their docs.

    const response = await axios.get(`${config.backendUrl}/tiktokauth`);
    const authUrl = response.data.url;
    setSimpleText(authUrl);
    // window.location.href = authUrl; 

    // ! Deprecated this needs to be improved
    // if (getRefreshToken() !== null && getRefreshToken() !== "") {
      // const response = await axios.post("process.env.BACKEND_URL/refresh", {
      //   refresh_token: getRefreshToken(),
      // });
      // igSaveToken(response.data.access_token);
      // igSaveRefreshToken(response.data.refresh_token);
      // navigate("/dashboard");
    // } else {
    //   const response = await axios.get("process.env.BACKEND_URL/tiktokauth");
    //   const authUrl = response.data.url;
    //   window.location.href = authUrl; 
    // }

  };

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
      {simpleText && <div role="alert" className="alert alert-error">
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
          <span>{simpleText}</span>
        </div>
      }
      <div className="hero bg-base-200 min-h-screen">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Login</h1>
            <p className="py-6">
              Let's get you generating your content!  We'll redirect you to get your instagram token after you verify your account and then we'll send you to the main page.  If you've already verified your account, just click the button below.
            </p>
            <button className="btn btn-primary" onClick={handleLogin}>Access Generator!</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
