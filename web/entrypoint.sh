#!/bin/bash

# Initialize the database
python init_db.py

# Start the Flask application
exec python app.py