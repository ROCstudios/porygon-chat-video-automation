import React from "react";

const Login = () => {
  const handleLogin = () => {
    const authUrl = "http://localhost:5000/auth"; // Flask server OAuth endpoint
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
