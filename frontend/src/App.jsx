import { useState, useEffect } from 'react'
import './App.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

function App() {
  const [tasks, setTasks] = useState([])
  const [userName, setUserName] = useState('Dikshita')
  const [currentDay, setCurrentDay] = useState(() => {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return days[new Date().getDay()]
  })
  const [loading, setLoading] = useState(true)

  // Fetch tasks from backend
  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`)
      const data = await response.json()
      setTasks(data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching tasks:', error)
      // Use default tasks if backend is not available
      setTasks([
        { id: 1, name: 'Task-1', desc: 'First task', status: false },
        { id: 2, name: 'Task-2', desc: 'Second task', status: false },
        { id: 3, name: 'Task-3', desc: 'Third task', status: false }
      ])
      setLoading(false)
    }
  }

  const calculateScore = () => {
    if (tasks.length === 0) return 0
    const completedTasks = tasks.filter(task => task.status).length
    return Math.round((completedTasks / tasks.length) * 100)
  }

  const toggleTask = async (id) => {
    const task = tasks.find(t => t.id === id)
    if (!task) return

    const updatedTask = { ...task, status: !task.status }

    // Optimistically update UI
    setTasks(tasks.map(t => t.id === id ? updatedTask : t))

    try {
      await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: !task.status })
      })
    } catch (error) {
      console.error('Error updating task:', error)
      // Revert on error
      setTasks(tasks.map(t => t.id === id ? task : t))
    }
  }

  if (loading) {
    return (
      <div className="app">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontSize: '2rem' }}>
          Loading...
        </div>
      </div>
    )
  }

  const completedTasks = tasks.filter(task => task.status).length
  const totalTasks = tasks.length

  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">CHECK-IT</h1>
        <div className="fraction-display">
          <span>{completedTasks}</span>
          <span>{totalTasks}</span>
        </div>
      </header>

      <main className="main-content">
        <div className="divider-line"></div>
        <h2 className="title">{userName}'s {currentDay}</h2>

        <div className="content-wrapper">
          <div className="task-list">
            {tasks.length === 0 ? (
              <p style={{ textAlign: 'center', fontSize: '1.5rem', fontFamily: 'Comic Sans MS, cursive' }}>No tasks yet!</p>
            ) : (
              tasks.map(task => (
                <div key={task.id} className="task-item">
                  <input
                    type="checkbox"
                    id={`task-${task.id}`}
                    checked={task.status}
                    onChange={() => toggleTask(task.id)}
                    className="task-checkbox"
                  />
                  <label htmlFor={`task-${task.id}`} className="task-label">
                    {task.name}
                  </label>
                </div>
              ))
            )}
          </div>

          <div className="character">
            <div className="speech-bubble">Hey There!</div>
            <div className="cartoon-character">
              <div className="character-hat"></div>
              <div className="character-tie"></div>
            </div>
          </div>
        </div>

        <div className="score-section">
          <div className="score-checkmark">✓</div>
          <div className="score-box">
            SCORE: {calculateScore()} %
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
