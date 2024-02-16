/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import './Chats.css'

function ChatListItem({ chat }) {
    return (
        <li>
          <Link key={chat} to={`/chats/${chat.id}`} className="chat-list-button">
            <p>{chat.name}</p> 
            <small>{new Date(chat.created_at).toLocaleString('en-US')}</small> 
            </Link>
          </li>
    )
  }

function ChatList({ chats }) {
    return (
        <div className="chat-list left-column">
            <ul>
                {chats.map((chat) => (
                    <ChatListItem key={chat.id} chat={chat} />
                ))}
            </ul>
        </div>
    )
}

function ChatListContainer() {
    const { data } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
          fetch("http://127.0.0.1:8000/chats")
            .then((response) => response.json())
        ),
      });
    
      if (data?.chats) {
        return (
          <div className="chat-list-container">
            <h2>Chat List</h2>
            <ChatList chats={data.chats} />
          </div>
        )
      }
    
      return (
        <h2>chat list</h2>
      );
}

function MessageCard({ message }) {

  //const attributes = ["user_id", "text", "created_at"];

  return (
    <div className="message-card right-column">
      {message.map((msg, index) => (
        <div key={index} className="message">
          <p>{msg["user_id"]}: {msg["text"]}</p>
        </div>
      ))}
    </div>
  );
  }

function MessagesCardContainer({ messages, selected_chat }) {
    return (
      <div className="chat-card-container right-column">
        <h1>{selected_chat.name}: {selected_chat.owner_id}&apos;s chat</h1>
        <h3>User&apos;s in chat: {selected_chat.user_ids.toString().replaceAll(",", ", ")} </h3>
        <MessageCard message={messages} />
      </div>
    );
  }

function ChatCardQueryContainer({ chatID }) {
  if (!chatID) {
    return <h2>Pick a chat</h2>;
}

const { data: messagesData } = useQuery({
    queryKey: ["messages", chatID],
    queryFn: () => (
        fetch(`http://127.0.0.1:8000/chats/${chatID}/messages`)
            .then((response) => response.json())
    ),
});

const { data: chatData } = useQuery({
  queryKey: ["chats", chatID],
  queryFn: () => (
    fetch(`http://127.0.0.1:8000/chats/${chatID}`)
    .then((response) => response.json())
  )
});


if (messagesData && messagesData.messages && chatData && chatData.chat) {
    return <MessagesCardContainer selected_chat={chatData.chat} messages={messagesData.messages}  />;
}

return <h2>loading...</h2>;
  }

function Chats() {
    const { chatID } = useParams();
    return (
        <div className="chats-page">
            <ChatListContainer />
            <ChatCardQueryContainer chatID={chatID} />
        </div>
    );
}

export default Chats