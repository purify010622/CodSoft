import { createContext, useContext, useState, useEffect } from 'react'
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  signInWithPopup,
  GoogleAuthProvider
} from 'firebase/auth'
import { auth, googleProvider } from '../config/firebase'
import api from '../config/api'

const AuthContext = createContext({})

export const useAuth = () => useContext(AuthContext)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [userData, setUserData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        setUser(firebaseUser)
        // Fetch user data from backend
        try {
          const response = await api.get('/auth/profile')
          setUserData(response.data)
        } catch (error) {
          console.error('Error fetching user data:', error)
          // Possibly first login?
          setUserData(null)
        }
      } else {
        setUser(null)
        setUserData(null)
      }
      setLoading(false)
    })

    return unsubscribe
  }, [])

  const loginWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider)
      // Check/Register in backend
      await api.post('/auth/login', {
        email: result.user.email,
        uid: result.user.uid,
        name: result.user.displayName
      })
      return result.user
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await signOut(auth)
      setUser(null)
      setUserData(null)
    } catch (error) {
      throw error
    }
  }

  // Keep playAsGuest for fallback
  const playAsGuest = () => {
    const guestUser = { uid: `guest_${Date.now()}`, isGuest: true }
    setUser(guestUser)
    setUserData({ username: 'Guest' })
  }

  const value = {
    user,
    userData,
    loading,
    loginWithGoogle,
    logout,
    playAsGuest
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
