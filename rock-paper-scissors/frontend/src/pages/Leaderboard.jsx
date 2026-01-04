import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../config/api'

const Leaderboard = () => {
  const navigate = useNavigate()
  const [leaderboard, setLeaderboard] = useState([])
  const [filter, setFilter] = useState('all_time')
  const [sortBy, setSortBy] = useState('win_rate')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLeaderboard()
  }, [filter, sortBy])

  const fetchLeaderboard = async () => {
    try {
      setLoading(true)
      const response = await api.get('/leaderboard', {
        params: {
          filter: filter,
          sort_by: sortBy,
          limit: 30
        }
      })
      setLeaderboard(response.data.leaderboard)
    } catch (error) {
      console.error('Error fetching leaderboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇'
    if (rank === 2) return '🥈'
    if (rank === 3) return '🥉'
    return `#${rank}`
  }

  const getRankColor = (rank) => {
    if (rank === 1) return 'from-yellow-400 to-yellow-600'
    if (rank === 2) return 'from-gray-300 to-gray-500'
    if (rank === 3) return 'from-orange-400 to-orange-600'
    return 'from-gray-200 to-gray-300'
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-5xl font-bold text-white mb-4">
          🏆 Leaderboard
        </h1>
        <p className="text-xl text-white/80">
          Top players from around the world
        </p>
      </motion.div>

      {/* Filters */}
      {/* Filters */}
      <div className="card mb-8">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Time Filter */}
          <div>
            <label className="block text-gray-300 font-semibold mb-3">
              Time Period
            </label>
            <div className="grid grid-cols-2 gap-2">
              {[
                { value: 'all_time', label: 'All Time' },
                { value: 'monthly', label: 'Monthly' },
                { value: 'weekly', label: 'Weekly' },
                { value: 'daily', label: 'Daily' }
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => setFilter(option.value)}
                  className={`px-4 py-2 rounded-lg font-semibold transition ${filter === option.value
                      ? 'bg-primary text-white'
                      : 'bg-white/10 text-gray-300 hover:bg-white/20'
                    }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          {/* Sort Filter */}
          <div>
            <label className="block text-gray-300 font-semibold mb-3">
              Sort By
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { value: 'win_rate', label: 'Win Rate' },
                { value: 'total_wins', label: 'Total Wins' },
                { value: 'total_games', label: 'Games Played' }
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => setSortBy(option.value)}
                  className={`px-4 py-2 rounded-lg font-semibold transition ${sortBy === option.value
                      ? 'bg-secondary text-white'
                      : 'bg-white/10 text-gray-300 hover:bg-white/20'
                    }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Leaderboard */}
      {loading ? (
        <div className="card text-center py-12">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading leaderboard...</p>
        </div>
      ) : leaderboard.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-400 text-xl">No players found</p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Top 3 */}
          {leaderboard.slice(0, 3).map((player, index) => (
            <motion.div
              key={player.user_id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => navigate(`/profile/${player.user_id}`)}
              className="card hover:shadow-2xl transition-all cursor-pointer border border-white/10"
            >
              <div className="flex items-center gap-6">
                {/* Rank */}
                <div className={`w-20 h-20 rounded-full bg-gradient-to-br ${getRankColor(player.rank)} flex items-center justify-center text-3xl font-bold text-white shadow-lg`}>
                  {getMedalEmoji(player.rank)}
                </div>

                {/* Player Info */}
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-white">
                    {player.display_name || player.username}
                  </h3>
                  <p className="text-gray-400">@{player.username}</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-8 text-center">
                  <div>
                    <p className="text-sm text-gray-400">Win Rate</p>
                    <p className="text-2xl font-bold text-purple-500">
                      {player.win_rate}%
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Wins</p>
                    <p className="text-2xl font-bold text-green-500">
                      {player.total_wins}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Games</p>
                    <p className="text-2xl font-bold text-primary">
                      {player.total_games}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}

          {/* Rest of the players */}
          {leaderboard.slice(3).map((player, index) => (
            <motion.div
              key={player.user_id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: (index + 3) * 0.05 }}
              onClick={() => navigate(`/profile/${player.user_id}`)}
              className="card hover:shadow-lg transition-all cursor-pointer border border-white/5 bg-white/5 backdrop-blur-sm"
            >
              <div className="flex items-center gap-6">
                {/* Rank */}
                <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center text-xl font-bold text-white/80">
                  #{player.rank}
                </div>

                {/* Player Info */}
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-white">
                    {player.display_name || player.username}
                  </h3>
                  <p className="text-gray-400 text-sm">@{player.username}</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-6 text-center">
                  <div>
                    <p className="text-xs text-gray-400">Win Rate</p>
                    <p className="text-lg font-bold text-purple-400">
                      {player.win_rate}%
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400">Wins</p>
                    <p className="text-lg font-bold text-green-400">
                      {player.total_wins}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400">Games</p>
                    <p className="text-lg font-bold text-primary-glow">
                      {player.total_games}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Back Button */}
      <div className="mt-8 text-center">
        <button
          onClick={() => navigate('/')}
          className="text-white hover:text-gray-200 inline-flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </button>
      </div>
    </div>
  )
}

export default Leaderboard
