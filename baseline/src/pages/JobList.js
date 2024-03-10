import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const JobList = () => {
  const [jobs, setJobs] = useState([])
  const location = useLocation();

  useEffect(() => {
    if (location.state && location.state.jobdata) {
      const jobData = location.state.jobdata;
      setJobs(jobData);
      console.log(jobData);
    }
  }, [location]);
  
  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Jobs</h2>
      <div className="row justify-content-center">
        <div className="col-md-6">
            
        {jobs.map((job) => (
          <div key={job[0]}>
          <a href={job[8]} target='_BLANK' className="col-md-12 mb-3" style={{color:"#000",textDecoration:'none'}}>
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{job[3]}, {job[4]}</h5>
                <p className="card-text">{job[2]}, Matching: {(job[9]*100).toFixed(2)}%</p>
              </div>
            </div>
          </a>
          <br/>
          </div>
        ))}
        
        </div>
      </div>
    </div>
  );
};

export default JobList;