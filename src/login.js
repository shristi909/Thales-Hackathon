import React, { useState } from "react";
import Webcam from "react-webcam";
import "./login.css";

function App() {
  const [isLogin, setIsLogin] = useState(true); // Toggle between Login and Sign Up
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState(""); // For the sign-up form
  const [image, setImage] = useState(null);
  const [showCamera, setShowCamera] = useState(false);

  const handleCapture = (webcamRef) => {
    if (webcamRef && webcamRef.current) {
      const capturedImage = webcamRef.current.getScreenshot();
      setImage(capturedImage);
      setShowCamera(false); // Hide the webcam after capturing the image
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isLogin) {
      console.log("Login Details:", { email, password });
    } else {
      console.log("Sign Up Details:", { name, email, password, image });
    }
  };

  const webcamRef = React.useRef(null);

  return (
    <div className="App">
      <div className="login-container">
        <h2>{isLogin ? "Login" : "Sign Up"} Form</h2>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <input
              type="text"
              placeholder="Enter your Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input-field"
              required
            />
          )}
          <input
            type="email"
            placeholder="Enter your Gmail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input-field"
            required
          />
          <input
            type="password"
            placeholder="Enter your Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
            required
          />
          <button
            type="button"
            onClick={() => setShowCamera(!showCamera)}
            className="capture-button"
          >
            {showCamera ? "Close Camera" : "Capture Image"}
          </button>

          {showCamera && (
            <div className="camera-container">
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="webcam-view"
              />
              <button
                type="button"
                onClick={() => handleCapture(webcamRef)}
                className="capture-image-button"
              >
                Capture
              </button>
            </div>
          )}

          {image && (
            <div className="captured-image">
              <h3>Captured Image:</h3>
              <img src={image} alt="Captured" />
            </div>
          )}

          <button type="submit" className="submit-button">
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>

        <p>
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <span
            className="toggle-link"
            onClick={() => {
              setIsLogin(!isLogin);
              setShowCamera(false); // Close the camera when switching
              setImage(null); // Reset captured image
            }}
          >
            {isLogin ? "Sign Up" : "Login"}
          </span>
        </p>
      </div>
    </div>
  );
}

export default App;
