function Chat({ message }) {
    // Format the date and time
    const date = new Date(message.created_at);
    const timestamp = `${date.getMonth() + 1}-${date.getDate()}-${date.getFullYear()} - ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
  
    return (
      <div className="flex flex-col bg-gray-700 text-white rounded p-2 mb-2">
        <div className="text-right text-xs text-gray-400">
          {timestamp}
        </div>
        <div className="flex">
          <span className="font-bold text-blue-400 mr-2 w-20">{message.user.username}:</span>
          <p className="flex-1 text-left pl-2.5">{message.text}</p>
        </div>
      </div>
    );
  }
  
  


export default Chat;