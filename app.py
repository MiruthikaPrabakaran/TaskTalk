from flask import Flask, request, jsonify
from database.database import create_table, get_connection

app = Flask(__name__)

# Create database table
create_table()


# Home
@app.route("/")
def home():
    return "TaskTalk is running!"


# CREATE TASK
@app.route("/api/tasks", methods=["POST"])
def create_task():

    data = request.get_json()

    title = data.get("title")
    due_date = data.get("due_date")
    due_time = data.get("due_time")
    priority = data.get("priority", "NORMAL")
    category = data.get("category", "General")

    if not title:
        return jsonify({
            "error": "Task title is required"
        }), 400

    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO tasks
        (title, due_date, due_time, priority, category)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        due_date,
        due_time,
        priority,
        category
    ))

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Task created successfully",
        "task_id": task_id
    }), 201


# GET ALL TASKS
@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    connection = get_connection()

    tasks = connection.execute("""
        SELECT * FROM tasks
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return jsonify([dict(task) for task in tasks])


# GET ONE TASK
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):

    connection = get_connection()

    task = connection.execute("""
        SELECT * FROM tasks
        WHERE id = ?
    """, (task_id,)).fetchone()

    connection.close()

    if task is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify(dict(task))


# UPDATE TASK
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    data = request.get_json()

    connection = get_connection()

    existing_task = connection.execute("""
        SELECT * FROM tasks
        WHERE id = ?
    """, (task_id,)).fetchone()

    if existing_task is None:
        connection.close()

        return jsonify({
            "error": "Task not found"
        }), 404

    title = data.get("title", existing_task["title"])
    due_date = data.get("due_date", existing_task["due_date"])
    due_time = data.get("due_time", existing_task["due_time"])
    priority = data.get("priority", existing_task["priority"])
    category = data.get("category", existing_task["category"])
    status = data.get("status", existing_task["status"])

    connection.execute("""
        UPDATE tasks
        SET title = ?,
            due_date = ?,
            due_time = ?,
            priority = ?,
            category = ?,
            status = ?
        WHERE id = ?
    """, (
        title,
        due_date,
        due_time,
        priority,
        category,
        status,
        task_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Task updated successfully"
    })


# DELETE TASK
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    connection = get_connection()

    existing_task = connection.execute("""
        SELECT * FROM tasks
        WHERE id = ?
    """, (task_id,)).fetchone()

    if existing_task is None:
        connection.close()

        return jsonify({
            "error": "Task not found"
        }), 404

    connection.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Task deleted successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)