import subprocess
import sys

# List of packages to be installed
packages = [
    'rsa',
    'bleach',
    'numpy',
    'requests',
    'whois',
    'xgboost==2.0.3',
    'customtkinter',
    'pillow',
    'tk',
    're,',
    'collections',
    'urllib',
    'ipaddress',
    'customtkinter',
    'PIL',
    'select',
    'pyperclip'
    
    
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    for package in packages:
        try:
            install(package)
            print(f'Successfully installed {package}')
        except subprocess.CalledProcessError:
            print(f'Failed to install {package}')

if __name__ == "__main__":
    main()
