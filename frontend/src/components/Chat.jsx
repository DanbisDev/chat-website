import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import { useApi } from "../hooks";
import Messages from "./Messages";


function NoChat() {
    return (
        <div className="font-bold text-2xl py-4 text-center">
            loading...
        </div>
    )
}

function ChatCard({ chat }) {
  
    const cardClassName = [
      "bg-lgrn text-black",
      "border-2 border-slate-900",
      "shadow-md shadow-slate-900",
    ].join(" ");
  
    return (
      <div className="flex flex-col w-full">
        <h2 className="text-center text-2xl text-grn font-bold py-4">
          {chat.name}
        </h2>
        <div className={cardClassName}>
            <Messages />
        </div>
      </div>
    )
  }

function ChatCardQueryContainer({ chatId }) {
    const api = useApi();
    const { data } = useQuery({
      queryKey: ["chats", chatId],
      queryFn: () => (
        api.get(`/chats/${chatId}`)
          .then((response) => response.json())
      ),
      enabled: chatId !== undefined,
    });
  
    if (data?.chat) {
      return <ChatCard chat={data.chat} />
    }
  
    return <NoChat />;
  }
  
  function Chat() {
    const { chatId } = useParams();
  
    if (chatId) {
      return (
        <ChatCardQueryContainer chatId={chatId} />
      );
    } else {
        return (
            <div className="flex flex-col items-center justify-center bg-gray-800 text-white">
                <h1 className="text-4xl font-bold mb-2">Welcome to Pony Express</h1>
                <p className="text-lg">To begin chatting please select a chat on the left side of the screen</p>
            </div>
        )
    }
  
  }
  
  export default Chat;