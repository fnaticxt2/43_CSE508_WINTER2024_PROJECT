import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Home = () => {
  const [inputJob, setInputJob] = useState("");
  const [selectedJob, setSelectedJob] = useState("");
  const [jobs, setJobs] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [suggestedJobs, setSuggestedJobs] = useState([]);
  const [resumeFile, setResumeFile] = useState(null);

  useEffect(() => {
    const jobList = ["Software Engineer", "Data Scientist", "Graphic Designer", "Marketing Specialist"];
    setJobs(jobList);
  }, []);

  useEffect(() => {
    const suggestions = jobs.filter((job) =>
      job.toLowerCase().includes(inputJob.toLowerCase())
    );
    setSuggestedJobs(suggestions);
  }, [inputJob, jobs]);

  useEffect(() => {
    const defaultCompanies = {
      "Software Engineer": [
        { name: "IBM", website: "https://www.ibm.com/" },
        { name: "Microsoft", website: "https://www.microsoft.com/" },
        { name: "Google", website: "https://www.google.com/" }
      ],
      "Data Scientist": [
        { name: "Microsoft", website: "https://www.microsoft.com/" },
        { name: "Google", website: "https://www.google.com/" },
        { name: "Nvidia", website: "https://www.nvidia.com/" }
      ],
      "Graphic Designer": [
        { name: "Google", website: "https://www.google.com/" },
        { name: "Nvidia", website: "https://www.nvidia.com/" }
      ],
      "Marketing Specialist": [
        { name: "Jio", website: "https://www.jio.com/" },
        { name: "Microsoft", website: "https://www.microsoft.com/" }
      ],
    };
    setCompanies(defaultCompanies[selectedJob] || []);
  }, [selectedJob]);

  const handleJobChange = (job) => {
    setInputJob("");
    setSelectedJob(job);
  };

  const handleSuggestionClick = (suggestedJob) => {
    setInputJob(suggestedJob);
    setSuggestedJobs([]);
  };

  const handleSubmit = () => {
    setSelectedJob(inputJob);
  };

  const handleResumeUpload = (event) => {
    const file = event.target.files[0];
    setResumeFile(file);
  };

  const handleUpload = () => {
    if (!resumeFile) {
      alert("Please choose a resume file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);

    fetch("http://your-server-endpoint/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Upload successful:", data);
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
      });
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-fluid">
          <Link className="navbar-brand" to="#">
            Job Portal
          </Link>
        </div>
      </nav>

      <div className="container mt-4">
        <div className="row">
          <div className="col-md-6">
            <form className="input-group">
              <input
                className="form-control"
                type="search"
                placeholder="Search for a job..."
                aria-label="Search"
                value={inputJob}
                onChange={(e) => setInputJob(e.target.value)}
              />
              <button
                className="btn btn-outline-success"
                type="button"
                onClick={handleSubmit}
              >
                Search
              </button>
            </form>

            {suggestedJobs.length > 0 && (
              <div className="mt-3">
                <p>Did you mean:</p>
                <div className="btn-group">
                  {suggestedJobs.map((suggestedJob) => (
                    <button
                      key={suggestedJob}
                      className="btn btn-outline-secondary"
                      type="button"
                      onClick={() => handleSuggestionClick(suggestedJob)}
                    >
                      {suggestedJob}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {selectedJob && (
              <div className="mt-3">
                <h4>List of Companies for {selectedJob}:</h4>
                {companies.length > 0 ? (
                  <ul className="list-group">
                    {companies.map((company) => (
                      <li key={company.name} className="list-group-item">
                        <a
                          href={company.website}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          {company.name}
                        </a>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No companies found for {selectedJob}.</p>
                )}
              </div>
            )}
          </div>

          <div className="col-md-6">
            <div className="mt-3">
              <label htmlFor="resumeUpload" className="form-label">
                Upload Resume:
              </label>
              <div className="input-group">
                <input
                  type="file"
                  className="form-control"
                  id="resumeUpload"
                  onChange={handleResumeUpload}
                  style={{ display: "none" }}
                />
                <label htmlFor="resumeUpload" className="btn btn-primary">
                  Choose File
                </label>
                {resumeFile && (
                  <p className="ml-2">Selected file: {resumeFile.name}</p>
                )}
              </div>
            </div>

            <div className="mt-3">
              <button
                className="btn btn-success"
                onClick={handleUpload}
              >
                Upload
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
