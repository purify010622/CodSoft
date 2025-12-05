import { memo } from 'react'
import { motion } from 'framer-motion'

const TaskModal = memo(({ task, onClose, onEdit }) => {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="bg-white rounded-2xl shadow-2xl max-w-lg w-full p-6"
      >
        <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Task Details</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">ID</label>
            <p className="text-lg text-gray-800">{task.id}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Title</label>
            <p className="text-lg text-gray-800 font-semibold">{task.title}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Description</label>
            <p className="text-gray-700">{task.description || 'No description'}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">Priority</label>
              <p className="text-gray-800">{task.priority}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">Status</label>
              <p className={task.completed ? 'text-green-600 font-medium' : 'text-orange-600 font-medium'}>
                {task.completed ? '✓ Completed' : '⏳ Pending'}
              </p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Due Date</label>
            <p className="text-gray-800">{task.due_date || 'Not set'}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Created At</label>
            <p className="text-gray-800">{task.created_at}</p>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={() => {
              onClose()
              onEdit(task)
            }}
            className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-3 rounded-xl transition-all duration-200"
          >
            ✏️ Edit Task
          </button>
          <button
            onClick={onClose}
            className="flex-1 bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white font-bold py-3 rounded-xl transition-all duration-200"
          >
            Close
          </button>
        </div>
      </motion.div>
    </div>
  )
})

TaskModal.displayName = 'TaskModal'

export default TaskModal
