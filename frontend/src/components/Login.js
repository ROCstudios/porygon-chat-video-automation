import React from "react";
import axios from "axios";

const Login = () => {
  const handleLogin = async () => {
    const response = await axios.get("http://localhost:8080/auth");
    const authUrl = response.data.url;
    console.log("Auth URL:", authUrl);
    window.location.href = authUrl; // Redirect to the Flask OAuth endpoint
  };

  return (
    <div>
      <h1>Login</h1>
      <button onClick={handleLogin}>Login with OAuth</button>
    </div>
  );
};

export default Login;
