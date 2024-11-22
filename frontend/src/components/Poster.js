import React from "react";
import axios from "axios";
import { useState } from "react";
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

          document.getElementById('winning_modal').showModal()
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
      { error && <ErrorAlert message={error} /> }
      <StepsIndicator currentStep={6} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-full">
              <p className="text-xl">Please wait...</p>
              <span className="loading loading-dots loading-lg"></span>
            </div>
          ) : (
            <div className="max-w-lg">
              <h1 className="text-5xl font-bold">Get Posting!</h1>
            <p className="py-6">
            </p>
            <label>
              <div className="label">
                <span className="label-text">Caption for your video</span>
              </div>
              <textarea
                placeholder="Enter a caption for your video..."
                className="textarea textarea-bordered textarea-lg w-full max-w-lg"
                onChange={(e) => setCaption(e.target.value)}
                >
              </textarea>
            </label>
            <div className="flex w-full max-w-lg mb-4">
              <div className="w-1/2 pr-2">
                <div className="form-control">
                    <div className="label">
                      <span className="label-text">Where we'll post your video</span>
                    </div>
                  <label className="cursor-pointer label">
                    <span className="label-text font-bold">Post to Instagram</span>
                    <input 
                      type="checkbox" 
                      className="checkbox checkbox-primary"
                      checked={postToIg}
                      onChange={(e) => setPostToIg(e.target.checked)}
                    />
                  </label>
                </div>
                <div className="form-control">
                  <label className="cursor-pointer label">
                    <span className="label-text font-bold">Post to TikTok</span>
                    <input 
                      type="checkbox" 
                      className="checkbox checkbox-secondary"
                      checked={postToTiktok}
                      onChange={(e) => setPostToTiktok(e.target.checked)}
                    />
                  </label>
                </div>
              </div>
              <div className="w-1/2 pl-2">
              </div>
            </div>
              <button className="btn btn-primary w-full max-w-lg mt-4" onClick={handleGenerate}>Generate!</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Poster;
