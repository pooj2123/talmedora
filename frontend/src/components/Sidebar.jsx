import { Link } from "react-router-dom";

function Sidebar() {

  const handleLogout = () => {

    localStorage.removeItem("token");

    window.location.href = "/login";
  };

  return (

    <div className="w-64 bg-white h-screen border-r p-5 flex flex-col">

      <div>

        <div className="mb-10">

          <h1 className="text-3xl font-bold text-red-600">
            TALMedora
          </h1>

          <p className="text-gray-500 text-sm">
            AI Medical Assistant
          </p>

        </div>

        <div className="space-y-3">

          <Link to="/dashboard">

            <button className="w-full text-left p-3 rounded-xl hover:bg-red-50">
              Dashboard
            </button>

          </Link>

          <Link to="/reports">

            <button className="w-full text-left p-3 rounded-xl hover:bg-red-50">
              Reports
            </button>

          </Link>

          <Link to="/assistant">

            <button className="w-full text-left p-3 rounded-xl hover:bg-red-50">
              AI Assistant
            </button>

          </Link>

        </div>

      </div>

      <div className="mt-auto">

        <button
          onClick={handleLogout}
          className="w-full bg-red-600 text-white p-3 rounded-xl hover:bg-red-700"
        >
          Logout
        </button>

      </div>

    </div>
  );
}

export default Sidebar;