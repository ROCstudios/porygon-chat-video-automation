import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { tiktokSaveToken, tiktokSaveRefreshToken } from "../util/TokenService";

const CallbackHandler = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      console.log("Handling callback");
      const urlParams = new URLSearchParams(window.location.search);
      console.log("URL params:", urlParams);
      const code = urlParams.get("code"); // Retrieve the authorization code
      console.log("Code:", code);

      if (code) {
        try {
          const response = await axios.post(`${process.env.BACKEND_URL}/tiktoken`, {
            code: code
          });
          if (response.status === 200) {
            tiktokSaveToken(response.data.access_token);
            tiktokSaveRefreshToken(response.data.refresh_token);

            // Redirect to the dashboard after successful authentication
            navigate("/dashboard");
          } else {
            alert("Authentication failed!");
          }
        } catch (error) {
          console.error("Error during callback processing:", error);
        }
      } else {
        alert("No authorization code found in the URL!");
      }
    };

    handleCallback();
  }, [navigate]);

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
      <div className="hero min-h-screen bg-base-200">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Processing Authentication...</h1>
            <div className="mt-4">
              <span className="loading loading-dots loading-lg"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CallbackHandler;
