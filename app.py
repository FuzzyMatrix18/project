from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  start TEXT NOT NULL,
                  end TEXT NOT NULL,
                  color TEXT NOT NULL)''')
    
    # Insert sample data if empty
    c.execute("SELECT COUNT(*) FROM events")
    if c.fetchone()[0] == 0:
        sample_events = [
            (1, "Meeting", "2023-04-15T10:00:00", "2023-04-15T12:00:00", "#3b82f6"),
            (2, "Lunch", "2023-04-16T12:00:00", "2023-04-16T14:00:00", "#10b981")
        ]
        c.executemany("INSERT OR IGNORE INTO events (id, title, start, end, color) VALUES (?, ?, ?, ?, ?)", sample_events)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('src', 'index.jsx')

@app.route('/add_event', methods=['POST'])
def add_event():
    event = request.get_json()
    if 'color' not in event:
        event['color'] = '#3b82f6'
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (title, start, end, color) VALUES (?, ?, ?, ?)",
              (event['title'], event['start'], event['end'], event['color']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Event added successfully"}), 201

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Event deleted successfully"}), 204

@app.route('/events')
def get_events():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    rows = c.fetchall()
    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "start": row[2],
            "end": row[3],
            "color": row[4]
        })
    conn.close()
    return jsonify(events)

@app.route('/edit_event/<int:event_id>', methods=['PUT'])
def edit_event(event_id):
    event_data = request.get_json()
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("""UPDATE events SET title = ?, start = ?, end = ?, color = ?
                 WHERE id = ?""",
              (event_data['title'], event_data['start'], event_data['end'], event_data['color'], event_id))
    if c.rowcount == 0:
        conn.close()
        return jsonify({"error": "Event not found"}), 404
    conn.commit()
    conn.close()
    return jsonify({"message": "Event updated successfully"})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
