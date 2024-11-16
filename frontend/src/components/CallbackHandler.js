import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const CallbackHandler = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      console.log("Handling callback");
      const urlParams = new URLSearchParams(window.location.search);
      console.log("URL params:", urlParams);
      const code = urlParams.get("code"); // Retrieve the authorization code
      console.log("Code:", code);

      // if (code) {
      if (true) {
        try {
          const response = await axios.post("http://localhost:8080/token", {
            // code,
            code: '80-wN4DpQpIImAeMVuHJVpmtu00YRZqiOxhIsAlZ-P59UqyCuW4LXAz8L-CILvdH0bB2IlQyrQSHxcTcet7NCE3CHzx0aUscm7ayZY9fUvmPk9up1Ijs5nb6UY7_7v8jWmzc6LST-CVm8lXL5ZiOiWtzCekJQiq-yhBiUH8K9sj21i_hEoRQU4YDZxAe4jlp%2A1%216299.va'
          });
          console.log("Response:", response);

          if (response.status === 200) {
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
