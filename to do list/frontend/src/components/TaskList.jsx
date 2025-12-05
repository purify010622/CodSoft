import { memo } from 'react'
import { motion } from 'framer-motion'

const TaskList = memo(({ tasks, onToggleComplete, onEdit, onDelete, onViewDetails }) => {
  const getPriorityColor = (priority) => {
    const colors = {
      High: 'bg-red-100 text-red-800 border-red-300',
      Medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      Low: 'bg-green-100 text-green-800 border-green-300'
    }
    return colors[priority] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  if (tasks.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-12 text-center border border-gray-200/50"
      >
        <p className="text-gray-500 text-lg">No tasks found. Add a new task to get started!</p>
      </motion.div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task, index) => (
        <motion.div
          key={task.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          className={`bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-6 transition-all duration-200 hover:shadow-xl border border-gray-200/50 ${
            task.completed ? 'opacity-75' : ''
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4 flex-1">
              {/* Checkbox */}
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggleComplete(task.id)}
                className="mt-1 w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
              />

              {/* Task Info */}
              <div className="flex-1" onClick={() => onViewDetails(task)} style={{ cursor: 'pointer' }}>
                <h3
                  className={`text-xl font-semibold mb-2 ${
                    task.completed ? 'line-through text-gray-500' : 'text-gray-800'
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-gray-600 mb-3">{task.description}</p>
                )}
                <div className="flex flex-wrap gap-3 items-center">
                  {/* Priority Badge */}
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium border ${getPriorityColor(
                      task.priority
                    )}`}
                  >
                    {task.priority}
                  </span>

                  {/* Due Date */}
                  {task.due_date && (
                    <span className="text-sm text-gray-600 flex items-center gap-1">
                      📅 {task.due_date}
                    </span>
                  )}

                  {/* Status */}
                  <span
                    className={`text-sm font-medium ${
                      task.completed ? 'text-green-600' : 'text-orange-600'
                    }`}
                  >
                    {task.completed ? '✓ Completed' : '⏳ Pending'}
                  </span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2 ml-4">
              <button
                onClick={() => onEdit(task)}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl transition-all duration-200 font-medium"
              >
                ✏️ Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-xl transition-all duration-200 font-medium"
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  )
})

TaskList.displayName = 'TaskList'

export default TaskList
