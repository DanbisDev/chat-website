import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import { AuthProvider } from './context/auth'
import { UserProvider } from './context/user'
import { useAuth } from "./hooks"
import Login from "./components/Login"
import Registration from "./components/Registration"
import Chats from "./components/Chats"
import TopNav from "./components/TopNav"
import Profile from "./components/Profile"
import Home from "./components/Home"

const queryClient = new QueryClient();



function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} /> 
      <Route path="/" element={<Home/>}/>
      <Route path="*" element={<Navigate to="/login"></Navigate>}/>
    </Routes>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/chats" element={<Chats />} />
      <Route path="/chats/:chatId" element={<Chats />} />
      <Route path="profile" element={<Profile />} />
      <Route path="*" element={<Navigate to="/chats"></Navigate>}/>
    </Routes>
  )
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  )
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="max-h-main">
      {isLoggedIn ?
      <AuthenticatedRoutes /> :
      <UnauthenticatedRoutes />}
    </main>
  )
}

function App() {
  return (
    <div className="min-w-screen bg-gray-800 text-white min-h-screen">
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
            <AuthProvider>
              <UserProvider>
                  <Header />
                  <Main />
              </UserProvider>
            </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
    </div>
  );
}

export default App
