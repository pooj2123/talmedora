import { useState } from "react";
import API from "../services/api";

function UploadBox({ refreshReports }) {

  const [file, setFile] = useState(null);

  const [description, setDescription] =
    useState("");

  const [message, setMessage] = useState("");

  const [uploadedFileName, setUploadedFileName] =
    useState("");

  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {

    if (!file) {

      alert("Please select a PDF");

      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    formData.append(
      "description",
      description
    );

    try {

      setLoading(true);

      const token =
  localStorage.getItem("token");

console.log(
  "TOKEN FROM STORAGE:",
  token
);

console.log(localStorage.getItem("token"));
const response = await API.post(
  "/upload",
  formData,
  {
    headers: {

      Authorization:
        `Bearer ${token}`,

      "Content-Type":
        "multipart/form-data",
    },
  }
);

      setMessage(response.data.message);

      setUploadedFileName(
        response.data.filename
      );

      // refresh reports instantly
      refreshReports();

    } catch (error) {

      console.error(error);

      setMessage("Upload failed");

    } finally {

      setLoading(false);
    }
  };

  const handleReset = () => {

    setFile(null);

    setDescription("");

    setMessage("");

    setUploadedFileName("");

    // clears file input visually
    document.getElementById(
      "pdf-upload"
    ).value = "";
  };

  return (

    <div className="bg-white p-6 rounded-2xl border">

      <h2 className="text-2xl font-bold mb-4">
        Upload Medical Report
      </h2>

      <div className="space-y-4">

        <input
          id="pdf-upload"
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
          className="border p-3 rounded-xl w-full"
        />

        <textarea
          placeholder="Add short description about this report..."
          value={description}
          onChange={(e) =>
            setDescription(e.target.value)
          }
          className="w-full border rounded-xl p-4 outline-none resize-none"
        />

        <div className="flex gap-3">

          <button
            onClick={handleUpload}
            disabled={loading}
            className="bg-red-500 text-white px-5 py-2 rounded-xl"
          >
            {loading
              ? "Uploading..."
              : "Upload"}
          </button>

          <button
            onClick={handleReset}
            className="bg-gray-200 px-5 py-2 rounded-xl"
          >
            Reset
          </button>

        </div>

      </div>

      {uploadedFileName && (

        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-xl">

          <p className="font-medium text-green-700">
            Report Uploaded Successfully
          </p>

          <p className="text-sm text-gray-600 mt-1">
            {uploadedFileName}
          </p>

        </div>

      )}

      {message && (

        <p className="mt-4 text-gray-600">
          {message}
        </p>

      )}

    </div>
  );
}

export default UploadBox;