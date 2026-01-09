# HashLab

*Your AI-Powered Pair Programmer. Run code securely with stdin support across multiple languages. Let AI explain, debug, improve, or generate snippets directly from your editor. HashLab: Your intelligent coding playground.*

## ✨ Features

  * **Multi-Language Code Execution**: Run code snippets instantly in Python, C++, C, Java, C\#, and JavaScript.
  * **Stdin Support**: Provide standard input for your code directly in the interface.
  * **Secure Environment**: Code execution is handled externally via the Piston API.
  * **AI Code Assistant**:
      * **Context-Aware**: Ask questions about the code currently in the editor without copy-pasting.
      * **Explain & Debug**: Get explanations or help finding bugs in your existing code.
      * **Improve**: Request suggestions for refactoring or optimization.
      * **Generate**: Ask the AI to write completely new code snippets.
  * **Syntax Highlighting**: Clear and readable code presentation using Prism.js.
  * **Responsive Design**: Usable interface across different screen sizes.

## 🛠️ Tech Stack

  * **Backend**: Django (Python)
  * **Frontend**: HTML, Tailwind CSS, JavaScript
  * **Code Execution**: Piston API
  * **AI Model**: Qwen/Qwen3-Coder (via Hugging Face API)
  * **Dependencies**: requests, openai, python-environ, django-tailwind

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

  * Python 3.8+
  * pip (Python package installer)
  * Git

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/<YOUR-GITHUB-USERNAME>/HashLab.git
    cd HashLab
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Tailwind CSS:**

      * Install Tailwind CLI tools if you haven't already (follow the `django-tailwind` documentation if needed).
      * Build the initial CSS:
        ```bash
        python manage.py tailwind build
        ```

5.  **Create the `.env` file:**

      * In the project root (where `manage.py` is), create a file named `.env`.
      * Add your Hugging Face API key:
        ```
        API_KEY="hf_YOUR_HUGGING_FACE_API_KEY"
        ```
      * **(Important)** Make sure `.env` is listed in your `.gitignore` file to prevent committing your secret key.

6.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

7.  **(Optional) Create a superuser for the Django Admin:**

    ```bash
    python manage.py createsuperuser
    ```

    *(Note: The admin panel is not currently used to manage app-specific data like code snippets unless you add models for that.)*

8.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

9.  **Open the app:** Navigate to `http://127.0.0.1:8000/` in your web browser.

## 📖 Usage

1.  **Select Language**: Choose the desired programming language from the dropdown.
2.  **Write Code**: Enter your code in the main editor panel.
3.  **(Optional) Provide Input**: If your code requires input, type it into the "Standard Input (stdin)" box. Each line represents a separate input.
4.  **Run Code**: Click the "Run Code" button or press `Ctrl + Enter`. The output (or error) will appear in the "Output" section.
5.  **Use AI Assistant**:
      * To get help with the code in the editor, type a question like "Explain this code" or "Find the bug" into the AI chat input and press Enter or click "Send".
      * To generate new code, start your prompt with "Write...", "Create...", or "Generate...". The AI will ignore the editor content for these requests.




