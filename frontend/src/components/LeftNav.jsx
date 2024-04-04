import { useApi } from "../hooks"
import { useQuery } from "react-query"
import { NavLink } from "react-router-dom"


function Link({ chat }) {
    const url = chat.empty ? "#" : `/chats/${chat.id}`;
    const className = ({ isActive }) => [
      "p-2",
      "hover:bg-gray-600 hover:text-grn",
      "flex flex-row justify-between",
      isActive ?
        "bg-gray-700 text-grn font-bold" :
        ""
    ].join(" ");
  
    const chatName = ({ isActive }) => (
      (isActive ? "\u00bb " : "") + chat.name
    );
  
    return (
      <NavLink to={url} className={className}>
        {chatName}
      </NavLink>
    );
  }

const emptyChat = (id) => ({
    id,
    name: "loading...",
    empty: true,
  });
  


function LeftNav() {
    const api = useApi();
  
    const { data } = useQuery({
      queryKey: ["chats"],
      queryFn: () => (
        api.get("/chats")
          .then((response) => response.json())
      ),
    });
  
    const chats = ( data?.chats || [1, 2, 3].map(emptyChat));
  
    return (
      <nav className="flex flex-col border-r-2 border-purple-400 h-main text-lg">
        <div className="flex flex-col border-b-2 border-purple-400">
          {chats.map((chat) => (
            <Link key={chat.id} chat={chat} className="text-xl"/>
          ))}
        </div>
      </nav>
    );
  }
  
  export default LeftNav;