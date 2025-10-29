import sqlite3

DATABASE_NAME = "tasks.db"

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            desc TEXT NOT NULL,
            status BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Check if tasks already exist
    cursor.execute('SELECT COUNT(*) FROM tasks')
    task_count = cursor.fetchone()[0]
    
    # Add default tasks if none exist
    if task_count == 0:
        default_tasks = [
            ('TASK-1', 'First task to complete', False),
            ('TASK-2', 'Second task to complete', False),
            ('TASK-3', 'Third task to complete', False)
        ]
        
        cursor.executemany(
            'INSERT INTO tasks (name, desc, status) VALUES (?, ?, ?)',
            default_tasks
        )

    conn.commit()
    conn.close()
