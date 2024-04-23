import React, { useState, useCallback } from "react";
import { useHistory } from "react-router-dom";
import { useDropzone } from 'react-dropzone';
import { Hourglass } from 'react-loader-spinner';
import background from '../assets/image/download-modified.jpg'; // Assuming the correct path to your image

const FileUpload = () => {
  const history = useHistory();
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingApp, setLoadingApp] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [resumePreviewUrl, setResumePreviewUrl] = useState(null);
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedOptions([...selectedOptions, value]);
    } else {
      setSelectedOptions(selectedOptions.filter(option => option !== value));
    }
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
    formData.append("selectedOptions", selectedOptions.join(","));
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
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        console.log("Upload successful:", data);
        setLoadingApp(false);
        setUploadedFileName(data.fileName); // Assuming the server responds with the uploaded file name
        history.push({ pathname: "/job-list", state: { jobdata: data.data } });
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        alert("Error uploading file. Please try again.");
        setLoadingApp(false); // Reset loading state on error
      });
  };

  return (
    <>
      <div className="background-container" style={{ backgroundSize: 'cover', minHeight: '100vh', padding: '0px', backgroundImage: `url(${background})`,opacity: 20 }}>
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary" style={{ marginBottom: '20px' }}>
          <div className="container-fluid text-center justify-content-center align-items-center">
            <h3 className="navbar-brand text-center" to="/" style={{ animation: 'rainbow-text-animation 5s infinite', fontSize: '24px' }}>
              Job Crawler
            </h3>
          </div>
        </nav>
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-md-8">
              <div className="card shadow">
                <div className="card-body">
                  <h3 className="card-title"  >Upload Resume</h3>
                  <div {...getRootProps()} style={{ height: 100, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgb(240, 240, 240)', border: '2px dashed rgb(172, 172, 172)', color: 'rgb(80, 80, 80)', padding: '20px', borderRadius: '8px' }}>
                    <input {...getInputProps()} />
                    {
                      isDragActive ?
                        <p>Drop the resume here ...</p> :
                        <p>Drag and drop your resume file here, or click to browse.</p>
                    }
                  </div>
                  <div className="mt-3 text-center">
                    <button className="btn btn-primary" onClick={() => document.getElementById('file-input').click()}>Browse</button>
                    <input type="file" id="file-input" className="d-none" onChange={(e) => {
                      setSelectedFile(e.target.files[0]);
                      setResumePreviewUrl(URL.createObjectURL(e.target.files[0]));
                    }} />
                    {selectedFile && (
                      <div className="mt-3">
                        <p className="text-center">Selected file: {selectedFile.name}</p>
                        <button className="btn btn-primary" onClick={handleUpload} style={{ backgroundColor: '#28a745', borderColor: '#28a745' }}>Submit</button>
                      </div>
                    )}
                  </div>
                  <div className="mt-4">
                    <h3>Select your options:</h3>
                    <div className="form-check">
                        <input type="checkbox" id="primary_skills" value="primary_skills" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('primary_skills')} />
                        <label htmlFor="primary_skills" className="form-check-label">Primary Skills</label>
                    </div>
                    <div className="form-check">
                      <input type="checkbox" id="secondary_skills" value="secondary_skills" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('secondary_skills')} />
                      <label htmlFor="secondary_skills" className="form-check-label">Secondary Skills</label>
                    </div>
                    <div className="form-check">
                      <input type="checkbox" id="latest_education" value="latest_education" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('latest_education')} />
                      <label htmlFor="latest_education" className="form-check-label">Latest Education</label>
                    </div>
                    <div className="form-check">
                      <input type="checkbox" id="past_experience" value="past_experience" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('past_experience')} />
                      <label htmlFor="past_experience" className="form-check-label">Past Experience</label>
                    </div>
                    <div className="form-check">
                      <input type="checkbox" id="soft_skills" value="soft_skills" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('soft_skills')} />
                      <label htmlFor="soft_skills" className="form-check-label">Soft Skills</label>
                    </div>
                    <div className="form-check">
                      <input type="checkbox" id="location" value="location" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('location')} />
                      <label htmlFor="location" className="form-check-label">Location</label>
                    </div>
                    <div className="form-check">
                      <input type="checkbox" id="hobbies" value="hobbies" className="form-check-input" onChange={handleCheckboxChange} checked={selectedOptions.includes('hobbies')} />
                      <label htmlFor="hobbies" className="form-check-label">Hobbies</label>
                    </div>  
                  </div>
                  {
                    loadingApp && (
                      <div className="mt-4 text-center">
                        <div className="progress">
                          <div className="progress-bar" role="progressbar" style={{ width: `${uploadProgress}%`, backgroundColor: '#007bff' }} aria-valuenow={uploadProgress} aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                        <p>Uploading File: {uploadedFileName}</p>
                        <div className="mt-3">
                          <Hourglass
                            visible={true}
                            height="80"
                            width="80"
                            ariaLabel="hourglass-loading"
                            colors={['#000', '#444']}
                          />
                        </div>
                      </div>
                    )
                  }
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
