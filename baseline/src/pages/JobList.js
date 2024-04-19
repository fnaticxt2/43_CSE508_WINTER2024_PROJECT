import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';


const JobList = () => {
  const [jobs, setJobs] = useState([])
  const location = useLocation();

  useEffect(() => {
    if (location.state && location.state.jobdata) {
      const jobData = location.state.jobdata;
      console.log(jobData);
      setJobs(jobData);
      console.log(jobData);
    }
  }, [location]);
  
  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Jobs</h2>
      <div className="row justify-content-center">
        <div className="col-md-6">
            
        {jobs.map((job) => {
          // Convert timestamp string to Date object
          const datetimeObj = new Date(job[9]);

          // Format the Date object
          const formattedDate = datetimeObj.toLocaleString("en-US", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false,
          });

          return (

          <div key={job[0]}>
            
          
          <a href={job[3]} target='_BLANK' className="col-md-12 mb-3" style={{color:"#000",textDecoration:'none'}}>
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{ job[7] ? ( <>{job[7]} ,</> ):( <></> )} {job[8]}</h5>
                <p className="card-text">{job[6]}<br/>Posted on: {formattedDate}</p>
              </div>
            </div>
          </a>
          <br/>
          </div>
          );
        })}
        
        </div>
      </div>
    </div>
  );
};

export default JobList;