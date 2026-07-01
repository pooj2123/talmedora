import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";

import API from "../services/api";

function Reports() {

  const [reports, setReports] = useState([]);

  const [search, setSearch] = useState("");

  const [expandedReport, setExpandedReport] = useState(null);

  // Fetch reports
  const fetchReports = async () => {

    try {

      const token =
        localStorage.getItem("token");

      const response = await API.get(
        "/reports",
        {
          headers: {

            Authorization:
              `Bearer ${token}`
          }
        }
      );

      setReports(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  useEffect(() => {

    fetchReports();

  }, []);

  // Download report
  const handleDownload = async (id, filename) => {

    try {

      const token =
        localStorage.getItem("token");

      const response = await API.get(
        `/download/${id}`,
        {
          responseType: "blob",

          headers: {

            Authorization:
              `Bearer ${token}`
          }
        }
      );

      const url =
        window.URL.createObjectURL(
          new Blob([response.data])
        );

      const link =
        document.createElement("a");

      link.href = url;

      link.setAttribute(
        "download",
        filename
      );

      document.body.appendChild(
        link
      );

      link.click();

      link.remove();

    } catch (error) {

      console.error(error);

      alert(
        "Download failed"
      );
    }
  };

  // Delete report
  const handleDelete = async (id) => {

    try {

      const token =
        localStorage.getItem("token");

      await API.delete(
        `/delete/${id}`,
        {
          headers: {

            Authorization:
              `Bearer ${token}`
          }
        }
      );

      fetchReports();

    } catch (error) {

      console.error(error);
    }
  };

  // Search filter
  const filteredReports = reports.filter(
    (report) =>

      report.filename
        .toLowerCase()
        .includes(search.toLowerCase())

      ||

      report.description
        .toLowerCase()
        .includes(search.toLowerCase())
  );

  return (

    <div className="flex bg-gray-100 min-h-screen">

      <Sidebar />

      <div className="flex-1 p-6">

        <Navbar />

        <div className="mt-6">

          <UploadBox
            refreshReports={fetchReports}
          />

        </div>

        <div className="bg-white p-6 rounded-2xl border mt-6">

          <div className="flex justify-between items-center mb-6">

            <h2 className="text-2xl font-bold">
              Uploaded Reports
            </h2>

            <input
              type="text"
              placeholder="Search reports..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              className="border rounded-xl px-4 py-2 outline-none"
            />

          </div>

          {filteredReports.length === 0 && (

            <div className="text-gray-500 text-center py-10">

              No reports found

            </div>

          )}

          <div className="space-y-4">

  {filteredReports.map((report) => (

    <div
      key={report.id}
      className="border rounded-2xl p-5 bg-gray-50"
    >

      <div className="flex justify-between items-start">

        <div className="flex-1">

          <h3 className="font-bold text-lg">
            {report.filename}
          </h3>

          <p className="text-gray-600 text-sm mt-1">
            {report.description}
          </p>

          <div className="mt-4">

            <button
              onClick={() =>
                setExpandedReport(
                  expandedReport === report.id
                    ? null
                    : report.id
                )
              }
              className="text-red-500 font-medium text-sm"
            >
              {expandedReport === report.id
                ? "Hide AI Summary"
                : "View AI Summary"}
            </button>

            {expandedReport === report.id && (

              <div className="mt-3 bg-white border rounded-xl p-4">

                <h4 className="font-semibold mb-2">
                  AI Summary
                </h4>

                <p className="text-gray-700 whitespace-pre-line">
                  {report.summary}
                </p>

              </div>

            )}

          </div>

        </div>

        <div className="flex gap-3 ml-6">

          <button
            onClick={() =>
              handleDownload(
                report.id,
                report.filename
              )
            }
            className="bg-red-500 text-white px-4 py-2 rounded-xl"
          >
            Download
          </button>

          <button
            onClick={() =>
              handleDelete(
                report.id
              )
            }
            className="bg-gray-200 px-4 py-2 rounded-xl"
          >
            Delete
          </button>

        </div>

      </div>

    </div>

  ))}

</div>

      </div>

    </div>
    </div>


  );
}

export default Reports;