# Backend Setup Guide

Flask REST API with MongoDB + JSON dual storage.

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- MongoDB (optional - app works without it)

## 🚀 Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- flask-cors (CORS support)
- pymongo (MongoDB driver)
- python-dotenv (environment variables)
- gunicorn (production server)

### 2. Run the Server

```bash
python api.py
```

Server runs on: **http://localhost:5000**

You should see:
```
✓ MongoDB connected successfully
* Running on http://127.0.0.1:5000
```

## 📡 API Endpoints

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `PATCH /api/tasks/<id>/toggle` - Toggle completion

### Health Check
- `GET /api/health` - Check API status

## 🗄️ Data Storage

The backend uses **dual storage**:

1. **MongoDB** (Primary) - Optional
2. **JSON File** (Fallback) - Always works

Both are synced automatically!

## 🐛 Troubleshooting

### MongoDB Connection Failed
This is OK! The app will use JSON storage.

### Module Not Found
```bash
pip install -r requirements.txt
```

## 🚀 Production Deployment

```bash
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```
