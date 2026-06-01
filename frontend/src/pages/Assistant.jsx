import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import ChatBox from "../components/ChatBox";

function Assistant() {

  return (

    <div className="flex bg-gray-100 min-h-screen">

      <Sidebar />

      <div className="flex-1 p-6">

        <Navbar />

        <ChatBox />

      </div>

    </div>
  );
}

export default Assistant;