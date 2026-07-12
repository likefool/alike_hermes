import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "notes.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print(f"Database '{DB_NAME}' initialized.")

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Missing title"}), 400
    
    # Sanitize input: limit length to prevent DoS via massive strings
    title = str(data['title'])[:255]
    content = str(data.get('content', ''))[:5000]
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)", 
            (title, content)
        )
        new_id = cursor.lastrowid
    
    return jsonify({"id": new_id, "title": title, "content": content}), 201

@app.route('/notes', methods=['GET'])
def get_notes():
    query_param = request.args.get('q', '').strip()
    
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if query_param:
            # Securely parameterized LIKE search
            search_pattern = f"%{query_param}%"
            cursor.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?", 
                (search_pattern, search_pattern)
            )
        else:
            cursor.execute("SELECT * FROM notes")
            
        notes = [dict(row) for row in cursor.fetchall()]
    return jsonify(notes), 200

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
    
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(dict(note)), 200

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    title = data.get('title')
    content = data.get('content')
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Verify existence first
        cursor.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Note not found"}), 404
        
        if title is not None:
            cursor.execute("UPDATE notes SET title = ? WHERE id = ?", (str(title)[:255], note_id))
        if content is not None:
            cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (str(content)[:5000], note_id))
            
    return jsonify({"message": "Note updated"}), 200

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Note not found"}), 404
            
    return jsonify({"message": "Note deleted"}), 200

if __name__ == '__main__':
    init_db()
    # HARDENED: Debug mode is OFF. 
    # In production, bind to a specific IP/Port as needed.
    app.run(host='0.0.0.0', port=5000, debug=False)
