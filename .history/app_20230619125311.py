from flask import Flask, request, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.environ.get('mongodb://atlas-sql-64907b19c8ebab13110f398c-wuy0l.a.query.mongodb.net/logging_db?ssl=true&authSource=admin')  # Replace with your Atlas MongoDB URI
DB_NAME = 'logging_db'  # Replace with your database name
COLLECTION_NAME = 'logging_db'  # Replace with your collection name

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Save the file to MongoDB
        file_id = collection.insert_one({'filename': file.filename, 'data': file.read()}).inserted_id

        return f'File uploaded with ID: {file_id}'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
