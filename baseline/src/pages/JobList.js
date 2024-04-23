import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Card, Button } from 'react-bootstrap'; // Import Bootstrap components for styling
import backgroundImage from '../assets/images/job.jpg';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const location = useLocation();

  useEffect(() => {
    if (location.state && location.state.jobdata) {
      const jobData = location.state.jobdata;
      setJobs(jobData);
    }
  }, [location]);

  return (
    <div className="background-container" style={{ backgroundImage: `url(${backgroundImage})`, backgroundSize: 'cover'}}>
      <div className="container mt-4">
        <h2 className="text-center mb-4" style={{  color: '#fff', padding: '10px' }}>List of Jobs</h2>
        <div className="row justify-content-center">
          <div className="col-md-8">
            {jobs.map((job) => {
              const datetimeObj = new Date(job[9]);
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
                <div key={job[0]} className="mb-4">
                  <Card>
                    <Card.Body>
                      <Card.Title>{job[7] ? `${job[7]}, ` : ''} {job[8]}</Card.Title>
                      <Card.Text>Experience: {job[1]}</Card.Text>
                      <Card.Text>Salary: {job[2]}</Card.Text>
                      <Card.Text>Location: {job[4]}</Card.Text>
                      <Card.Text>Posted on: {formattedDate}</Card.Text>
                      <Button variant="primary" href={job[3]} target="_blank" style={{ animation: 'rainbow-text-animation 5s infinite' }}>Apply</Button>
                    </Card.Body>
                  </Card>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobList;
