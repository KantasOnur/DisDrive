import React, { useState, useEffect } from 'react';
function App() {

    const [active_request, setRequest] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [files, setFiles] = useState([])
    const [progress, setProgress] = useState(null)
    const [downloadState, setDownloadState] = useState({})
    const [deleteState, setDeleteState] = useState({})

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleFileUpload = () => {

        if (selectedFile && !active_request) {
            setRequest(true)

            const formData = new FormData();
            formData.append('file', selectedFile);
            console.log("uploading file")
            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
            .finally(() => {
                 setRequest(false)
            })
        }
        else if (selectedFile && active_request){
            console.log("There is an active request")
        }
        else {
            console.log("No file selected");
        }
    };


    useEffect(() => {
        const interval = setInterval(() => {
            fetch('/files')
                .then(res => res.json())
                .then(files => {
                    setFiles(files);
                })
                .catch(error => {
                    console.error('Error fetching files:', error);
                });

            fetch('/progress')
                .then(res => res.json())
                .then(progress => {
                    setProgress(progress['progress']);
                })
                .catch(error => {
                    console.error('Error fetching progress:', error);
                });
        }, 1000); // 500 milliseconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

    const handleFileDownload = (file) => {

        if(!active_request){

            setRequest(true)
            setDownloadState({[file.filename] : true});

            const formData = new FormData();
            formData.append('file', file.filename); // Changed to 'filename' to match server-side expectation
            console.log("downloading")
            fetch('/download', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.blob()) // Process the response as a Blob
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', file.filename); // Set the filename for the download
                link.click();
                window.URL.revokeObjectURL(url)

            })
            .catch(error => console.error('Download error:', error))
            .finally(() => {
                setRequest(false)
                setDownloadState({[file.filename]: false})
            })
        }
        else{
            console.log("active request")
        }

    };

    const handleFileDelete = (file) =>{

        if(!active_request){
            setRequest(true)
            setDeleteState({[file.filename] : true})
            const formData = new FormData();
            formData.append('file', file.filename);

            fetch('/delete', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
            .finally(() => {
                setRequest(false)
                setDeleteState({[file.filename]: false})
            })
        }
        else{
            console.log("active request in progress")
        }
    };

    return (
        <div style={{
            fontFamily: "'Trebuchet MS', sans-serif",
            margin: 0,
            padding: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center"}}>

            <div>
            {progress !== null ? (
                <div>
                    <h2>Upload Progress</h2>
                    <progress value={progress} max="100"></progress> {/* HTML5 Progress Bar */}
                    <p>{progress}%</p>
                </div>
            ) : (
                <p>No active upload.</p>
            )}
            </div>

            <input type="file" style={{marginTop: '30vh'}} onChange={handleFileChange}></input>
            <button style={{
                    fontFamily: "'Trebuchet MS', sans-serif",
                    marginRight: '10px',
                    marginTop: '10px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    padding: '10px 15px',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    fontSize: '16px'}} onClick={handleFileUpload}>Upload File</button>
            <h1>
                {files.map((file, index) => (
                    <div key={index} style={{ listStyleType: 'none', marginBottom: '20px' }}>
                        <li>{file.filename} - {file.size >= 1000**3 ? (file.size / 1000**3).toFixed(2) + ' GB' : file.size >= 1000**2 ? (file.size / 1000**2).toFixed(2) + ' MB' : (file.size / 1000).toFixed(2) + ' KB'}</li>
                        <button style={{
                        fontFamily: "'Trebuchet MS', sans-serif",
                        marginRight: '10px',
                        backgroundColor: '#4CAF50',
                        color: 'white',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '16px'
                    }} onClick={() => handleFileDownload(file)} disabled={downloadState[file.filename]}>{downloadState[file.filename] ? 'Downloading...' : 'Download'}</button>
                        <button style={{
                        fontFamily: "'Trebuchet MS', sans-serif",
                        backgroundColor: '#f44336',
                        color: 'white',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '16px'
                    }} onClick={() => handleFileDelete(file)} disabled={deleteState[file.filename]}>{deleteState[file.filename] ? 'Deleting...' : 'Delete'}</button>
                    </div>
                ))}
            </h1>
        </div>
    );
}

export default App;