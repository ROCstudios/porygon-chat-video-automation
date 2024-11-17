import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { igSaveToken, igSaveRefreshToken, tiktokSaveToken, tiktokSaveRefreshToken } from "../util/TokenService";

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
          const response = await axios.post("http://localhost:8080/tiktoken", {
            // code,
            code: 'cXf_XwR0YbyVRy3eMXZQjyWhws0ebSRsInyXtQOnJ9uiq9kERQTj01J65BtUAHIGKAgdc7l2qn7QtLME6zzVTQolaYbavRUq73TEAFoQkrdJlsp4gFTwwtVNP5l5OcCv8avQb6QqHIZ75ykJwfpKLGQ_Vutjzh-nV8yuoa9AOBmb87t3STvqg0bPFepHFFn_%2A3%216345.va'
          });
          console.log('🚀 ~ file: CallbackHandler.js:26 ~ handleCallback ~ response:', response);
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

  return <h1>Processing Authentication...</h1>;
};

export default CallbackHandler;
