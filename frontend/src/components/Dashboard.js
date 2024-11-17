import React from "react";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { igGetToken, tiktokGetToken } from "../util/TokenService";


const Dashboard = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [topic, setTopic] = useState("");
  const [caption, setCaption] = useState("");
  const [postToIg, setPostToIg] = useState(false);
  const [postToTiktok, setPostToTiktok] = useState(false);
  const [turns, setTurns] = useState(5);
  const [name, setName] = useState("");

  const [cloudUrl, setCloudUrl] = useState(null);

  const handleGenerate = async () => {
    setError(null);
    if (topic === "" || turns === 0 || turns > 10 || (postToIg === false && postToTiktok === false)) {
      setError("Please enter valid information");
      return;
    } else {
      setLoading(true);
      try {
        const response = await axios.post(`${process.env.BACKEND_URL}/generate`, {
          topic: topic,
          turns: turns,
          caption: caption,
          post_to_ig: postToIg,
          post_to_tiktok: postToTiktok,
          tiktok_access_token: tiktokGetToken(),
          name: name
        });
        console.log('🚀 ~ file: Dashboard.js:34 ~ handleGenerate ~ response:', response.data);

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
      {/* Open the modal using document.getElementById('ID').showModal() method */}
      <dialog id="winning_modal" className="modal modal-bottom sm:modal-middle">
        <div className="modal-box">
          <h3 className="font-bold text-lg">Your video is ready!</h3>
          <div className="py-4">
            {cloudUrl && (
              <a href={cloudUrl} target="_blank" rel="noopener noreferrer" className="btn btn-secondary w-full">
                View your video now.
              </a>
            )}
          </div>
          <div className="modal-action">
            <form method="dialog">
              <button className="btn">Close</button>
            </form>
          </div>
        </div>
      </dialog>
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
      <div className="hero bg-base-200 min-h-screen">
        <div className="hero-content text-center">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-full">
              <p className="text-xl">Please wait...</p>
              <span className="loading loading-dots loading-lg"></span>
            </div>
          ) : (
            <div className="max-w-lg">
              <h1 className="text-5xl font-bold">Let's Get This Chat Party Started! 🎉</h1>
            <p className="py-6">
              Describe your conversation and we'll post it for you and send back the video and links to access it.
            </p>
            <label>
              <div className="label">
                <span className="label-text">Name that appears above the chat bubbles</span>
              </div>
              <input
                type="text"
                placeholder="Type the name here..."
                className="input input-bordered input-md w-full max-w-lg"
                onChange={(e) => setName(e.target.value)}
                />
            </label>
            <label>
              <div className="label">
                <span className="label-text">Topic of the conversation that AI will generate</span>
              </div>
              <textarea
                placeholder="Type your chat here..."
                className="textarea textarea-bordered textarea-lg w-full max-w-lg"
                onChange={(e) => setTopic(e.target.value)}
                >
              </textarea>
            </label>
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
                <div className="label">
                    <span className="label-text">Number of chat bubbles</span>
                  </div>
                <input type="range" min={0} max="10" value={turns} className="range mt-4" onChange={(e) => setTurns(e.target.value)} />
                <p className="font-bold">Number of turns: {turns}</p>
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

export default Dashboard;
