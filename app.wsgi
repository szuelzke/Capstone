#!/usr/bin/python3
import sys
sys.path.append('/usr/lib64/python3.9/site-packages')

from main import app as application

if __name__ == "__main__":
    application.run(debug=True)