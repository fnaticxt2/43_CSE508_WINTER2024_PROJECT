import React, { useState,useCallback } from "react";
import { useHistory } from "react-router-dom";
import ReactLoading from 'react-loading';
import { Link } from "react-router-dom";
import {useDropzone} from 'react-dropzone'
import Dropzone from 'react-dropzone'
import { Hourglass } from 'react-loader-spinner'

const FileUpload = () => {
  const history = useHistory();
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingApp, setLoadingApp] = useState(false)

  const onDrop = useCallback(acceptedFiles => {
    handleUpload(acceptedFiles)
  }, [])
  const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})
/*
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };
*/
  const handleUpload = (acceptedFiles) => {
    /*
    if (!selectedFile) {
      alert("Please choose a file before uploading.");
      return;
    }
*/
    const formData = new FormData();
    formData.append("resume", acceptedFiles[0]);
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

            <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            Job Portal
          </Link>
        </div>
      </nav>
      <div className="container mt-4">
        <div className="row">
      

        <div {...getRootProps()} style={{flex:1, width:"100%", height:200,display:'flex',alignItems: 'center', justifyContent: 'center',backgroundColor:'rgb(219, 219, 219)',border: '2px dashed rgb(172, 172, 172)',color:'rgb(119, 119, 119)'}}>
      <input {...getInputProps()} />
      {
        <p>Drop the resume here ...</p>
      }
    </div>

    


    </div> 
    </div> 

    
{
    loadingApp ? (
            <div
              style={{ flex: 1, width:'100%',height:'100vh',display:'flex',top:'0px',left:'0px',backgroundColor:'rgba(255, 255, 255, 0.6)',position:'fixed',alignItems: 'center', justifyContent: 'center' }}>
              <div><div style={{display:'flex',justifyContent:'center'}}>
              <Hourglass
  visible={true}
  height="80"
  width="80"
  ariaLabel="hourglass-loading"
  wrapperStyle={{}}
  wrapperClass=""
  colors={['#000', '#444']}
  />
              </div><br/>
              <div>
  Fetching Jobs...</div>
  </div>
  </div>
  ) : (
    <></>
  )
}
    </>
  );
};

export default FileUpload;