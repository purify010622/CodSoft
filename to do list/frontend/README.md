# Frontend Setup Guide

React + Tailwind CSS + Firebase frontend for TaskFlow.

## 📋 Prerequisites

- Node.js 16 or higher
- npm or yarn
- Firebase account (free)

## 🚀 Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Firebase Configuration

1. Go to https://console.firebase.google.com/
2. Create a new project
3. Enable **Google Authentication**
4. Get your Firebase config
5. Create `.env` file:

```
VITE_API_URL=http://localhost:5000/api
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_domain
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend runs on: **http://localhost:3000**

## 🎨 Features

- Firebase Google Authentication
- FullCalendar integration (Month/Week/Day views)
- Framer Motion animations
- Tailwind CSS styling
- Responsive design

## 🔧 Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

## 🐛 Troubleshooting

### White Screen
- Check Firebase configuration
- Ensure backend is running on port 5000
- Check browser console for errors

### Firebase Error
- Verify Google Sign-in is enabled
- Check Firebase config in `.env`

## 📦 Build for Production

```bash
npm run build
```

Output in `dist/` folder ready to deploy!
