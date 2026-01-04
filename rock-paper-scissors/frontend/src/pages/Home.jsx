import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { motion } from 'framer-motion'

const Home = () => {
  const { userData } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="container mx-auto px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold text-white mb-4">
          Welcome, {userData?.display_name || 'Player'}!
        </h1>
        <p className="text-xl text-white/80">
          Choose your game mode and start playing
        </p>
      </motion.div>

      {/* Stats Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12"
      >
        <div className="card text-center">
          <p className="text-gray-400 text-sm">Total Games</p>
          <p className="text-3xl font-bold text-primary">{userData?.stats?.total_games || 0}</p>
        </div>
        <div className="card text-center">
          <p className="text-gray-400 text-sm">Wins</p>
          <p className="text-3xl font-bold text-green-500">{userData?.stats?.wins || 0}</p>
        </div>
        <div className="card text-center">
          <p className="text-gray-400 text-sm">Losses</p>
          <p className="text-3xl font-bold text-red-500">{userData?.stats?.losses || 0}</p>
        </div>
        <div className="card text-center">
          <p className="text-gray-400 text-sm">Win Rate</p>
          <p className="text-3xl font-bold text-purple-500">{userData?.stats?.win_rate || 0}%</p>
        </div>
      </motion.div>

      {/* Game Modes */}
      <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="card hover:shadow-2xl transition-all cursor-pointer transform hover:-translate-y-2 bg-gradient-to-br from-dark-lighter to-dark-card hover:border-primary/50 border border-white/5"
          onClick={() => navigate('/game-mode')}
        >
          <div className="text-center">
            <div className="text-6xl mb-4">🤖</div>
            <h2 className="text-2xl font-bold text-white mb-2">
              Play vs Computer
            </h2>
            <p className="text-gray-400 mb-4">
              Practice your skills against AI
            </p>
            <button className="btn-primary w-full">
              Start Game
            </button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card hover:shadow-2xl transition-all cursor-pointer transform hover:-translate-y-2 bg-gradient-to-bl from-dark-lighter to-dark-card hover:border-secondary/50 border border-white/5"
          onClick={() => navigate('/online')}
        >
          <div className="text-center">
            <div className="text-6xl mb-4">🌐</div>
            <h2 className="text-2xl font-bold text-white mb-2">
              Online Multiplayer
            </h2>
            <p className="text-gray-400 mb-4">
              Challenge real players online
            </p>
            <button className="btn-secondary w-full">
              Find Match
            </button>
          </div>
        </motion.div>
      </div>

      {/* Quick Links */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="mt-12 flex justify-center gap-4"
      >
        <button
          onClick={() => navigate('/leaderboard')}
          className="bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-lg transition backdrop-blur-sm"
        >
          View Leaderboard
        </button>
        <button
          onClick={() => navigate(`/profile/${userData?.firebase_uid}`)}
          className="bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-lg transition backdrop-blur-sm"
        >
          My Profile
        </button>
      </motion.div>
    </div>
  )
}

export default Home
