import { useState, useEffect, useCallback, useMemo } from 'react'
import axios from 'axios'
import { onAuthStateChanged, signOut } from 'firebase/auth'
import { auth } from './firebase'
import { motion, AnimatePresence } from 'framer-motion'
import Login from './components/Login'
import TaskList from './components/TaskList'
import TaskForm from './components/TaskForm'
import SearchFilter from './components/SearchFilter'
import TaskModal from './components/TaskModal'
import CalendarView from './components/CalendarView'

// API configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Create axios instance for API calls
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [tasks, setTasks] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState(null)
  const [selectedTask, setSelectedTask] = useState(null)
  const [view, setView] = useState('list')
  const [filters, setFilters] = useState({
    search: '',
    status: 'all',
    priority: 'All'
  })

  // Fetch all tasks for the current user
  const fetchTasks = useCallback(async (userId) => {
    try {
      const response = await api.get('/tasks', {
        params: { user_id: userId }
      })
      setTasks(response.data)
    } catch (error) {
      console.error('Error fetching tasks:', error)
    }
  }, [])

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
      if (currentUser) {
        fetchTasks(currentUser.uid)
      }
    })
    return () => unsubscribe()
  }, [fetchTasks])

  // Filter tasks based on search and filter criteria
  const filteredTasks = useMemo(() => {
    let filtered = [...tasks]

    // Search by title or description
    if (filters.search) {
      const searchLower = filters.search.toLowerCase()
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(searchLower) ||
        task.description.toLowerCase().includes(searchLower)
      )
    }

    // Filter by completion status
    if (filters.status === 'completed') {
      filtered = filtered.filter(task => task.completed)
    } else if (filters.status === 'pending') {
      filtered = filtered.filter(task => !task.completed)
    }

    // Filter by priority
    if (filters.priority !== 'All') {
      filtered = filtered.filter(task => task.priority === filters.priority)
    }

    return filtered
  }, [tasks, filters])

  // Create a new task
  const handleCreateTask = useCallback(async (taskData) => {
    try {
      await api.post('/tasks', {
        ...taskData,
        user_id: user.uid
      })
      fetchTasks(user.uid)
      setShowForm(false)
    } catch (error) {
      console.error('Error creating task:', error)
    }
  }, [user, fetchTasks])

  // Update existing task
  const handleUpdateTask = useCallback(async (taskData) => {
    try {
      if (!editingTask || !editingTask.id) {
        alert('Error: Cannot update task - no task ID found')
        return
      }
      
      await api.put(`/tasks/${editingTask.id}`, {
        ...taskData,
        user_id: user.uid
      })
      
      await fetchTasks(user.uid)
      setShowForm(false)
      setEditingTask(null)
    } catch (error) {
      console.error('Error updating task:', error)
      alert(`Error updating task: ${error.message}`)
    }
  }, [user, editingTask, fetchTasks])

  // Delete a task with confirmation
  const handleDeleteTask = useCallback(async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await api.delete(`/tasks/${taskId}`)
        fetchTasks(user.uid)
      } catch (error) {
        console.error('Error deleting task:', error)
      }
    }
  }, [user, fetchTasks])

  // Toggle task completion status
  const handleToggleComplete = useCallback(async (taskId) => {
    try {
      await api.patch(`/tasks/${taskId}/toggle`)
      fetchTasks(user.uid)
    } catch (error) {
      console.error('Error toggling task:', error)
    }
  }, [user, fetchTasks])

  // Open edit form for a task
  const handleEditClick = useCallback((task) => {
    setEditingTask(task)
    setShowForm(true)
  }, [])

  // Open form to add new task
  const handleAddClick = useCallback(() => {
    setEditingTask(null)
    setShowForm(true)
  }, [])

  // Close the task form
  const handleCloseForm = useCallback(() => {
    setShowForm(false)
    setEditingTask(null)
  }, [])

  // Handle user logout
  const handleLogout = useCallback(async () => {
    try {
      await signOut(auth)
      setTasks([])
    } catch (error) {
      console.error('Logout error:', error)
    }
  }, [])

  // Handle calendar date click to create new task
  const handleDateClick = useCallback((info) => {
    setEditingTask(null)
    setShowForm(true)
  }, [])

  // Handle calendar event click to view task details
  const handleEventClick = useCallback((info) => {
    const task = tasks.find(t => t.id === parseInt(info.event.id))
    if (task) {
      setSelectedTask(task)
    }
  }, [tasks])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full"
        />
      </div>
    )
  }

  if (!user) {
    return <Login onLogin={setUser} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="bg-white/80 backdrop-blur-md shadow-lg border-b border-gray-200/50 sticky top-0 z-40"
      >
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  TaskFlow
                </h1>
                <p className="text-sm text-gray-600">Welcome, {user.displayName}</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* View Toggle */}
              <div className="flex bg-gray-100 rounded-xl p-1">
                <button
                  onClick={() => setView('list')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    view === 'list'
                      ? 'bg-white text-purple-600 shadow-md'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  List
                </button>
                <button
                  onClick={() => setView('calendar')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    view === 'calendar'
                      ? 'bg-white text-purple-600 shadow-md'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Calendar
                </button>
              </div>

              {/* User Menu */}
              <div className="flex items-center gap-3">
                <img
                  src={user.photoURL}
                  alt={user.displayName}
                  className="w-10 h-10 rounded-full border-2 border-purple-500"
                />
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-xl font-medium transition-all"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </motion.header>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Search and Filter */}
        <SearchFilter filters={filters} setFilters={setFilters} />

        {/* Add Task Button */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-6"
        >
          <button
            onClick={handleAddClick}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg transition-all duration-200 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add New Task
          </button>
        </motion.div>

        {/* Content */}
        <AnimatePresence mode="wait">
          {view === 'list' ? (
            <motion.div
              key="list"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
            >
              <TaskList
                tasks={filteredTasks}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEditClick}
                onDelete={handleDeleteTask}
                onViewDetails={setSelectedTask}
              />
            </motion.div>
          ) : (
            <motion.div
              key="calendar"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
            >
              <CalendarView
                tasks={filteredTasks}
                onDateClick={handleDateClick}
                onEventClick={handleEventClick}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Task Form Modal */}
        <AnimatePresence>
          {showForm && (
            <TaskForm
              task={editingTask}
              onSubmit={editingTask && editingTask.id ? handleUpdateTask : handleCreateTask}
              onClose={handleCloseForm}
            />
          )}
        </AnimatePresence>

        {/* Task Details Modal */}
        <AnimatePresence>
          {selectedTask && !showForm && (
            <TaskModal 
              task={selectedTask} 
              onClose={() => setSelectedTask(null)}
              onEdit={(task) => {
                setSelectedTask(null)
                handleEditClick(task)
              }}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default App
