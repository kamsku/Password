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
python main.py
```

## Project Structure

```
.
├── LICENSE
├── README.md
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

## Improvements Introduced in the Project

The original code has been significantly improved and refactored to meet the standards of a professional GitHub project. Key changes include:

1.  **Modularity and Code Readability**: The code has been divided into smaller, logical files, each responsible for a specific aspect of functionality. This increases readability, facilitates maintenance, and testing.
2.  **Improved Error Handling**: More detailed exception handling has been added, especially in the password generator and menu functions, to make the application more resilient to user errors and unforeseen situations.
3.  **Enhanced Password Validation**: Password validation logic has been improved to ensure that generated passwords are even stronger and meet more stringent criteria (e.g., added lowercase letter requirement).
4.  **Better User Interface (CLI)**: UI functions have been extracted into a separate module (`cli_utils.py`), and their implementation has been standardized. `display_error`, `display_success`, `display_info` functions have been added for consistent message display.
5.  **Centralized Configuration**: All configuration constants have been moved to `config.py`, which simplifies project settings management.
6.  **Code Documentation**: Docstrings have been added to classes and functions, explaining their purpose, arguments, and return values, which is crucial for other developers to understand the code.
7.  **Dependency Management**: A `requirements.txt` file has been created for easy installation of all required libraries.
8.  **Professional README**: A comprehensive `README.md` file has been created, detailing the project, its functionalities, installation and running instructions, and the improvements made, which is essential for any open-source project.

These changes transform the code from a simple script into a well-organized and professional application, ideal for presentation in a portfolio.