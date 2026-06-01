import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const handleSignup = async () => {

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/register",
        {
          email,
          password
        }
      );

      alert(
        response.data.message
      );

      navigate("/login");

    } catch (error) {

      console.log(error);

      alert(
        error?.response?.data?.message
        || "Signup failed"
      );

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-2xl shadow-md w-96">

        <h1 className="text-3xl font-bold mb-2">
          Create Account
        </h1>

        <p className="text-gray-500 mb-6">
          Join TALMedora
        </p>

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
          className="w-full border p-3 rounded-lg mb-6"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button
          onClick={handleSignup}
          disabled={loading}
          className="w-full bg-red-500 text-white py-3 rounded-lg"
        >
          {
            loading
            ? "Creating..."
            : "Sign Up"
          }
        </button>

        <p className="text-center mt-5 text-sm">

          Already have an account?

          <Link
            to="/login"
            className="text-red-500 ml-1"
          >
            Login
          </Link>

        </p>

      </div>

    </div>
  );
}