import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import ReactLoading from 'react-loading';

const FileUpload = () => {
  const history = useHistory();
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingApp, setLoadingApp] = useState(false)

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert("Please choose a file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", selectedFile);
    setLoadingApp(true)
    fetch("http://localhost:8000/upload-resume", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
//        console.log("Upload successful:", data);
        setLoadingApp(false)
        history.push({pathname:"/job-list",state: { jobdata: data.data }});
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("Error uploading file. Please try again.");
      });
  };

  return (
    <>
    {/*user ? (*/
        loadingApp ? (
            <div
              style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
              <div className="loader">Loading...</div>
            </div>
          ) : (
            <>
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>PDF File Upload</h2>
      <input type="file" onChange={handleFileChange} accept=".pdf" />
      {selectedFile && <p>Selected file: {selectedFile.name}</p>}
      <button onClick={handleUpload}>Upload</button>
    </div>
    </>
    )}
    </>
  );
};

export default FileUpload;