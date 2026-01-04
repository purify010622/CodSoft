import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { io } from 'socket.io-client'
import { useAuth } from '../context/AuthContext'

const OnlineGame = () => {
  const navigate = useNavigate()
  const { user, userData } = useAuth()

  const [socket, setSocket] = useState(null)
  const [gameState, setGameState] = useState('menu') // menu, searching, playing, result
  const [gameData, setGameData] = useState(null)
  const [playerMove, setPlayerMove] = useState(null)
  const [opponentMove, setOpponentMove] = useState(null)
  const [roundResult, setRoundResult] = useState(null)
  const [waitingForOpponent, setWaitingForOpponent] = useState(false)

  const moves = [
    { id: 'rock', emoji: '✊', name: 'Rock', color: 'bg-red-500' },
    { id: 'paper', emoji: '✋', name: 'Paper', color: 'bg-blue-500' },
    { id: 'scissors', emoji: '✌️', name: 'Scissors', color: 'bg-green-500' }
  ]

  useEffect(() => {
    // Check if user is guest
    if (user?.isGuest) {
      alert('Online multiplayer is only available for registered users')
      navigate('/')
      return
    }

    // Initialize Socket.IO
    const socketUrl = '/'
    const newSocket = io(socketUrl)

    newSocket.on('connected', (data) => {
      console.log('Connected to server:', data)
    })

    newSocket.on('waiting_for_opponent', (data) => {
      console.log('Waiting for opponent:', data)
    })

    newSocket.on('game_found', (data) => {
      console.log('Game found:', data)
      setGameData(data)
      setGameState('playing')
    })

    newSocket.on('move_submitted', (data) => {
      console.log('Move submitted:', data)
      setWaitingForOpponent(true)
    })

    newSocket.on('round_result', (data) => {
      console.log('Round result:', data)
      setOpponentMove(data.round_result.opponent_move)
      setRoundResult(data.round_result)
      setWaitingForOpponent(false)
      setGameState('result')

      // Check if game finished
      if (data.game_finished) {
        setTimeout(() => {
          setGameState('menu')
          setGameData(null)
        }, 5000)
      }
    })

    newSocket.on('opponent_disconnected', (data) => {
      alert('Opponent disconnected')
      setGameState('menu')
      setGameData(null)
    })

    newSocket.on('opponent_left', (data) => {
      alert('Opponent left the game')
      setGameState('menu')
      setGameData(null)
    })

    setSocket(newSocket)

    return () => {
      if (newSocket) {
        newSocket.disconnect()
      }
    }
  }, [user, navigate])

  const startMatchmaking = () => {
    if (socket) {
      socket.emit('join_matchmaking', {
        user_id: user.uid,
        username: userData?.username || 'Player',
        mode: 'quick_play'
      })
      setGameState('searching')
    }
  }

  const cancelMatchmaking = () => {
    if (socket) {
      socket.emit('cancel_matchmaking')
      setGameState('menu')
    }
  }

  const handleMove = (move) => {
    if (!socket || !gameData || waitingForOpponent) return

    setPlayerMove(move)
    socket.emit('submit_move', {
      game_id: gameData.game_id,
      user_id: user.uid,
      move: move
    })
  }

  const playAgain = () => {
    setPlayerMove(null)
    setOpponentMove(null)
    setRoundResult(null)
    setGameState('playing')
  }

  const leaveGame = () => {
    if (socket && gameData) {
      socket.emit('leave_game', {
        game_id: gameData.game_id,
        user_id: user.uid
      })
    }
    setGameState('menu')
    setGameData(null)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          Online Multiplayer
        </h1>
        <p className="text-white/80">
          Challenge real players in real-time
        </p>
      </div>

      <div className="max-w-4xl mx-auto">
        <AnimatePresence mode="wait">
          {/* Menu State */}
          {gameState === 'menu' && (
            <motion.div
              key="menu"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="card text-center"
            >
              <div className="text-6xl mb-6">🌐</div>
              <h2 className="text-3xl font-bold text-white mb-4">
                Ready to Play?
              </h2>
              <p className="text-gray-400 mb-8">
                Find an opponent and start playing
              </p>
              <button
                onClick={startMatchmaking}
                className="btn-primary text-xl px-12 py-4"
              >
                Find Match
              </button>
              <div className="mt-6">
                <button
                  onClick={() => navigate('/')}
                  className="text-gray-400 hover:text-white"
                >
                  Back to Home
                </button>
              </div>
            </motion.div>
          )}

          {/* Searching State */}
          {gameState === 'searching' && (
            <motion.div
              key="searching"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="card text-center"
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="text-6xl mb-6"
              >
                🔍
              </motion.div>
              <h2 className="text-3xl font-bold text-white mb-4">
                Searching for Opponent...
              </h2>
              <p className="text-gray-400 mb-8">
                Please wait while we find you a match
              </p>
              <div className="flex justify-center gap-2 mb-8">
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                  className="w-3 h-3 bg-primary rounded-full"
                />
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                  className="w-3 h-3 bg-primary rounded-full"
                />
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                  className="w-3 h-3 bg-primary rounded-full"
                />
              </div>
              <button
                onClick={cancelMatchmaking}
                className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition"
              >
                Cancel
              </button>
            </motion.div>
          )}

          {/* Playing State */}
          {gameState === 'playing' && (
            <motion.div
              key="playing"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="card"
            >
              {gameData && (
                <div className="text-center mb-6">
                  <p className="text-gray-400 mb-2">Playing against opponent</p>
                  <div className="text-xl font-bold text-white">
                    Score: {roundResult?.scores?.player1 || 0} - {roundResult?.scores?.player2 || 0}
                  </div>
                </div>
              )}

              {!playerMove ? (
                <>
                  <h2 className="text-2xl font-bold text-center mb-8 text-white">
                    Choose Your Move
                  </h2>
                  <div className="grid grid-cols-3 gap-6">
                    {moves.map((move) => (
                      <motion.button
                        key={move.id}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleMove(move.id)}
                        className={`${move.color} hover:opacity-90 text-white p-8 rounded-xl shadow-lg transition-all`}
                      >
                        <div className="text-6xl mb-4">{move.emoji}</div>
                        <div className="text-xl font-bold">{move.name}</div>
                      </motion.button>
                    ))}
                  </div>
                </>
              ) : (
                <div className="text-center">
                  <motion.div
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 1, repeat: Infinity }}
                    className="text-8xl mb-6"
                  >
                    {moves.find(m => m.id === playerMove)?.emoji}
                  </motion.div>
                  <h3 className="text-2xl font-bold text-white mb-4">
                    Waiting for opponent...
                  </h3>
                  <p className="text-gray-400">
                    Your move: {moves.find(m => m.id === playerMove)?.name}
                  </p>
                </div>
              )}

              <div className="mt-6 text-center">
                <button
                  onClick={leaveGame}
                  className="text-red-400 hover:text-red-300 font-semibold"
                >
                  Leave Game
                </button>
              </div>
            </motion.div>
          )}

          {/* Result State */}
          {gameState === 'result' && roundResult && (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="card"
            >
              <div className="text-center mb-8">
                <motion.h2
                  initial={{ y: -20 }}
                  animate={{ y: 0 }}
                  className={`text-4xl font-bold mb-4 ${roundResult.winner === 'player1' ? 'text-green-400' :
                    roundResult.winner === 'player2' ? 'text-red-400' :
                      'text-yellow-400'
                    }`}
                >
                  {roundResult.winner === 'player1' ? '🎉 You Win!' :
                    roundResult.winner === 'player2' ? '😢 You Lose!' :
                      '🤝 It\'s a Tie!'}
                </motion.h2>
              </div>

              <div className="grid grid-cols-2 gap-8 mb-8">
                <div className="text-center">
                  <p className="text-gray-400 mb-4 font-semibold">Your Move</p>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="text-8xl"
                  >
                    {moves.find(m => m.id === roundResult.your_move)?.emoji}
                  </motion.div>
                  <p className="text-xl font-bold text-white mt-4">
                    {moves.find(m => m.id === roundResult.your_move)?.name}
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-gray-400 mb-4 font-semibold">Opponent Move</p>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-8xl"
                  >
                    {moves.find(m => m.id === roundResult.opponent_move)?.emoji}
                  </motion.div>
                  <p className="text-xl font-bold text-white mt-4">
                    {moves.find(m => m.id === roundResult.opponent_move)?.name}
                  </p>
                </div>
              </div>

              <div className="text-center mb-6">
                <p className="text-xl font-bold text-white">
                  Score: {roundResult.scores.player1} - {roundResult.scores.player2}
                </p>
              </div>

              <div className="flex gap-4 justify-center">
                <button
                  onClick={playAgain}
                  className="btn-primary"
                >
                  Next Round
                </button>
                <button
                  onClick={leaveGame}
                  className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition"
                >
                  Leave Game
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default OnlineGame
