import React from "react";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
const Dashboard = () => {
  const navigate = useNavigate();

  const [topic, setTopic] = useState("");
  const [caption, setCaption] = useState("");
  const [postToIg, setPostToIg] = useState(false);
  const [postToTiktok, setPostToTiktok] = useState(false);
  const [turns, setTurns] = useState(5);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (topic === "" || turns === 0 || turns > 10 || (postToIg === false && postToTiktok === false)) {
      alert("Please enter valid information");
      return;
    } else {
      try {
        const response = await axios.post('http://localhost:8080/generate', {
          topic: topic,
          turns: turns,
          caption: caption,
          post_to_ig: postToIg,
          post_to_tiktok: postToTiktok
        });
      } catch (error) {
        console.error('Error generating content:', error);
        alert('Failed to generate content');
      }
    }
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
              <li><a>Homepage</a></li>
              <li><a>Portfolio</a></li>
              <li><a>About</a></li>
            </ul>
          </div>
        </div>
        <div className="navbar-center">
          <a className="btn btn-ghost text-xl">AI Content Generator</a>
        </div>
        <div className="navbar-end">
        </div>
      </div>
      <div className="hero bg-base-200 min-h-screen">
        <div className="hero-content text-center">
          <div className="max-w-lg">
            <h1 className="text-5xl font-bold">Enter Your Chat</h1>
            <p className="py-6">
              Describe your conversation and we'll post it for you and send back the video and links to access it.
            </p>
            <textarea
              placeholder="Type your chat here..."
              className="textarea textarea-bordered textarea-lg w-full max-w-lg"
              onChange={(e) => setTopic(e.target.value)}
            >
            </textarea>
            <textarea
              placeholder="Enter a caption for your video..."
              className="textarea textarea-bordered textarea-lg w-full max-w-lg"
              onChange={(e) => setCaption(e.target.value)}
            >
            </textarea>
            <div className="flex w-full max-w-lg mb-4">
              <div className="w-1/2 pr-2">
                <div className="form-control">
                  <label className="cursor-pointer label">
                    <span className="label-text">Post to Instagram</span>
                    <input type="checkbox" className="checkbox checkbox-primary" />
                  </label>
                </div>
                <div className="form-control">
                  <label className="cursor-pointer label">
                    <span className="label-text">Post to TikTok</span>
                    <input type="checkbox" className="checkbox checkbox-secondary" />
                  </label>
                </div>
              </div>
              <div className="w-1/2 pl-2">
                <input type="range" min={0} max="10" value={turns} className="range mt-4" onChange={(e) => setTurns(e.target.value)} />
                <p>Number of turns: {turns}</p>

              </div>
            </div>
            <button className="btn btn-primary w-full max-w-lg mt-4" onClick={handleGenerate}>Generate!</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
