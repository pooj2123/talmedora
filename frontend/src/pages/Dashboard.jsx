import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function Dashboard() {

  return (

    <div className="flex bg-gray-100 min-h-screen">

      <Sidebar />

      <div className="flex-1 p-6">

        <Navbar />

        <div className="mt-6 bg-white p-8 rounded-2xl border">

          <h1 className="text-4xl font-bold text-red-600">
            TALMedora
          </h1>

          <p className="mt-4 text-gray-600 text-lg">
            AI-powered medical report intelligence platform
            helping users understand healthcare reports
            in simple language.
          </p>

        </div>

        <div className="grid grid-cols-3 gap-6 mt-6">

          <div className="bg-white p-6 rounded-2xl border">
            <h2 className="text-xl font-bold mb-2">
              Upload Reports
            </h2>

            <p className="text-gray-600">
              Upload and analyze medical PDFs securely.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border">
            <h2 className="text-xl font-bold mb-2">
              AI Assistant
            </h2>

            <p className="text-gray-600">
              Ask questions about your reports naturally.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border">
            <h2 className="text-xl font-bold mb-2">
              Smart Insights
            </h2>

            <p className="text-gray-600">
              Get simplified explanations and findings.
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;