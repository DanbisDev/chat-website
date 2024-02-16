import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import Chats from './components/Chats'
import './App.css'

const queryClient = new QueryClient();

function NotFound() {
  return <h1> 404: not found</h1>
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
            <Route path="/" element={<Chats />} />
            <Route path="/chats" element={<Chats />} />
            <Route path="/chats/:chatID" element={<Chats />} />
            <Route path="/error/404" element={<NotFound></NotFound>} />
            <Route path="*" element={<Navigate to="/error/404"/>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
