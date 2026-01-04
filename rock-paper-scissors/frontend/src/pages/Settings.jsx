import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import { updatePassword } from 'firebase/auth'
import { auth } from '../config/firebase'
import api from '../config/api'

const Settings = () => {
  const navigate = useNavigate()
  const { user, userData } = useAuth()

  const [activeTab, setActiveTab] = useState('profile')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  // Profile form
  const [profileForm, setProfileForm] = useState({
    username: '',
    display_name: '',
    bio: '',
    profile_picture: ''
  })

  // Password form
  const [passwordForm, setPasswordForm] = useState({
    newPassword: '',
    confirmPassword: ''
  })

  /* Game Settings State */
  const [gameSettings, setGameSettings] = useState({
    masterVolume: 80,
    sfxVolume: 100,
    musicVolume: 60,
    particles: true,
    highContrast: false
  })

  useEffect(() => {
    // Load settings from local storage
    const savedSettings = localStorage.getItem('rps_game_settings')
    if (savedSettings) {
      setGameSettings(JSON.parse(savedSettings))
    }

    // Load profile data
    if (userData) {
      setProfileForm({
        username: userData.username || '',
        display_name: userData.display_name || '',
        bio: userData.bio || '',
        profile_picture: userData.profile_picture || ''
      })
    }
  }, [userData])

  const handleGameSettingChange = (key, value) => {
    const newSettings = { ...gameSettings, [key]: value }
    setGameSettings(newSettings)
    localStorage.setItem('rps_game_settings', JSON.stringify(newSettings))
    // In a real app, we'd apply these changes immediately (e.g. update audio context)
  }

  const handleProfileChange = (e) => {
    setProfileForm({
      ...profileForm,
      [e.target.name]: e.target.value
    })
  }

  const handlePasswordChange = (e) => {
    setPasswordForm({
      ...passwordForm,
      [e.target.name]: e.target.value
    })
  }

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      await api.put('/user/profile', profileForm)
      setMessage({ type: 'success', text: 'Profile updated successfully!' })
      // Delay navigation slightly to show success message
      setTimeout(() => {
        // Optional: navigate away or just stay
      }, 1000)

    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to update profile'
      })
    } finally {
      setLoading(false)
    }
  }

  const handlePasswordSubmit = async (e) => {
    e.preventDefault()
    setMessage({ type: '', text: '' })

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setMessage({ type: 'error', text: 'Passwords do not match' })
      return
    }

    if (passwordForm.newPassword.length < 6) {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters' })
      return
    }

    setLoading(true)

    try {
      await updatePassword(auth.currentUser, passwordForm.newPassword)
      setMessage({ type: 'success', text: 'Password updated successfully!' })
      setPasswordForm({ newPassword: '', confirmPassword: '' })
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.message || 'Failed to update password'
      })
    } finally {
      setLoading(false)
    }
  }

  const TabButton = ({ id, label }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`px-6 py-3 font-semibold transition-all duration-300 rounded-lg ${activeTab === id
          ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-lg scale-105'
          : 'text-gray-400 hover:text-white hover:bg-white/5'
        }`}
    >
      {label}
    </button>
  )

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-neon-blue via-primary-glow to-neon-pink drop-shadow-lg">
          Settings
        </h1>
        <p className="text-gray-400 text-lg">
          Customize your experience
        </p>
      </motion.div>

      <div className="max-w-4xl mx-auto">
        {/* Tabs */}
        <div className="card mb-8 p-2">
          <div className="flex flex-wrap gap-2 justify-center">
            <TabButton id="profile" label="Profile" />
            {!user?.isGuest && <TabButton id="password" label="Security" />}
            <TabButton id="game" label="Game Settings" />
          </div>
        </div>

        {/* Message */}
        {message.text && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`card mb-6 border-l-4 ${message.type === 'success'
                ? 'bg-green-500/10 border-green-500 text-green-400'
                : 'bg-red-500/10 border-red-500 text-red-400'
              }`}
          >
            <p className="font-semibold">{message.text}</p>
          </motion.div>
        )}

        {/* Profile Settings Tab */}
        {activeTab === 'profile' && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">
              Profile Information
            </h2>
            <form onSubmit={handleProfileSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-gray-300 font-medium mb-2">Username</label>
                  <input
                    type="text"
                    name="username"
                    value={profileForm.username}
                    onChange={handleProfileChange}
                    className="input-field"
                    placeholder="Username"
                    disabled
                  />
                  <p className="text-xs text-gray-500 mt-2">Username cannot be changed</p>
                </div>
                <div>
                  <label className="block text-gray-300 font-medium mb-2">Display Name</label>
                  <input
                    type="text"
                    name="display_name"
                    value={profileForm.display_name}
                    onChange={handleProfileChange}
                    className="input-field"
                    placeholder="Display Name"
                  />
                </div>
              </div>

              <div>
                <label className="block text-gray-300 font-medium mb-2">Bio</label>
                <textarea
                  name="bio"
                  value={profileForm.bio}
                  onChange={handleProfileChange}
                  className="input-field min-h-[120px]"
                  placeholder="Tell us about yourself..."
                />
              </div>

              <div>
                <label className="block text-gray-300 font-medium mb-2">
                  Profile Picture URL
                </label>
                <input
                  type="url"
                  name="profile_picture"
                  value={profileForm.profile_picture}
                  onChange={handleProfileChange}
                  className="input-field"
                  placeholder="https://example.com/image.jpg"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Enter a URL to your profile picture
                </p>
              </div>

              <div className="flex justify-end gap-4 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </motion.div>
        )}

        {/* Password Tab */}
        {activeTab === 'password' && !user?.isGuest && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">
              Security Settings
            </h2>
            <form onSubmit={handlePasswordSubmit} className="space-y-6 max-w-md mx-auto">
              <div>
                <label className="block text-gray-300 font-medium mb-2">New Password</label>
                <input
                  type="password"
                  name="newPassword"
                  value={passwordForm.newPassword}
                  onChange={handlePasswordChange}
                  className="input-field"
                  placeholder="Min. 6 characters"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 font-medium mb-2">Confirm Password</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={passwordForm.confirmPassword}
                  onChange={handlePasswordChange}
                  className="input-field"
                  placeholder="Retype password"
                  required
                />
              </div>

              <div className="flex justify-end pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary w-full"
                >
                  {loading ? 'Updating...' : 'Update Password'}
                </button>
              </div>
            </form>
          </motion.div>
        )}

        {/* Game Settings Tab */}
        {activeTab === 'game' && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <div className="card">
              <h2 className="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">
                Audio Settings
              </h2>
              <div className="space-y-8">
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-gray-300 font-medium">Master Volume</label>
                    <span className="text-primary font-bold">{gameSettings.masterVolume}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={gameSettings.masterVolume}
                    onChange={(e) => handleGameSettingChange('masterVolume', parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-gray-300 font-medium">Music Volume</label>
                    <span className="text-secondary font-bold">{gameSettings.musicVolume}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={gameSettings.musicVolume}
                    onChange={(e) => handleGameSettingChange('musicVolume', parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-secondary"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-gray-300 font-medium">SFX Volume</label>
                    <span className="text-neon-blue font-bold">{gameSettings.sfxVolume}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={gameSettings.sfxVolume}
                    onChange={(e) => handleGameSettingChange('sfxVolume', parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-neon-blue"
                  />
                </div>
              </div>
            </div>

            <div className="card">
              <h2 className="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">
                Graphics & Gameplay
              </h2>
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                  <div>
                    <h3 className="text-white font-bold">Particle Effects</h3>
                    <p className="text-sm text-gray-400">Enable fancy particle animations during gameplay</p>
                  </div>
                  <button
                    onClick={() => handleGameSettingChange('particles', !gameSettings.particles)}
                    className={`w-14 h-8 rounded-full p-1 transition-colors duration-300 ${gameSettings.particles ? 'bg-primary' : 'bg-gray-600'
                      }`}
                  >
                    <div className={`w-6 h-6 bg-white rounded-full shadow-md transform transition-transform duration-300 ${gameSettings.particles ? 'translate-x-6' : 'translate-x-0'
                      }`} />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                  <div>
                    <h3 className="text-white font-bold">High Contrast Mode</h3>
                    <p className="text-sm text-gray-400">Increase contrast for better visibility</p>
                  </div>
                  <button
                    onClick={() => handleGameSettingChange('highContrast', !gameSettings.highContrast)}
                    className={`w-14 h-8 rounded-full p-1 transition-colors duration-300 ${gameSettings.highContrast ? 'bg-primary' : 'bg-gray-600'
                      }`}
                  >
                    <div className={`w-6 h-6 bg-white rounded-full shadow-md transform transition-transform duration-300 ${gameSettings.highContrast ? 'translate-x-6' : 'translate-x-0'
                      }`} />
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Back Button */}
      <div className="mt-12 text-center">
        <button
          onClick={() => navigate('/')}
          className="text-gray-400 hover:text-white inline-flex items-center gap-2 transition-colors group"
        >
          <svg className="w-5 h-5 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </button>
      </div>
    </div>
  )
}

export default Settings
