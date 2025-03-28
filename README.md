# TermList - Advanced Terminal Task Manager

## Overview

TermList is a powerful command-line task management application designed for users who prefer working in the terminal environment. It combines robust task organization features with a secure user authentication system, all presented through an intuitive interface built with Python's Rich library for enhanced visual presentation.

## Key Features

- **Secure User Authentication**: Utilizes bcrypt for password hashing and secure credential storage
- **Comprehensive Task Management**:
  - Create, edit, and delete tasks with detailed metadata
  - Set priorities, due dates, and custom tags
  - Archive completed tasks without permanent deletion
- **Advanced Organization**:
  - Filter tasks by priority level
  - View both active and archived tasks
  - Track creation and modification timestamps
- **Rich Terminal Interface**:
  - Beautifully formatted tables for task display
  - Color-coded output for better readability
  - Progress tracking capabilities

## Installation

To install TermList, run the following command:

```bash
wget https://raw.githubusercontent.com/linuxfanboy4/termlist/refs/heads/main/src/termlist.py && python3 termlist.py
```

## System Requirements

- Python 3.6 or higher
- SQLite3 (typically included with Python)
- Required Python packages (install via `pip install -r requirements.txt`):
  - rich
  - click
  - bcrypt

## Usage

TermList operates through a command-line interface with the following commands available:

### User Management

```bash
# Create a new user account
python3 termlist.py signup username password

# Login to an existing account
python3 termlist.py login username password
```

### Task Operations

```bash
# Add a new task
python3 termlist.py add_new_task "Task Title" "Description" "YYYY-MM-DD" priority "tag1,tag2"

# Delete a task
python3 termlist.py delete task_id

# Archive a task
python3 termlist.py archive task_id

# Edit an existing task
python3 termlist.py edit task_id

# Filter tasks by priority (1-5)
python3 termlist.py filter_priority level
```

## Example Session

```bash
# Initialize the application database
python3 termlist.py

# Create a new user
python3 termlist.py signup johndoe securepassword123

# Login (will display user's tasks)
python3 termlist.py login johndoe securepassword123

# Add several tasks
python3 termlist.py add_new_task "Complete project" "Finish the CLI application" "2023-12-15" 3 "work,urgent"
python3 termlist.py add_new_task "Buy groceries" "Milk, eggs, bread" "2023-12-10" 2 "personal"
python3 termlist.py add_new_task "Schedule meeting" "Team sync for Q1 planning" "2023-12-20" 4 "work"

# View tasks (automatically shown after login)

# Archive a completed task
python3 termlist.py archive 2

# Edit a task
python3 termlist.py edit 1
# Follow prompts to update task details

# Filter high-priority tasks
python3 termlist.py filter_priority 4

# Delete a task
python3 termlist.py delete 3
```

## Database Schema

TermList uses SQLite3 with the following schema:

### Users Table
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- password (TEXT - bcrypt hashed)

### Tasks Table
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER - foreign key to users)
- title (TEXT)
- description (TEXT)
- due_date (TEXT)
- priority (INTEGER)
- status (TEXT)
- tags (TEXT)
- created_at (TEXT)
- updated_at (TEXT)
- archived (INTEGER DEFAULT 0)

## Security Considerations

- All passwords are hashed using bcrypt before storage
- Database connections are properly closed after each operation
- User authentication is required for task operations
- Sensitive operations (deletion) require explicit confirmation

## License

TermList is released under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes. Ensure all code follows PEP 8 guidelines and includes appropriate tests.

## Support

For issues or feature requests, please open an issue on the GitHub repository.
