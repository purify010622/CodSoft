import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../config/api'

const AdminDashboard = () => {
  const navigate = useNavigate()

  const [activeTab, setActiveTab] = useState('analytics')
  const [analytics, setAnalytics] = useState(null)
  const [users, setUsers] = useState([])
  const [games, setGames] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  useEffect(() => {
    fetchAnalytics()
  }, [])

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers()
    } else if (activeTab === 'games') {
      fetchGames()
    }
  }, [activeTab, searchTerm, statusFilter])

  const fetchAnalytics = async () => {
    try {
      const response = await api.get('/admin/analytics')
      setAnalytics(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching analytics:', error)
      if (error.response?.status === 403) {
        alert('Admin access required')
        navigate('/')
      }
      setLoading(false)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await api.get('/admin/users', {
        params: {
          search: searchTerm,
          status: statusFilter,
          page: 1,
          limit: 50
        }
      })
      setUsers(response.data.users)
    } catch (error) {
      console.error('Error fetching users:', error)
    }
  }

  const fetchGames = async () => {
    try {
      const response = await api.get('/admin/games', {
        params: {
          status: statusFilter,
          page: 1,
          limit: 50
        }
      })
      setGames(response.data.games)
    } catch (error) {
      console.error('Error fetching games:', error)
    }
  }

  const handleBanUser = async (userId) => {
    const reason = prompt('Enter ban reason:')
    if (!reason) return

    try {
      await api.put(`/admin/user/${userId}/ban`, { reason })
      alert('User banned successfully')
      fetchUsers()
    } catch (error) {
      alert('Failed to ban user')
    }
  }

  const handleUnbanUser = async (userId) => {
    try {
      await api.put(`/admin/user/${userId}/unban`)
      alert('User unbanned successfully')
      fetchUsers()
    } catch (error) {
      alert('Failed to unban user')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-white"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-white mb-2">
          🛡️ Admin Dashboard
        </h1>
        <p className="text-white/80">
          System management and monitoring
        </p>
      </motion.div>

      {/* Tabs */}
      <div className="card mb-8">
        <div className="flex gap-4 border-b border-white/10">
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-6 py-3 font-semibold transition ${activeTab === 'analytics'
                ? 'text-primary border-b-2 border-primary'
                : 'text-gray-400 hover:text-white'
              }`}
          >
            Analytics
          </button>
          <button
            onClick={() => setActiveTab('users')}
            className={`px-6 py-3 font-semibold transition ${activeTab === 'users'
                ? 'text-primary border-b-2 border-primary'
                : 'text-gray-400 hover:text-white'
              }`}
          >
            Users
          </button>
          <button
            onClick={() => setActiveTab('games')}
            className={`px-6 py-3 font-semibold transition ${activeTab === 'games'
                ? 'text-primary border-b-2 border-primary'
                : 'text-gray-400 hover:text-white'
              }`}
          >
            Games
          </button>
        </div>
      </div>

      {/* Analytics Tab */}
      {activeTab === 'analytics' && analytics && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {/* User Stats */}
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">User Statistics</h2>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <p className="text-gray-400 mb-2">Total Users</p>
                <p className="text-4xl font-bold text-primary">{analytics.users.total}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 mb-2">Active Users</p>
                <p className="text-4xl font-bold text-green-600">{analytics.users.active}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 mb-2">Banned Users</p>
                <p className="text-4xl font-bold text-red-600">{analytics.users.banned}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 mb-2">New Today</p>
                <p className="text-4xl font-bold text-purple-600">{analytics.users.new_today}</p>
              </div>
            </div>
          </div>

          {/* Game Stats */}
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">Game Statistics</h2>
            <div className="grid md:grid-cols-4 gap-6 mb-6">
              <div className="text-center">
                <p className="text-gray-400 mb-2">Total Games</p>
                <p className="text-4xl font-bold text-primary">{analytics.games.total}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 mb-2">Active Games</p>
                <p className="text-4xl font-bold text-green-600">{analytics.games.active}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 mb-2">Finished Games</p>
                <p className="text-4xl font-bold text-blue-600">{analytics.games.finished}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 mb-2">Games Today</p>
                <p className="text-4xl font-bold text-purple-600">{analytics.games.today}</p>
              </div>
            </div>

            <h3 className="text-xl font-bold text-white mb-4">Games by Mode</h3>
            <div className="grid md:grid-cols-5 gap-4">
              {Object.entries(analytics.games.by_mode).map(([mode, count]) => (
                <div key={mode} className="bg-white/10 p-4 rounded-lg text-center">
                  <p className="text-sm text-gray-300 mb-1">
                    {mode.replace('_', ' ').toUpperCase()}
                  </p>
                  <p className="text-2xl font-bold text-white">{count}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Top Players */}
          <div className="card">
            <h2 className="text-2xl font-bold text-white mb-6">Top Players</h2>
            <div className="space-y-4">
              {analytics.top_players.map((player, index) => (
                <div key={player.user_id} className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div className="flex items-center gap-4">
                    <span className="text-2xl font-bold text-gray-400">#{index + 1}</span>
                    <div>
                      <p className="font-bold text-white">{player.username}</p>
                      <p className="text-sm text-gray-400">
                        {player.total_games} games played
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-primary">{player.win_rate}%</p>
                    <p className="text-sm text-gray-400">{player.total_wins} wins</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {/* Filters */}
          <div className="card mb-6">
            <div className="grid md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Search by username or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field"
              />
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="input-field"
              >
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="banned">Banned</option>
                <option value="suspended">Suspended</option>
              </select>
            </div>
          </div>

          {/* Users List */}
          <div className="card">
            <h2 className="text-2xl font-bold text-white mb-6">
              Users ({users.length})
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/10 text-gray-300">
                    <th className="text-left py-3 px-4">Username</th>
                    <th className="text-left py-3 px-4">Email</th>
                    <th className="text-left py-3 px-4">Status</th>
                    <th className="text-left py-3 px-4">Games</th>
                    <th className="text-left py-3 px-4">Win Rate</th>
                    <th className="text-left py-3 px-4">Actions</th>
                  </tr>
                </thead>
                <tbody className="text-gray-300">
                  {users.map((user) => (
                    <tr key={user.firebase_uid} className="border-b border-white/10 hover:bg-white/5">
                      <td className="py-3 px-4 font-semibold text-white">{user.username}</td>
                      <td className="py-3 px-4 text-gray-400">{user.email}</td>
                      <td className="py-3 px-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${user.status === 'active' ? 'bg-green-500/20 text-green-400' :
                            user.status === 'banned' ? 'bg-red-500/20 text-red-400' :
                              'bg-yellow-500/20 text-yellow-400'
                          }`}>
                          {user.status}
                        </span>
                      </td>
                      <td className="py-3 px-4">{user.stats.total_games}</td>
                      <td className="py-3 px-4">{user.stats.win_rate}%</td>
                      <td className="py-3 px-4">
                        {user.status === 'active' ? (
                          <button
                            onClick={() => handleBanUser(user.firebase_uid)}
                            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
                          >
                            Ban
                          </button>
                        ) : (
                          <button
                            onClick={() => handleUnbanUser(user.firebase_uid)}
                            className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm"
                          >
                            Unban
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>
      )}

      {/* Games Tab */}
      {activeTab === 'games' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {/* Filter */}
          <div className="card mb-6">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input-field"
            >
              <option value="">All Games</option>
              <option value="active">Active</option>
              <option value="finished">Finished</option>
              <option value="abandoned">Abandoned</option>
            </select>
          </div>

          {/* Games List */}
          <div className="card">
            <h2 className="text-2xl font-bold text-white mb-6">
              Games ({games.length})
            </h2>
            <div className="space-y-4">
              {games.map((game) => (
                <div key={game.game_id} className="border border-white/10 rounded-lg p-4 bg-white/5">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-bold text-white">
                        {game.mode.replace('_', ' ').toUpperCase()}
                      </p>
                      <p className="text-sm text-gray-400">
                        {game.opponent_type === 'computer' ? 'vs Computer' : 'vs Player'}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        Game ID: {game.game_id}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${game.status === 'active' ? 'bg-blue-500/20 text-blue-400' :
                          game.status === 'finished' ? 'bg-green-500/20 text-green-400' :
                            'bg-gray-500/20 text-gray-400'
                        }`}>
                        {game.status}
                      </span>
                      <p className="text-sm text-white mt-2">
                        Score: {game.scores.player1} - {game.scores.player2}
                      </p>
                      <p className="text-xs text-gray-500">
                        {game.rounds.length} rounds
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
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

export default AdminDashboard
