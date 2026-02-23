from flask import Flask, render_template, url_for, request, redirect  # Import Flask and related modules
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM
from datetime import datetime  # Import datetime for timestamp

app = Flask(__name__)  # Initialize Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Set up SQLite database
db = SQLAlchemy(app)  # Initialize SQLAlchemy with app

class Todo(db.Model):
    # Model for a to-do task
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each task
    content = db.Column(db.String(200), nullable=False)  # Task description
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp when task is created

    def __repr__(self):
        # Representation for debugging
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Main page route. Handles displaying tasks and adding new tasks.
    POST: Add a new task.
    GET: Show all tasks.
    """
    if request.method == 'POST':
        task_content = request.form.get('content')  # Get task content from form
        if not task_content:
            return 'Task content cannot be empty', 400
        new_task = Todo(content=task_content)  # Create new task object
        try:
            db.session.add(new_task)  # Add task to session
            db.session.commit()  # Commit to database
            return redirect('/')  # Redirect to main page
        except Exception as e:
            db.session.rollback()  # Rollback on error
            return f'There was an issue adding your task: {e}', 500
    else:
        tasks = Todo.query.order_by(Todo.date_created.desc()).all()  # Get all tasks ordered by date
        return render_template('index.html', tasks=tasks)  # Render main page


@app.route('/delete/<int:id>')
def delete(id):
    """
    Route to delete a task by ID.
    """
    task_to_delete = Todo.query.get_or_404(id)  # Get task or 404 if not found
    try:
        db.session.delete(task_to_delete)  # Delete task
        db.session.commit()  # Commit changes
        return redirect('/')  # Redirect to main page
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return f'There was a problem deleting that task: {e}', 500

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """
    Route to update a task by ID.
    GET: Show update form.
    POST: Update task content.
    """
    task = Todo.query.get_or_404(id)  # Get task or 404 if not found
    if request.method == 'POST':
        task_content = request.form.get('content')  # Get updated content
        if not task_content:
            return 'Task content cannot be empty', 400
        task.content = task_content  # Update task content
        try:
            db.session.commit()  # Commit changes
            return redirect('/')  # Redirect to main page
        except Exception as e:
            db.session.rollback()  # Rollback on error
            return f'There was an issue updating your task: {e}', 500
    else:
        return render_template('update.html', task=task)  # Render update form


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
