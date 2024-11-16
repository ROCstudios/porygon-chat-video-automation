import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const CallbackHandler = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get("code"); // Retrieve the authorization code

      if (code) {
        try {
          const response = await axios.post("http://localhost:5000/callback", {
            code,
          });

          if (response.data.success) {
            navigate("/dashboard"); // Redirect to the dashboard after successful authentication
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

  return <h1>Processing Authentication...</h1>;
};

export default CallbackHandler;
