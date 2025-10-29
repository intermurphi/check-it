# CHECK-IT - Task Management App

A beautiful task management application with a pink/cream aesthetic, featuring a friendly panda companion!

## Features

- Interactive task checklist with checkboxes
- Real-time score tracking (percentage of completed tasks)
- Responsive design with a fun, colorful interface
- Backend API for persistent task storage
- Animated panda character
- Dynamic day-of-week display

## Tech Stack

### Frontend
- React.js with Vite
- CSS3 with animations
- Fetch API for backend communication

### Backend
- FastAPI (Python)
- SQLite database
- RESTful API architecture

## Setup Instructions

### Prerequisites
- Node.js (v20+)
- Python 3.8+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

The backend will be running at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be running at `http://localhost:5173`

## Usage

1. Start both the backend and frontend servers
2. Open your browser to `http://localhost:5173`
3. Check off tasks as you complete them
4. Watch your score increase as you make progress!

## API Endpoints

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Project Structure

```
check-it/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── core.py          # Business logic
│   ├── db.py            # Database configuration
│   ├── models.py        # Data models
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main React component
│   │   ├── App.css      # Styling
│   │   └── index.css    # Global styles
│   └── package.json     # Node dependencies
└── README.md
```

## Design Credits

Based on the original hand-drawn design featuring "Dikshita's Monday" theme with a cute panda character.
