# Flask ToDoList

A simple and intuitive web-based to-do list application built with Flask. This project allows users to create, view, update, and delete their tasks in a clean and user-friendly interface.

## Features
- Add new tasks
- View all tasks
- Update existing tasks
- Delete tasks
- Tasks are stored in a SQLite database

## Project Structure

```
├── app.py              # Main Flask application
├── test_app.py         # Unit tests for the app
├── requirements.txt    # Python dependencies
├── static/             # Static files (CSS)
│   └── css/
│       └── main.css
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   └── update.html
└── env/                # Python virtual environment
```

## API Endpoints

- `/` [GET, POST]: Main page. View tasks and add new tasks.
- `/delete/<int:id>` [GET]: Delete a task by ID.
- `/update/<int:id>` [GET, POST]: Update a task by ID.

## How To Run
1. Install `virtualenv`:
	```bash
	pip install virtualenv
	```
2. Open a terminal in the project root directory and run:
	```bash
	virtualenv env
	```
3. Activate the virtual environment:
	- On macOS/Linux:
	  ```bash
	  source env/bin/activate
	  ```
	- On Windows:
	  ```bash
	  .\env\Scripts\activate
	  ```
4. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
5. Start the web server:
	```bash
	python app.py
	```

## Running Tests

Unit tests are provided in `test_app.py`.

To run tests:

```bash
python -m unittest test_app.py
```

## License

This project is licensed under the MIT License.
