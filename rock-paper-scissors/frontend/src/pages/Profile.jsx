import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import { useGame } from '../context/GameContext'
import api from '../config/api'

const StatsCard = ({ title, value, color }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="card text-center hover:bg-white/5 transition-colors"
  >
    <p className="text-gray-400 text-sm mb-2 uppercase tracking-wide">{title}</p>
    <p className={`text-4xl font-bold ${color}`}>
      {value}
    </p>
  </motion.div>
)

const MiniStat = ({ title, value, color = 'text-white' }) => (
  <div>
    <p className="text-gray-400 text-xs uppercase">{title}</p>
    <p className={`text-2xl font-bold ${color}`}>
      {value || 0}
    </p>
  </div>
)

const Profile = () => {
  const { userId } = useParams()
  const navigate = useNavigate()
  const { user, userData } = useAuth()
  const { getGameHistory } = useGame()

  const [profile, setProfile] = useState(null)
  const [stats, setStats] = useState(null)
  const [gameHistory, setGameHistory] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('stats')

  const isOwnProfile = !userId || userId === user?.uid

  useEffect(() => {
    fetchProfile()
    fetchStats()
    if (isOwnProfile) {
      fetchGameHistory()
    }
  }, [userId, filter])

  const fetchProfile = async () => {
    try {
      const response = await api.get('/user/profile', {
        params: { user_id: userId || user?.uid }
      })
      setProfile(response.data.user)
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await api.get('/user/stats', {
        params: {
          user_id: userId || user?.uid,
          filter: filter
        }
      })
      setStats(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching stats:', error)
      setLoading(false)
    }
  }

  const fetchGameHistory = async () => {
    try {
      const response = await getGameHistory(1, 10)
      setGameHistory(response.games)
      setGameHistory(response.games)
    } catch (error) {
      console.error('Error fetching game history:', error)
    }
  }

  const handlePhotoUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    // Convert to base64 for simplicity in this demo
    const reader = new FileReader()
    reader.onloadend = async () => {
      const base64String = reader.result
      try {
        // Optimistic update
        setProfile(prev => ({ ...prev, profile_picture: base64String }))

        // Send to backend (Assuming endpoint exists or I'll add it)
        await api.put('/user/profile/photo', { photo: base64String })
      } catch (error) {
        console.error('Error uploading photo:', error)
      }
    }
    reader.readAsDataURL(file)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
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
        className="card mb-8 relative overflow-hidden group"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-secondary/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center gap-8">
            <div className="relative">
              <div className="w-28 h-28 rounded-full border-4 border-white/20 overflow-hidden shadow-2xl relative">
                {profile?.profile_picture ? (
                  <img src={profile.profile_picture} alt="Profile" className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-5xl text-white font-bold">
                    {profile?.username?.charAt(0).toUpperCase()}
                  </div>
                )}

                {isOwnProfile && (
                  <label className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 hover:opacity-100 cursor-pointer transition-opacity duration-300">
                    <span className="text-white text-xs font-bold uppercase tracking-wider">Change</span>
                    <input type="file" className="hidden" accept="image/*" onChange={handlePhotoUpload} />
                  </label>
                )}
              </div>
              <div className="absolute bottom-0 right-0 w-6 h-6 bg-green-500 rounded-full border-4 border-dark-card"></div>
            </div>

            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                {profile?.display_name || profile?.username}
              </h1>
              <p className="text-primary-glow font-medium text-lg">@{profile?.username}</p>
              {profile?.bio && (
                <p className="text-gray-300 mt-4 max-w-lg leading-relaxed">{profile.bio}</p>
              )}
            </div>
          </div>

          {isOwnProfile && (
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/settings')}
                className="btn-outline"
              >
                Edit Profile
              </button>
              <button
                onClick={async () => {
                  try {
                    await useAuth().logout()
                    navigate('/login')
                  } catch (error) {
                    console.error('Logout error:', error)
                  }
                }}
                className="btn-outline border-red-500/50 text-red-400 hover:bg-red-500/10 hover:border-red-500"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="card mb-8 p-1">
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('stats')}
            className={`flex-1 py-3 rounded-xl font-semibold transition-all duration-300 ${activeTab === 'stats'
              ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-lg'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
          >
            Statistics
          </button>
          {isOwnProfile && (
            <button
              onClick={() => setActiveTab('history')}
              className={`flex-1 py-3 rounded-xl font-semibold transition-all duration-300 ${activeTab === 'history'
                ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-lg'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
            >
              Game History
            </button>
          )}
        </div>
      </div>

      {/* Statistics Tab */}
      {activeTab === 'stats' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {/* Stats Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatsCard title="Total Games" value={stats?.filtered_stats?.total_games || profile?.stats?.total_games || 0} color="text-white" />
            <StatsCard title="Wins" value={stats?.filtered_stats?.wins || profile?.stats?.wins || 0} color="text-green-400" />
            <StatsCard title="Losses" value={stats?.filtered_stats?.losses || profile?.stats?.losses || 0} color="text-red-400" />
            <StatsCard title="Win Rate" value={`${stats?.filtered_stats?.win_rate || profile?.stats?.win_rate || 0}%`} color="text-neon-pink" />
          </div>

          {/* Overall Stats */}
          {filter !== 'all' && (
            <div className="card">
              <h3 className="text-xl font-bold text-white mb-4">Overall Statistics</h3>
              <div className="grid grid-cols-4 gap-4">
                <MiniStat title="Total" value={stats?.overall_stats?.total_games} />
                <MiniStat title="Wins" value={stats?.overall_stats?.wins} color="text-green-400" />
                <MiniStat title="Losses" value={stats?.overall_stats?.losses} color="text-red-400" />
                <MiniStat title="Win Rate" value={`${stats?.overall_stats?.win_rate}%`} color="text-neon-pink" />
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Game History Tab */}
      {activeTab === 'history' && isOwnProfile && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-white mb-6">Recent Games</h3>
          {gameHistory.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No games played yet</p>
          ) : (
            <div className="space-y-4">
              {gameHistory.map((game) => (
                <div
                  key={game.game_id}
                  className="border border-white/10 rounded-lg p-4 hover:bg-white/5 transition bg-white/5"
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-white">
                        {game.mode.replace('_', ' ').toUpperCase()}
                      </p>
                      <p className="text-sm text-gray-400">
                        vs {game.opponent_type === 'computer' ? 'Computer' : 'Player'}
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold text-white">
                        {game.scores.player1} - {game.scores.player2}
                      </p>
                      <p className={`text-sm font-semibold ${game.scores.player1 > game.scores.player2 ? 'text-green-400' :
                        game.scores.player1 < game.scores.player2 ? 'text-red-400' :
                          'text-yellow-400'
                        }`}>
                        {game.scores.player1 > game.scores.player2 ? 'Won' :
                          game.scores.player1 < game.scores.player2 ? 'Lost' :
                            'Tied'}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-400">
                        {formatDate(game.created_at)}
                      </p>
                      <p className="text-xs text-gray-500">
                        {game.rounds.length} rounds
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
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



export default Profile
