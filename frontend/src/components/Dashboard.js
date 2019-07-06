import React, {Component} from 'react'
import Navbar from './Navbar'
import List from './List'
import Spinner from './Spinner'

class Dashboard extends Component {

    state = {
        "status": "active",
        "isLoading": false
    }

    setStatusHandler = (status) => {
        this.setState({"status":status})
    }

    setLoadingHandler = (loading) => {
        this.setState({'isLoading': loading})
    }

    render() {
        return (
            <div className="card">
                <div className="card-header">
                    <Navbar setLoadingHandler={this.setLoadingHandler} setStatusHandler={this.setStatusHandler} status={this.state.status} />
                    <Spinner spin={this.state.isLoading} />
                </div>
                <div className="card-body">
                    <List setLoadingHandler={this.setLoadingHandler} status={this.state.status} />
                </div>
            </div>
        )
    }

}

export default Dashboard
