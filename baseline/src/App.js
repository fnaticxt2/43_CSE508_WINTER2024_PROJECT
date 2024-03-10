import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from "./home";  // Adjust the path accordingly
import JobList from "./pages/JobList";

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/job-list" component={JobList} />
      </Switch>
    </Router>
  );
};

export default App;
