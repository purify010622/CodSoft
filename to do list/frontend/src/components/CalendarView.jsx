import { useMemo, memo } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { motion } from 'framer-motion'

const getPriorityColor = (priority) => {
  switch (priority) {
    case 'High':
      return '#ef4444'
    case 'Medium':
      return '#f59e0b'
    case 'Low':
      return '#10b981'
    default:
      return '#6366f1'
  }
}

const CalendarView = memo(({ tasks, onDateClick, onEventClick }) => {
  // Memoize events to prevent unnecessary recalculations
  const events = useMemo(() => {
    return tasks
      .filter(task => task.due_date)
      .map(task => ({
        id: task.id,
        title: task.title,
        date: task.due_date,
        backgroundColor: getPriorityColor(task.priority),
        borderColor: getPriorityColor(task.priority),
        extendedProps: {
          completed: task.completed,
          priority: task.priority,
          description: task.description
        },
        classNames: task.completed ? ['opacity-60', 'line-through'] : []
      }))
  }, [tasks])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-gray-200/50"
    >
      <style>
        {`
          .fc {
            font-family: inherit;
          }
          .fc-theme-standard td, .fc-theme-standard th {
            border-color: #e5e7eb;
          }
          .fc-theme-standard .fc-scrollgrid {
            border-color: #e5e7eb;
          }
          .fc .fc-button-primary {
            background-color: #6366f1;
            border-color: #6366f1;
            font-weight: 600;
            text-transform: capitalize;
          }
          .fc .fc-button-primary:hover {
            background-color: #4f46e5;
            border-color: #4f46e5;
          }
          .fc .fc-button-primary:disabled {
            background-color: #9ca3af;
            border-color: #9ca3af;
          }
          .fc-toolbar-title {
            font-size: 1.5rem !important;
            font-weight: 700;
            color: #1f2937;
          }
          .fc-col-header-cell {
            background-color: #f9fafb;
            font-weight: 600;
            color: #4b5563;
            padding: 12px 0;
          }
          .fc-daygrid-day-number {
            color: #374151;
            font-weight: 600;
            padding: 8px;
          }
          .fc-daygrid-day.fc-day-today {
            background-color: #eef2ff !important;
          }
          .fc-event {
            border-radius: 6px;
            padding: 2px 4px;
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
          }
          .fc-event:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
          }
          .fc-daygrid-event {
            margin: 2px 4px;
          }
          .fc-timegrid-event {
            border-radius: 6px;
          }
        `}
      </style>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        }}
        events={events}
        dateClick={onDateClick}
        eventClick={onEventClick}
        height="auto"
        editable={true}
        selectable={true}
        selectMirror={true}
        dayMaxEvents={true}
      />
    </motion.div>
  )
})

CalendarView.displayName = 'CalendarView'

export default CalendarView
