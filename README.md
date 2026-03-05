# Password Generator and Hashing Tool

## Project Description

This project is an advanced password generator with hashing functionalities and time measurement for various cryptographic algorithms. The application offers an interactive terminal menu, allowing the user to generate single passwords, perform batch analysis of multiple passwords with CSV/XLSX export, and hash entered passwords using selected algorithms.

The project was created with security in mind, utilizing cryptographically secure random number generators (`secrets`) and popular hashing algorithms such as MD5, SHA-1, SHA-256, SHA-512, bcrypt, and scrypt. It is an ideal tool for demonstrating Python programming skills, with a particular focus on good coding practices, modularity, and console user interface handling.

## Features

*   **Password Generator**: Creates strong, unique passwords meeting complex criteria (length, special characters, uppercase letters, digits).
*   **Batch Analysis**: Generates multiple passwords, hashes them with various algorithms, and measures the execution time for each.
*   **Data Export**: Batch analysis results can be exported to CSV and XLSX files, facilitating further analysis and reporting.
*   **Single Password Hashing**: Ability to hash a user-entered password (with hidden input) using a selected algorithm.
*   **Time Measurement**: Precise measurement of hashing operation execution times, allowing for performance comparison of algorithms.
*   **Interactive CLI Menu**: User-friendly text interface with colored output (ANSI support, with fallback for Windows).
*   **Modular Code Structure**: Code divided into logical modules (`cli_utils`, `config`, `password_generator`, `hashing_functions`, `timing_utils`, `main`), which facilitates understanding, testing, and development.

## Technologies Used

*   **Python 3.x**
*   `secrets` (standard module) - for generating cryptographically secure random numbers.
*   `hashlib` (standard module) - for MD5, SHA-1, SHA-256, SHA-512 algorithms.
*   `bcrypt` (external library) - for secure password hashing.
*   `pandas` (external library) - for handling and exporting data in DataFrame format.
*   `colorama` (external library) - optional, for ANSI color support in the Windows console.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kamsku/Password.git
    cd Password
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate   # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

After installing dependencies, run the application using the command:

```bash
python password_generator/main.py
```

## Project Structure

```
.
├── LICENSE
├── README.md
├── requirements.txt
└── password_generator
    ├── cli_utils.py
    ├── config.py
    ├── hashing_functions.py
    ├── main.py
    ├── password_generator.py
    └── timing_utils.py
```

*   `main.py`: The main application file, containing menu logic and module orchestration.
*   `cli_utils.py`: Helper functions for command-line interface handling (colors, headers, menus, data prompts).
*   `config.py`: Configuration file containing constants and global settings (e.g., password length, hashing parameters).
*   `hashing_functions.py`: Implementations of various hashing algorithms (MD5, SHA-1, SHA-256, SHA-512, bcrypt, scrypt).
*   `password_generator.py`: Logic for password generation and validation.
*   `timing_utils.py`: Function for precise measurement of other functions' execution time.
*   `requirements.txt`: List of Python dependencies.

