import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from './components/Dashboard'
import Create from './components/Create'
import Workers from './components/Workers'

class App extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-8">
          <Dashboard />
        </div>
        <div className="col-md-4">
          <Create />
          <br />
          <Workers />
          <br />

          <div className="card">
            <div className="card-header">Stats</div>
            <div className="card-body">Goes here</div> 
          </div>


        </div>
      </div>
    );
  }
}

export default App;
