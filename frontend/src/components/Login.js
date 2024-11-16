import React from "react";
import axios from "axios";
import { saveToken, getToken, getRefreshToken, saveRefreshToken } from "../util/TokenService";
import axios from "axios";

const Login = () => {
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
    <div>
      <h1>Login</h1>
      <button onClick={handleLogin}>Access Generator!</button>
    </div>
  );
};

export default Login;
