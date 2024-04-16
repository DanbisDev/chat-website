import Chat from "./Chat";
import LeftNav from "./LeftNav";

function Chats() {
  return (
    <div className="flex flex-row h-main">
      <div className="w-80">
        <LeftNav />
      </div>
      <div className="mx-auto pt-8 flex-col w-full">
        <Chat />
      </div>
    </div>
  )
}

export default Chats;