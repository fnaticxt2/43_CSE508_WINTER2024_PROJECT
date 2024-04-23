import React, { useState, useCallback } from "react";
import { useHistory } from "react-router-dom";
import { Link } from "react-router-dom";
import { useDropzone } from 'react-dropzone'
import { Hourglass } from 'react-loader-spinner';
//import backgroundImage from '../assets/images/download.jpg';

const FileUpload = () => {
  const history = useHistory();
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingApp, setLoadingApp] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [resumePreviewUrl, setResumePreviewUrl] = useState(null);

  const [selectedOptions, setSelectedOptions] = useState([]);
  const handleSelectChange = (event) => {
    const selectedValues = Array.from(event.target.selectedOptions, option => option.value);
    setSelectedOptions(selectedValues);
  };
  const onDrop = useCallback(acceptedFiles => {
    setSelectedFile(acceptedFiles[0]);
    setResumePreviewUrl(URL.createObjectURL(acceptedFiles[0])); // Generate preview URL for PDF
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleUpload = () => {
    if (!selectedFile) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("selectedOptions", selectedOptions);
    formData.append("resume", selectedFile);
    
    setLoadingApp(true);
    setUploadProgress(0); // Reset progress initially

    fetch("http://localhost:8000/upload-resume", {
      method: "POST",
      body: formData,
      onUploadProgress: (progressEvent) => {
        const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
        setUploadProgress(progress);
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Upload successful:", data);
        setLoadingApp(false);
        setUploadedFileName(data.fileName); // Assuming the server responds with the uploaded file name
        history.push({ pathname: "/job-list", state: { jobdata: data.data } });
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("Error uploading file. Please try again.");
      });
  };


  return (
    <>
      <div className="background-container" style={{ backgroundSize: 'cover', minHeight: '100vh' }}>
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
          <div className="container-fluid text-center justify-content-center align-items-center" style={{ backgroundColor: '#f8f8f8' }}>
          <h3 className="navbar-brand text-center" to="/" style={{ animation: 'rainbow-text-animation 5s infinite' }}>
              Job Crawler
          </h3>
          </div>
        </nav>
        <div className="container mt-4">
          <div className="row">
            <div className="col-md-6 offset-md-3">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Upload Resume</h5>
                  <p className="card-text">Drag and drop your resume file here, or click to browse.</p>
                  <div {...getRootProps()} style={{ flex: 1, width: "100%", height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgb(219, 219, 219)', border: '2px dashed rgb(172, 172, 172)', color: 'rgb(119, 119, 119)', padding: '20px' }}>
                    <input {...getInputProps()} />
                    {
                      isDragActive ?
                        <p>Drop the resume here ...</p> :
                        <p>Drag and drop your resume file here, or click to browse.</p>
                    }
                  </div>
                  <div className="mt-3">
                    <button className="btn btn-primary" onClick={() => document.getElementById('file-input').click()}>Browse</button>
                    <input type="file" id="file-input" className="d-none" onChange={(e) => {
                      setSelectedFile(e.target.files[0]);
                      setResumePreviewUrl(URL.createObjectURL(e.target.files[0]));
                    }} />
                    {selectedFile && (
                      <div>
                        <p>Selected file: {selectedFile.name}</p>
                        <div className="resume-preview-container">
                          <iframe src={resumePreviewUrl} className="resume-preview" title="Resume Preview" />
                        </div>
                        <button className="btn btn-primary" onClick={handleUpload}>Submit</button>
                      </div>
                    )}
                  </div>
                  <h2>Select your options:</h2>
                  <select multiple className="form-select" value={selectedOptions} onChange={handleSelectChange}>
        <option value="primary_skills" selected>Primary Skills</option>
        <option value="secondary_skills">Secondary Skills</option>
        <option value="latest_education">Latest Education</option>
        <option value="past_experience">Past Experience</option>
        <option value="soft_skills">Soft Skills</option>
        <option value="location">Location</option>
        <option value="hobbies">Hobbies</option>
      </select>
                  {loadingApp && (
                    <div style={{ marginTop: '20px' }}>
                      <p>Uploading: {uploadProgress}%</p>
                      <div className="progress">
                        <div className="progress-bar" role="progressbar" style={{ width: `${uploadProgress}%` }} aria-valuenow={uploadProgress} aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                      <p>Uploaded File: {uploadedFileName}</p>
                      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                        <Hourglass
                          visible={true}
                          height="80"
                          width="80"
                          ariaLabel="hourglass-loading"
                          wrapperStyle={{}}
                          wrapperClass=""
                          colors={['#000', '#444']}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default FileUpload;
