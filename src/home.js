import React from "react";
import { Link } from "react-router-dom";
import FileUpload from "./pages/FileUpload";

const Home = () => {
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
          <div className="col-md-6">
            <FileUpload />
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;