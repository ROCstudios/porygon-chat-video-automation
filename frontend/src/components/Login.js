import React from "react";
import axios from "axios";
import { saveToken, getToken, getRefreshToken, saveRefreshToken } from "../util/TokenService";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = async () => {

    if (getRefreshToken() !== null && getRefreshToken() !== "") {
      const response = await axios.post("http://localhost:8080/refresh", {
        refresh_token: getRefreshToken(),
      });
      saveToken(response.data.access_token);
      saveRefreshToken(response.data.refresh_token);
      navigate("/dashboard");
    } else {
      const response = await axios.get("http://localhost:8080/auth");
      const authUrl = response.data.url;
      window.location.href = authUrl; 
    }

  };

  return (
    <div className="hero bg-base-200 min-h-screen">
      <div className="hero-content text-center">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold">Login</h1>
          <p className="py-6">
            Let's get you generating your content!  We'll redirect you to get your instagram token after you verify your account and then we'll send you to the main page.  If you've already verified your account, just click the button below.
          </p>
          <button className="btn btn-primary" onClick={handleLogin}>Access Generator!</button>
        </div>
      </div>
    </div>
  );
};

export default Login;
