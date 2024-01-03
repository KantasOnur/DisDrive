from flask import Flask, jsonify, request, after_this_request, send_file
import os
import json
from math import ceil
import sqlite3

# Constants
ATTACHMENT_SIZE = 25000000
DATABASE_FILE = 'files.db'
# Initialize Flask app
app = Flask(__name__)
upload_progress = {}
requested_file = {}


def writeChunkFile(file_name, chunk_num, chunk_contents):
    """
    Writes a chunk of file and returns the chunk file name.
    """
    chunk_file = f"{file_name.split('.')[0]}_{chunk_num}.txt"
    with open(chunk_file, "wb") as out_f:
        out_f.write(chunk_contents)

    return chunk_file


def fileExists(upload_filename):
    with sqlite3.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM files WHERE filename=?", [upload_filename])

        return cur.fetchone() is not None


@app.route("/files", methods=['GET'])
def listFiles():
    with sqlite3.connect(DATABASE_FILE) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        rows = cur.execute("SELECT DISTINCT filename, size from files").fetchall()
        return jsonify([dict(ix) for ix in rows])


@app.route('/progress', methods=['GET'])
def getProgress():
    """
    Progress is updated everytime a chunk is uploaded.
    """
    if 'progress' in upload_progress:
        return jsonify({'progress': ceil(upload_progress['progress'])})
    return jsonify({'progress': None})


def sendReqToBot(requestType, filename, size, chunkid, num_chunks):
    with open('message.json', 'w') as json_file:
        json.dump({
            "requestType": requestType,
            "filename": filename,
            "size": size,
            "chunkid": chunkid,
            "totalchunks": num_chunks
        }, json_file)


def waitForBot():
    while os.path.exists('message.json'):
        continue


@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and fileExists(file.filename):
        return jsonify({'error': 'File already exists'}), 409

    file_contents = file.read()
    num_chunks = ceil(len(file_contents) / ATTACHMENT_SIZE)
    bytes_uploaded = 0

    upload_progress['progress'] = 0  # Initialize progress

    for chunkid in range(num_chunks):
        first_byte = chunkid * ATTACHMENT_SIZE
        chunk_contents = file_contents[first_byte:first_byte + ATTACHMENT_SIZE]
        writeChunkFile(file.filename, chunkid, chunk_contents)

        sendReqToBot("upload", file.filename, len(file_contents), chunkid, num_chunks)
        waitForBot()

        bytes_uploaded += len(chunk_contents)
        upload_progress['progress'] = (bytes_uploaded / len(file_contents)) * 100

    del upload_progress['progress']
    return jsonify({'message': 'File uploaded and read successfully'})


@app.route('/download', methods=['POST'])
def downloadFile():
    filename = request.form['file']
    sendReqToBot("download", filename, [], None, None)
    waitForBot()

    @after_this_request
    def cleanup(response):
        os.remove(filename)
        return response

    return send_file(filename, as_attachment=True)


@app.route("/delete", methods=['POST'])
def deleteFile():
    filename = request.form['file']
    sendReqToBot("delete", filename, [], None, None)
    waitForBot()

    return jsonify({"message": f"{filename} is deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=4000)
