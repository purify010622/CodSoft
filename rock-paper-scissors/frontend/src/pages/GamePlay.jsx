import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useGame } from '../context/GameContext'
import { useAuth } from '../context/AuthContext'

const GamePlay = () => {
  const { mode } = useParams()
  const navigate = useNavigate()
  const { createGame, makeMove, currentGame } = useGame()
  const { user } = useAuth()

  const [playerMove, setPlayerMove] = useState(null)
  const [computerMove, setComputerMove] = useState(null)
  const [result, setResult] = useState(null)
  const [showResult, setShowResult] = useState(false)
  const [gameStarted, setGameStarted] = useState(false)
  const [loading, setLoading] = useState(false)

  const moves = [
    { id: 'rock', emoji: '✊', name: 'Rock', color: 'bg-red-500' },
    { id: 'paper', emoji: '✋', name: 'Paper', color: 'bg-blue-500' },
    { id: 'scissors', emoji: '✌️', name: 'Scissors', color: 'bg-green-500' }
  ]

  const modeNames = {
    quick_play: 'Quick Play',
    best_of_3: 'Best of 3',
    best_of_5: 'Best of 5',
    best_of_7: 'Best of 7',
    endless: 'Endless Mode'
  }

  useEffect(() => {
    startNewGame()
  }, [])

  const startNewGame = async () => {
    try {
      if (user?.isGuest) {
        // Guest mode - local game only
        setGameStarted(true)
      } else {
        await createGame(mode, 'computer')
        setGameStarted(true)
      }
    } catch (error) {
      console.error('Error starting game:', error)
    }
  }

  const handleMove = async (move) => {
    if (loading || showResult) return

    setLoading(true)
    setPlayerMove(move)

    // Simulate thinking
    await new Promise(resolve => setTimeout(resolve, 500))

    try {
      if (user?.isGuest) {
        // Guest mode - local game logic
        const computerChoice = moves[Math.floor(Math.random() * moves.length)].id
        setComputerMove(computerChoice)

        const winner = determineWinner(move, computerChoice)
        setResult(winner)
        setShowResult(true)
      } else {
        // Registered user - API call
        const response = await makeMove(currentGame.game_id, move)
        setComputerMove(response.round_result.player2_move)
        setResult(response.round_result.winner === 'player1' ? 'win' :
          response.round_result.winner === 'player2' ? 'lose' : 'tie')
        setShowResult(true)
      }
    } catch (error) {
      console.error('Error making move:', error)
    } finally {
      setLoading(false)
    }
  }

  const determineWinner = (player, computer) => {
    if (player === computer) return 'tie'
    if (
      (player === 'rock' && computer === 'scissors') ||
      (player === 'paper' && computer === 'rock') ||
      (player === 'scissors' && computer === 'paper')
    ) {
      return 'win'
    }
    return 'lose'
  }

  const playAgain = () => {
    setPlayerMove(null)
    setComputerMove(null)
    setResult(null)
    setShowResult(false)

    // Check if game should end
    if (currentGame?.status === 'finished') {
      navigate('/game-mode')
    }
  }

  const quitGame = () => {
    navigate('/game-mode')
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          {modeNames[mode]}
        </h1>
        {currentGame && (
          <div className="text-white/80 text-lg">
            Score: You {currentGame.scores.player1} - {currentGame.scores.player2} Computer
          </div>
        )}
      </div>

      {/* Game Area */}
      <div className="max-w-4xl mx-auto">
        <AnimatePresence mode="wait">
          {!showResult ? (
            <motion.div
              key="selection"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="card"
            >
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
                    disabled={loading}
                    className={`${move.color} hover:opacity-90 text-white p-8 rounded-xl shadow-lg transition-all disabled:opacity-50`}
                  >
                    <div className="text-6xl mb-4">{move.emoji}</div>
                    <div className="text-xl font-bold">{move.name}</div>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="card"
            >
              {/* Result Display */}
              <div className="text-center mb-8">
                <motion.h2
                  initial={{ y: -20 }}
                  animate={{ y: 0 }}
                  className={`text-4xl font-bold mb-4 ${result === 'win' ? 'text-green-400' :
                      result === 'lose' ? 'text-red-400' :
                        'text-yellow-400'
                    }`}
                >
                  {result === 'win' ? '🎉 You Win!' :
                    result === 'lose' ? '😢 You Lose!' :
                      '🤝 It\'s a Tie!'}
                </motion.h2>
              </div>

              {/* Moves Display */}
              <div className="grid grid-cols-2 gap-8 mb-8">
                <div className="text-center">
                  <p className="text-gray-400 mb-4 font-semibold">Your Move</p>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="text-8xl"
                  >
                    {moves.find(m => m.id === playerMove)?.emoji}
                  </motion.div>
                  <p className="text-xl font-bold text-white mt-4">
                    {moves.find(m => m.id === playerMove)?.name}
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-gray-400 mb-4 font-semibold">Computer Move</p>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-8xl"
                  >
                    {moves.find(m => m.id === computerMove)?.emoji}
                  </motion.div>
                  <p className="text-xl font-bold text-white mt-4">
                    {moves.find(m => m.id === computerMove)?.name}
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4 justify-center">
                <button
                  onClick={playAgain}
                  className="btn-primary"
                >
                  {currentGame?.status === 'finished' ? 'New Game' : 'Next Round'}
                </button>
                <button
                  onClick={quitGame}
                  className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition"
                >
                  Quit Game
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Game Info */}
      <div className="mt-8 text-center">
        <button
          onClick={() => navigate('/game-mode')}
          className="text-white hover:text-gray-200 inline-flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Game Modes
        </button>
      </div>
    </div>
  )
}

export default GamePlay
