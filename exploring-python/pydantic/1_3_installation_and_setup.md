# 1.3. Installation and Setup

This section will guide you through the process of installing Pydantic and setting up a development environment for working with the library.

## Installing Pydantic

Pydantic can be easily installed using pip, the Python package installer. Here are the steps to install Pydantic:

1. **Ensure you have Python installed**: Pydantic requires Python 3.7+. You can check your Python version by running:

   ```
   python --version
   ```

2. **Install Pydantic**: Open your terminal or command prompt and run:

   ```
   pip install pydantic
   ```

   This will install the latest stable version of Pydantic.

3. **Verify the installation**: You can verify that Pydantic was installed correctly by running:

   ```python
   python -c "import pydantic; print(pydantic.__version__)"
   ```

   This should print the version number of Pydantic that was installed.

### Optional Dependencies

Pydantic has several optional dependencies that you might want to install depending on your use case:

- `email-validator`: For email validation
- `typing-extensions`: For additional typing features
- `dotenv`: For loading environment variables from .env files

You can install these along with Pydantic using:

```
pip install pydantic[email,dotenv]
```

## Setting up a Development Environment

For a productive development experience with Pydantic, consider setting up the following:

1. **Virtual Environment**: It's a good practice to use virtual environments to isolate your project dependencies. Here's how to set one up:

   ```
   python -m venv pydantic_env
   source pydantic_env/bin/activate  # On Windows, use `pydantic_env\Scripts\activate`
   ```

2. **IDE with Python Support**: Use an IDE that supports Python and type hinting. Some popular options include:
   - PyCharm
   - Visual Studio Code with the Python extension
   - Sublime Text with the Anaconda package

3. **Install Development Tools**: Some useful tools for Python development include:
   - `pytest` for testing
   - `mypy` for static type checking
   - `black` for code formatting

   Install these with:

   ```
   pip install pytest mypy black
   ```

4. **Create a Sample Project**: Let's create a simple project to test our Pydantic setup:

   ```python
   # sample_project.py
   from pydantic import BaseModel, EmailStr, ValidationError

   class User(BaseModel):
       username: str
       email: EmailStr
       age: int

   try:
       user = User(username="johndoe", email="john@example.com", age=30)
       print(user)
   except ValidationError as e:
       print(e)

   # Try with invalid data
   try:
       invalid_user = User(username="jane", email="invalid-email", age="not-an-integer")
   except ValidationError as e:
       print(e)
   ```

5. **Run the Sample Project**: Execute the script to ensure everything is working:

   ```
   python sample_project.py
   ```

   You should see output showing a valid user and validation errors for the invalid user.

6. **Set Up Version Control**: If you haven't already, initialize a Git repository for your project:

   ```
   git init
   echo "__pycache__\n*.pyc\npydantic_env/" > .gitignore
   git add .
   git commit -m "Initial commit with Pydantic setup"
   ```

7. **Configure Linting and Formatting**: Create a `setup.cfg` file in your project root:

   ```ini
   [mypy]
   plugins = pydantic.mypy

   [tool:pytest]
   addopts = --verbose

   [flake8]
   max-line-length = 88
   extend-ignore = E203
   ```

   This sets up mypy with Pydantic support, configures pytest, and aligns flake8 with Black's formatting.

By following these steps, you'll have a fully functional development environment for working with Pydantic. This setup provides you with tools for type checking, testing, and maintaining code quality, which are crucial for developing robust applications with Pydantic.