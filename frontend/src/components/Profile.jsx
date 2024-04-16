import { useEffect, useState } from "react";
import { useAuth, useUser } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [created_at, setCreatedAt] = useState("");

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
    const date = new Date(user.created_at);
    const formattedDate = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
    setCreatedAt(formattedDate);
    }
  }

  useEffect(reset, [user]);

  return (
    <div className="max-w-96 mx-auto px-4 py-8 bg-grey-800 shadow-md rounded-lg">
      <h2 className="text-2xl font-bold py-2 text-center text-blue-500">
        Profile
      </h2>
      <div className="border border-gray-600 rounded px-4 py-2">
        <div className="flex justify-between mb-4">
          <span className="font-bold text-white">Username:</span>
          <span className="text-white">{username}</span>
        </div>
        <div className="flex justify-between mb-4">
          <span className="font-bold text-white">Email:</span>
          <span className="text-white">{email}</span>
        </div>
        <div className="flex justify-between mb-4">
          <span className="font-bold text-white">Created At:</span>
          <span className="text-white">{created_at}</span>
        </div>
      </div>
      <div className="flex justify-center items-center">
        <Button onClick={logout} className="mt-4 bg-blue-500 text-white rounded ">
          logout
        </Button>
      </div>
    </div>
  );
}

export default Profile;
