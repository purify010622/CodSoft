# TaskFlow - Modern To-Do List Application

**CODSOFT Python Programming Internship - Task 1**

A full-stack To-Do List application with React + Tailwind CSS frontend, Flask backend, Firebase Authentication, and MongoDB + JSON dual storage.

## 🎯 Features

- ✅ Create, update, delete tasks
- ✓ Mark tasks as complete/incomplete
- 🔍 Real-time search
- 🎯 Filter by status and priority
- 📅 Calendar view (Month/Week/Day)
- 🔐 Firebase Google Sign-in
- 💾 MongoDB + JSON dual storage
- 🎨 Modern minimalist UI
- 📱 Fully responsive

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 16+
- MongoDB (optional)
- Firebase account

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd "python project"
```

2. **Setup Backend**
```bash
cd backend
pip install -r requirements.txt
python api.py
```
Backend runs on: http://localhost:5000

3. **Setup Frontend**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: http://localhost:3000

4. **Configure Firebase**
- Create Firebase project at https://console.firebase.google.com/
- Enable Google Authentication
- Update `frontend/src/firebase.js` with your config

For detailed setup instructions, see:
- [Backend Setup](backend/README.md)
- [Frontend Setup](frontend/README.md)

## 📁 Project Structure

```
python project/
├── backend/              # Flask API
│   ├── api.py           # REST API endpoints
│   ├── task_manager.py  # JSON storage
│   ├── mongodb_manager.py # MongoDB storage
│   └── README.md        # Backend setup guide
├── frontend/            # React app
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   └── utils/       # Utilities
│   └── README.md        # Frontend setup guide
└── README.md            # This file
```

## 🛠️ Tech Stack

**Frontend:** React 18, Tailwind CSS, Vite, Firebase, FullCalendar, Framer Motion  
**Backend:** Flask, PyMongo, Python-dotenv  
**Database:** MongoDB + JSON  
**Auth:** Firebase Google Sign-in

## 📖 Usage

1. **Sign in** with your Google account
2. **Add tasks** using the "Add New Task" button
3. **Switch views** between List and Calendar
4. **Search** tasks in real-time
5. **Filter** by status or priority
6. **Edit** tasks by clicking on them
7. **Delete** tasks when done

## 👨‍💻 Author

Created for CODSOFT Python Programming Internship

## 📄 License

Free to use for educational purposes
