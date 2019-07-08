import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from './components/Dashboard'
import Create from './components/Create'
import Workers from './components/Workers'
import Stats from './components/Stats'
import fetchData from './lib/Fetch'


class App extends Component {

  state = {
    stat_items:{}
  }

  componentDidMount = ()=>{
    fetchData.stats('', (data)=>{
        this.setState({'stat_items': data})
    })
    
    this.updateRecords = setInterval(() => {
        fetchData.stats('', (data)=>{
            this.setState({'stat_items': data})
        })
    }, 2000)
  }

  componentWillUnmount =()=>{
      clearInterval(this.updateRecords)
  }

  render() {
    return (
      <div className="row">
        <div className="col-md-8">
          <Dashboard stat_items={this.state.stat_items} />
        </div>
        <div className="col-md-4">
          <Create />
          <Workers />
          <Stats stat_items={this.state.stat_items} />
        </div>
      </div>
    );
  }
}

export default App;
