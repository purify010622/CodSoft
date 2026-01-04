import { createContext, useContext, useState } from 'react'
import api from '../config/api'

const GameContext = createContext({})

export const useGame = () => useContext(GameContext)

export const GameProvider = ({ children }) => {
  const [currentGame, setCurrentGame] = useState(null)
  const [gameHistory, setGameHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const createGame = async (mode, opponentType = 'computer') => {
    try {
      setLoading(true)
      const response = await api.post('/game/create', {
        mode,
        opponent_type: opponentType
      })
      setCurrentGame(response.data.game)
      return response.data.game
    } catch (error) {
      console.error('Error creating game:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const makeMove = async (gameId, move) => {
    try {
      const response = await api.post('/game/move', {
        game_id: gameId,
        move
      })
      setCurrentGame(response.data.game)
      return response.data
    } catch (error) {
      console.error('Error making move:', error)
      throw error
    }
  }

  const getGame = async (gameId) => {
    try {
      const response = await api.get(`/game/${gameId}`)
      return response.data.game
    } catch (error) {
      console.error('Error fetching game:', error)
      throw error
    }
  }

  const getGameHistory = async (page = 1, limit = 20) => {
    try {
      const response = await api.get('/game/history', {
        params: { page, limit }
      })
      setGameHistory(response.data.games)
      return response.data
    } catch (error) {
      console.error('Error fetching game history:', error)
      throw error
    }
  }

  const endGame = () => {
    setCurrentGame(null)
  }

  const value = {
    currentGame,
    gameHistory,
    loading,
    createGame,
    makeMove,
    getGame,
    getGameHistory,
    endGame
  }

  return (
    <GameContext.Provider value={value}>
      {children}
    </GameContext.Provider>
  )
}
