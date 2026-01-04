import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const NavLink = ({ to, children }) => (
  <Link
    to={to}
    className="relative text-gray-300 hover:text-white font-medium transition-colors duration-200 group"
  >
    {children}
    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-neon-blue to-neon-pink group-hover:w-full transition-all duration-300"></span>
  </Link>
)

const Navbar = () => {
  const { user, userData, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
      navigate('/login')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <nav className="glass-nav sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link to="/" className="text-3xl font-bold flex items-center gap-3 group">
            <span className="text-4xl group-hover:animate-bounce">✊</span>
            <span className="text-gradient font-extrabold tracking-tight">RPS ARENA</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-8">
            <NavLink to="/">Arena</NavLink>
            <NavLink to="/leaderboard">Leaderboard</NavLink>
            {user && <NavLink to={`/profile/${user.uid}`}>Profile</NavLink>}
            {userData?.role === 'admin' && <NavLink to="/admin">Admin</NavLink>}
          </div>

          {/* User Menu */}
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <Link to="/settings" className="p-2 text-gray-300 hover:text-white transition-colors duration-200">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </Link>
                {!user.isGuest && (
                  <button
                    onClick={handleLogout}
                    className="btn-outline text-sm py-2 px-4 border-red-500/50 text-red-400 hover:bg-red-500/10 hover:border-red-500"
                  >
                    Logout
                  </button>
                )}
              </>
            ) : (
              <div className="flex gap-4">
                <Link to="/login" className="text-gray-300 hover:text-white font-medium px-4 py-2">
                  Login
                </Link>
                <Link to="/register" className="btn-primary py-2 px-6 text-sm">
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}


export default Navbar
