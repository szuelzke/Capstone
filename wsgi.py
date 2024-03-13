import sys
sys.path.insert(0, '/var/www/html/your_repository')

from app import app as application

if __name__ == "__main__":
    application.run()