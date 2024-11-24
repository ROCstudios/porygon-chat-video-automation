import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import CallbackHandler from "./components/CallbackHandler";
import InstaLogin from "./components/InstaLogin";
import Poster from "./components/Poster";
import Conversation from "./components/Conversation";
import Avatar from "./components/Avatar";
import Audio from "./components/Audio";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/instaauth" element={<InstaLogin />} />
        <Route path="/redirect" element={<CallbackHandler />} />
        <Route path="/conversation" element={<Conversation />} />
        <Route path="/avatar" element={<Avatar />} />
        <Route path="/audio" element={<Audio />} />
        <Route path="/poster" element={<Poster />} />
      </Routes>
    </Router>
  );
}

export default App;
