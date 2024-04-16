import Message from "./Message";
import { useApi } from "../hooks";
import { useQuery, useQueryClient } from "react-query";
import { useParams } from "react-router-dom";
import ScrollContainer from "./ScrollContainer";
import Input from "./FormInput";
import Button from "./Button"
import { useState } from "react";
import { useMutation } from "react-query";

function MessageCard({ message }) {
    const cardClassName = [
        "bg-lgrn text-white",
        "border-2 border-slate-900",
        "shadow-md shadow-slate-900",
      ].join(" ");
    
      return (
          <div className={cardClassName}>
              <Message message={message}/>
          </div>
      )
}


function MessageCardQueryContainer({ chatId }) {
    const api = useApi();
    const { data } = useQuery({
      queryKey: ["messages", chatId],
      queryFn: () => (
        api.get(`/chats/${chatId}/messages`)
          .then((response) => response.json())
      ),
      enabled: chatId !== undefined,
    });
  
    if (data?.messages) {
      return data.messages.map((message) => <MessageCard key={message.id} message={message} />);
    }
  
    return null; // or some loading state
  }


function Messages() {
  const [new_message_txt, setMessageText] = useState("");
  const { chatId } = useParams();
  const api = useApi();
  const queryClient = useQueryClient();
  const newMessage = (e) => { 
    e.preventDefault();
    mutation.mutate();
    setMessageText("")
  }

  const mutation = useMutation({
    mutationFn: () => (
        api.post(
            `/chats/${chatId}/messages`,
            {
                "text": new_message_txt
            }
        )
    ),
    onSuccess: () => {
        queryClient.invalidateQueries({
            queryKey: ["messages", chatId]
        })
    }
  })
  if (chatId) {
    
    return (
        <ScrollContainer>
            <div className="max-h-3/4">
                <MessageCardQueryContainer chatId={chatId} />
                <form onSubmit={newMessage} style={{ display: 'flex', color: 'white', alignItems: 'center', justifyContent: 'space-between', paddingLeft: '10px', paddingRight: '10px' }}>
                    <Input
                        text="text"
                        type="text"
                        value={new_message_txt}
                        onChange={(e) => setMessageText(e.target.value)}
                        style={{ marginRight: '10px', flex: '1', height: '40px' }}
                    />
                    <Button type="submit" style={{ height: '40px', width: '80px' }}>send</Button>
                </form>
            </div>
        </ScrollContainer>

    )
  }

}

export default Messages;