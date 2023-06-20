from flask import Flask, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.environ.get('MONGO_URI')  # Replace with your Atlas MongoDB URI
DB_NAME = 'logging_db'  # Replace with your database name
COLLECTION_NAME = 'logging_collection'  # Replace with your collection name

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Create the database and collection if they don't exist
if DB_NAME not in client.list_database_names():
    db.create_collection(COLLECTION_NAME)

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
