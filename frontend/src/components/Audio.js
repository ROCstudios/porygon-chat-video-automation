import React from "react";
import axios from "axios";
import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import StepsIndicator from "./StepsIndicator";
import NavBar from "./NavBar";
import config from "../config";
import ErrorAlert from "./ErrorAlert";

const Audio = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [audio, setAudio] = useState(null);
  const [audios, setAudios] = useState([]);

  useEffect(() => {
    getAudios();
  }, []);

  const handlePlay = (audioElement) => {
    if (audioElement) {
      audioElement.play();
    }
  }

  const getAudios = async () => {
    setLoading(true)
    const response = await axios.get(`${config.backendUrl}/getter/audios`);
    setAudios(response.data.audios);
    if (response.status == 200) {
    } else {
      setError(response.data.message)
    }
    setLoading(false)
  }

  const generationConfirmed = async () => {
    document.getElementById('winning_modal').close()
    setLoading(true);
    try {
      if (audio !== null) {
        const response = await axios.post(`${config.backendUrl}/set/audio`, {
          audio_url: audio
        });
        if (response.status === 200) {
          navigate('/poster');
        }
      }
      navigate('/poster');
    } catch (error) {
      console.error('Error generating content:', error);
      setError("Error: " + error.response.data.error);
    } finally {
      setLoading(false);
    }
  }

  const handleGenerate = () => {
    setError(null);
    document.getElementById('winning_modal').showModal()
  };

  return (
    <div>
      <dialog id="winning_modal" className="modal modal-bottom sm:modal-middle">
        <div className="modal-box">
          <h3 className="font-bold text-lg">This will generate a video for review.  Are you sure?</h3>
          <div className="py-4">
            <button className="btn btn-primary w-full max-w-lg" onClick={generationConfirmed}>
              Yes, generate my video!
            </button>
          </div>
          <div className="modal-action">
            <form method="dialog">
              <button className="btn">Cancel</button>
            </form>
          </div>
        </div>
      </dialog>
      <NavBar index={3} />
      {error && <ErrorAlert message={error} />}
      <StepsIndicator currentStep={3} />
      <div className="hero bg-base-200 min-h-screen -mt-16">
        <div className="hero-content text-center">
          <div className="max-w-lg">
            <h1 className="text-5xl font-bold">Upload your tunes</h1>
            <p className="py-6">
              {audio ? `${audio.split('/').pop().split('.')[0].replaceAll('_', ' ').replaceAll('%20', ' ')} selected! 🎉` : "Please select an audio file"}
            </p>
            <label className="flex flex-col items-center px-4 py-6 bg-white text-blue rounded-lg shadow-lg tracking-wide uppercase border border-blue cursor-pointer hover:bg-gray-500 hover:text-white transition duration-300 ease-in-out">
              <svg className="w-8 h-8" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
              </svg>
              <span className="mt-2 text-base leading-normal">Select an audio file</span>
              <input type='file' className="hidden" accept="audio/*" onChange={(e) => setAudio(e.target.files[0])} />
            </label>
            {loading ? (
              <div className="flex flex-col justify-center items-center h-full mt-4">
                <p className="text-xl">Getting audio. Please wait...</p>
                <span className="loading loading-dots loading-lg"></span>
              </div>
            ) : (
              <div className="dropdown dropdown-hover w-full">
                <div tabIndex={0} role="button" className="btn m-1 w-full bg-blue-500 text-white">Select an audio</div>
                <ul tabIndex={0} className="dropdown-content menu bg-base-100 rounded-box z-[1 p-2 shadow">
                  {audios.map((audio, index) => (
                    <li key={index}>
                      <div className="flex flex-col justify-between items-center">
                        <p>{audio.split('/').pop().split('.')[0].replaceAll('_', ' ').replaceAll('%20', ' ')}</p>
                        <audio src={audio}
                          controls
                          onPlay={(e) => {
                            e.preventDefault();
                            handlePlay(e.target);
                          }}
                        />
                        <button 
                          className="btn btn-sm w-full mt-2"
                          onClick={() => setAudio(audio)} 
                        >
                          Select this audio
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <button className="btn btn-primary w-full max-w-lg mt-4" onClick={handleGenerate}>Generate!</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Audio;
