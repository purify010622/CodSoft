import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

const GameMode = () => {
  const navigate = useNavigate()

  const gameModes = [
    {
      id: 'quick_play',
      title: 'Quick Play',
      description: 'Single round - Fast and simple',
      icon: '⚡',
      color: 'from-yellow-400 to-orange-500'
    },
    {
      id: 'best_of_3',
      title: 'Best of 3',
      description: 'First to 2 wins',
      icon: '🥉',
      color: 'from-blue-400 to-blue-600'
    },
    {
      id: 'best_of_5',
      title: 'Best of 5',
      description: 'First to 3 wins',
      icon: '🥈',
      color: 'from-purple-400 to-purple-600'
    },
    {
      id: 'best_of_7',
      title: 'Best of 7',
      description: 'First to 4 wins',
      icon: '🥇',
      color: 'from-pink-400 to-red-500'
    },
    {
      id: 'endless',
      title: 'Endless Mode',
      description: 'Play until you quit',
      icon: '♾️',
      color: 'from-green-400 to-teal-500'
    }
  ]

  return (
    <div className="container mx-auto px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <button
          onClick={() => navigate('/')}
          className="text-white hover:text-gray-200 mb-4 inline-flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </button>
        <h1 className="text-5xl font-bold text-white mb-4">
          Choose Game Mode
        </h1>
        <p className="text-xl text-white/80">
          Select your preferred game mode to play against the computer
        </p>
      </motion.div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {gameModes.map((mode, index) => (
          <motion.div
            key={mode.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => navigate(`/game/${mode.id}`)}
            className="card hover:shadow-2xl transition-all cursor-pointer transform hover:-translate-y-2 group"
          >
            <div className={`w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br ${mode.color} flex items-center justify-center text-4xl group-hover:scale-110 transition-transform`}>
              {mode.icon}
            </div>
            <h2 className="text-2xl font-bold text-white mb-2 text-center">
              {mode.title}
            </h2>
            <p className="text-gray-400 text-center mb-4">
              {mode.description}
            </p>
            <button className="btn-primary w-full">
              Play Now
            </button>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="text-center mt-12"
      >
        <div className="card max-w-2xl mx-auto bg-white/10 backdrop-blur-md border border-white/20">
          <h3 className="text-2xl font-bold text-white mb-4">Game Rules</h3>
          <div className="text-white/90 space-y-2">
            <p>✊ Rock beats Scissors</p>
            <p>✋ Paper beats Rock</p>
            <p>✌️ Scissors beats Paper</p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default GameMode
