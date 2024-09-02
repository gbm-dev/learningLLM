import venv
import subprocess
import sys
import os
import platform
import getpass
import shutil
import logging
import io
import traceback

# Set up logging
log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Try to import colorama, fall back to no colors if not available
try:
    from colorama import init, Fore, Style # type: ignore
    init()
    
    def print_color(text, color, end='\n'):
        print(f"{color}{text}{Style.RESET_ALL}", end=end)
        logging.info(text)  # Log the text without color

except ImportError:
    # Fallback function if colorama is not installed
    def print_color(text, color, end='\n'):
        print(text, end=end)
        logging.info(text)  # Log the text

    # Define dummy color constants to avoid errors
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        CYAN = ''
        LIGHTYELLOW_EX = ''

def create_env_file():
    if os.path.exists('.env'):
        print_color("📁 .env file already exists. Skipping creation.", Fore.YELLOW)
        return

    print_color("🔑 Please enter your OpenAI API key: ", Fore.CYAN, end='')
    sys.stdout.flush()  # Ensure the prompt is displayed
    openai_api_key = getpass.getpass(prompt='')
    
    with open('.env', 'w') as f:
        f.write(f"OPENAI_API_KEY={openai_api_key}\n")
    
    print_color("✅ .env file created successfully.", Fore.GREEN)

def run_command(command, use_sudo=False):
    try:
        if use_sudo:
            command = ["sudo"] + command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Command executed: {' '.join(command)}")
        logging.info(f"Command output: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"Error executing command: {e}"
        print_color(error_msg, Fore.RED)
        logging.error(error_msg)
        logging.error(f"Command error output: {e.stderr}")
        return None

def is_venv_installed():
    try:
        import ensurepip
        return True
    except ImportError:
        return False

def install_python_venv(version):
    print_color(f"Attempting to install python{version}-venv package...", Fore.YELLOW)
    update_command = ["apt", "update"]
    install_command = ["apt", "install", "-y", f"python{version}-venv"]
    
    if run_command(update_command, use_sudo=True) is not None and run_command(install_command, use_sudo=True) is not None:
        print_color(f"✅ python{version}-venv package installed successfully.", Fore.GREEN)
        return True
    else:
        print_color(f"❌ Failed to install python{version}-venv package. Please install it manually.", Fore.RED)
        return False

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def install_requirements(python_path):
    print_color("Installing required packages:", Fore.CYAN)
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()

    for package in requirements:
        try:
            # Check if the package is already installed
            result = subprocess.run([python_path, '-m', 'pip', 'show', package], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print_color(f"  ✅ {package} is already installed.", Fore.GREEN)
            else:
                # If not installed, attempt to install it
                install_result = subprocess.run([python_path, '-m', 'pip', 'install', package], 
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if install_result.returncode == 0:
                    print_color(f"  ✅ Installed {package} successfully.", Fore.GREEN)
                else:
                    error_msg = f"  ❌ Failed to install {package}. Error: {install_result.stderr}"
                    print_color(error_msg, Fore.RED)
                    logging.error(error_msg)
                    return False
        except subprocess.CalledProcessError as e:
            error_msg = f"  ❌ Error checking/installing {package}: {str(e)}"
            print_color(error_msg, Fore.RED)
            logging.error(error_msg)
            return False
    return True

def setup_venv():
    venv_path = os.path.join(os.getcwd(), 'venv')
    python_version = get_python_version()
    
    # Remove existing venv if it exists
    if os.path.exists(venv_path):
        print_color(f"Removing existing virtual environment at {venv_path}", Fore.YELLOW)
        shutil.rmtree(venv_path)
        print_color("✅ Existing virtual environment removed.", Fore.GREEN)
    
    if not is_venv_installed():
        print_color("python3-venv is not installed. Attempting to install it...", Fore.YELLOW)
        if not install_python_venv(python_version):
            print_color("Failed to install python3-venv. Please install it manually and run this script again.", Fore.RED)
            return False
    
    try:
        venv.create(venv_path, with_pip=True)
        print_color(f"✅ Virtual environment created at {venv_path}", Fore.GREEN)
    except subprocess.CalledProcessError as e:
        error_msg = f"❌ Virtual environment creation failed: {str(e)}"
        print_color(error_msg, Fore.RED)
        logging.error(error_msg)
        return False
    
    # Determine the path to the activated Python interpreter
    if platform.system() == 'Windows':
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        activate_path = os.path.join('.', 'venv', 'Scripts', 'activate')
    else:
        python_path = os.path.join(venv_path, 'bin', 'python')
        activate_path = os.path.join('.', 'venv', 'bin', 'activate')
    
    # Install requirements
    if not install_requirements(python_path):
        return False
    
    return activate_path

if __name__ == "__main__":
    try:
        create_env_file()
        activate_path = setup_venv()
        if activate_path:
            print_color("🚀 Setup complete! You're ready to start exploring LLMs!", Fore.GREEN)
            print_color("\nTo activate the virtual environment:", Fore.LIGHTYELLOW_EX)
            if platform.system() == 'Windows':
                print_color(f"    {activate_path}", Fore.LIGHTYELLOW_EX)
            else:
                print_color(f"    source {activate_path}", Fore.LIGHTYELLOW_EX)
        else:
            raise Exception("Setup failed")
    except Exception as e:
        print_color(f"⚠️ An error occurred during setup: {str(e)}", Fore.RED)
        print_color("Check the 'setup_log.txt' file for detailed error information.", Fore.YELLOW)
        logging.error(f"Error details:\n{traceback.format_exc()}")
        
        # Write log to file
        with open('setup_log.txt', 'w') as log_file:
            log_file.write(log_stream.getvalue())