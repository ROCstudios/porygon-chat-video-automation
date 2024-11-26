import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { igGetToken, tiktokGetToken } from "../util/TokenService";
import StepsIndicator from "./StepsIndicator";
import NavBar from "./NavBar";
import config from "../config";
import ErrorAlert from "./ErrorAlert";

const Poster = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [caption, setCaption] = useState("");
  const [postToIg, setPostToIg] = useState(false);
  const [postToTiktok, setPostToTiktok] = useState(false);

  const [cloudUrl, setCloudUrl] = useState(null);

  useEffect(() => {
    if (cloudUrl == null) {
      initPoster();
    }
  }, [])

  const initPoster = async () => {
    try {
      setLoading(true);
      const posterResponse = await axios.post(`${config.backendUrl}/generate/movie`);
      console.log('🚀 ~ file: Poster.js:34 ~ useEffect ~ posterResponse:', posterResponse.data);
      setCloudUrl(posterResponse.data.cloud_url);
      setLoading(false);
    } catch (error) {
      console.error('Error generating content:', error);
      setError("Error: " + error.response.data.error);
    }
  }

  const handleGenerate = async () => {
    setError(null);
    if ((postToIg === false && postToTiktok === false)) {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${config.backendUrl}/generate/poster`, {
          caption: caption,
          post_to_ig: postToIg,
          post_to_tiktok: postToTiktok,
          tiktok_access_token: tiktokGetToken()
        });
        console.log('🚀 ~ file: Poster.js:34 ~ handleGenerate ~ response:', response.data);

        if (response.data.status === 'success') {
          setCloudUrl(response.data.cloud_url);
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
      {error && <ErrorAlert message={error + " : You will likely need to go back to the start and try again."} />}
      <StepsIndicator currentStep={4} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          {loading && error === null ? (
            <div className="flex flex-col justify-center items-center h-full">
              <p className="text-xl">Please wait...</p>
              <span className="loading loading-dots loading-lg"></span>
            </div>
          ) : (
            <div className="max-w-2xl">
              <h1 className="text-5xl font-bold">Take a Look</h1>
              <p className="py-6">
              </p>
              <video alt="Generated video" controls>
                <source src={cloudUrl} type="video/mp4" />
              </video>

              <button className="btn btn-primary w-full max-w-xl mt-4" onClick={handleGenerate}>Post it now!!</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Poster;
