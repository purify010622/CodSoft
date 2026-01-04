import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { GameProvider } from './context/GameContext'

// Pages
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import GameMode from './pages/GameMode'
import GamePlay from './pages/GamePlay'
import OnlineGame from './pages/OnlineGame'
import Profile from './pages/Profile'
import Leaderboard from './pages/Leaderboard'
import Settings from './pages/Settings'
import AdminDashboard from './pages/AdminDashboard'

// Components
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <Router>
      <AuthProvider>
        <GameProvider>
          <AppContent />
        </GameProvider>
      </AuthProvider>
    </Router>
  )
}

function AppContent() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-white"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      {user && <Navbar />}
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path="/register" element={!user ? <Register /> : <Navigate to="/" />} />
        
        {/* Protected Routes */}
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/game-mode" element={<ProtectedRoute><GameMode /></ProtectedRoute>} />
        <Route path="/game/:mode" element={<ProtectedRoute><GamePlay /></ProtectedRoute>} />
        <Route path="/online" element={<ProtectedRoute><OnlineGame /></ProtectedRoute>} />
        <Route path="/profile/:userId?" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/leaderboard" element={<ProtectedRoute><Leaderboard /></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>} />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  )
}

export default App
