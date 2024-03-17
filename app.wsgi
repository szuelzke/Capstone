#!/usr/bin/python3
import sys
sys.path.insert(0,'/usr/bin/python3')

from main import app as application

if __name__ == "__main__":
    application.run(debug=True)