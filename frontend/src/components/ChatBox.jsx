import { useState } from "react";
import API from "../services/api";
import ReactMarkdown from "react-markdown";

function ChatBox() {

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {

    if (!question) return;

    const userMessage = {
      type: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {

      const token =
        localStorage.getItem("token");

      const response = await API.post(
        "/chat",
        {
          question: question,
        },
        {
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

      const aiMessage = {
        type: "ai",
        text: response.data.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {

      console.error(error);

      const errorMessage = {
        type: "ai",
        text: "Error getting AI response.",
      };

      setMessages((prev) => [...prev, errorMessage]);

    } finally {

      setLoading(false);

      setQuestion("");
    }
  };

  return (

    <div className="bg-white p-6 rounded-2xl border mt-6">

      <h2 className="text-xl font-bold mb-4">
        Chat with AI Assistant
      </h2>

      <div className="h-96 overflow-y-auto border rounded-xl p-4 bg-gray-50">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`mb-4 flex ${
              msg.type === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-[80%] p-4 rounded-2xl ${
                msg.type === "user"
                  ? "bg-red-500 text-white"
                  : "bg-white border"
              }`}
            >

              <ReactMarkdown>
                {msg.text}
              </ReactMarkdown>

            </div>

          </div>

        ))}

        {loading && (

          <div className="text-gray-500">
            Thinking...
          </div>

        )}

      </div>

      <div className="mt-4 flex gap-3">

        <textarea
          placeholder="Ask medical questions..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          className="flex-1 border rounded-xl p-4 outline-none resize-none"
        />

        <button
          onClick={handleAsk}
          className="bg-red-500 text-white px-6 rounded-xl"
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default ChatBox;