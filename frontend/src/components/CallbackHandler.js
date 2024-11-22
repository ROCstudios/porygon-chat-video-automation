import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { tiktokSaveToken, tiktokSaveRefreshToken } from "../util/TokenService";
import config from "../config";
import NavBar from "./NavBar";

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
          const response = await axios.post(`${config.backendUrl}/tiktoken`, {
            code: code
          });
          if (response.status === 200) {
            tiktokSaveToken(response.data.access_token);
            tiktokSaveRefreshToken(response.data.refresh_token);

            // Redirect to the dashboard after successful authentication
            navigate("/instaauth");
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
      <NavBar />
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
