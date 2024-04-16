import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useApiWithoutToken, useAuth } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return (
    <div className="text-red-300 text-xs">
      {message}
    </div>
  );
}

function RegistrationLink() {
  return (
    <div className="pt-8 flex flex-col">
      <p>Don&apos;t have an account? <Link to="/registration" className="text-blue-500 hover:underline">Create an account</Link></p>
    </div>
  );
}

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const { login } = useAuth();
  const api = useApiWithoutToken();

  const disabled = username === "" || password === "";

  const onSubmit = (e) => {
    e.preventDefault();

    api.postForm("/auth/token", { username, password })
      .then((response) => {
        if (response.ok) {
          response.json().then(login).then(
            () => navigate("/animals")
          );
        } else if (response.status === 401) {
          response.json().then((data) => {
            setError(data.detail.error_description);
          });
        } else {
          setError("error logging in");
        }
      });
  }

  return (
    <div className="max-w-96 mx-auto px-4 py-8 bg-grey-800 shadow-md rounded-lg">
      <form className="space-y-4" onSubmit={onSubmit}>
        <FormInput
          type="text"
          name="username"
          setter={setUsername}
          className="bg-gray-700 text-white rounded"
        />
        <FormInput
          type="password"
          name="password"
          setter={setPassword}
          className="bg-gray-700 text-white rounded"
        />
        <Button
          className="w-full bg-blue-500 text-white rounded"
          type="submit"
          disabled={disabled}
        >
          login
        </Button>
        <Error message={error} />
      </form>
      <RegistrationLink />
    </div>
  );
}

export default Login;
