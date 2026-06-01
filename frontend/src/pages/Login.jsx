import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const handleLogin = async () => {

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/login",
        {
          email,
          password
        }
      );

      console.log(
        "LOGIN RESPONSE:",
        response.data
      );

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      navigate("/dashboard");

    } catch (error) {

      alert("Login failed");

      console.log(error);
    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-lg shadow-md w-96">

        <h1 className="text-2xl font-bold mb-6">
          Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          className="w-full border p-3 rounded-lg mb-4"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-3 rounded-lg mb-4"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button
          onClick={handleLogin}
          className="bg-red-500 text-white px-4 py-3 rounded-lg w-full"
        >
          Login
        </button>

        <p className="text-center mt-5 text-sm">

          Don't have an account?

          <Link
            to="/signup"
            className="text-red-500 ml-1 font-medium"
          >
            Sign Up
          </Link>

        </p>

      </div>

    </div>
  );
}