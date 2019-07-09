import React, { Component } from 'react';
import Item from './Item'
import fetchData from '../lib/Fetch'
import Detail from './Detail'

class List extends Component {
    
    props = {
        "status": "active"
    }

    state = {
        jobs : [],
        isLoading: true,
        error: false,
        detail: {
            "show": false,
            "job": {}
        }
    }

    showDetail = (job) => {
        const detail = this.state.detail
        detail['job'] = job
        detail['show'] = true
        this.setState({ detail })
    }

    handleClose = () => {
        const detail = this.state.detail
        detail['show'] = false
        this.setState({ detail })
    }

    render() {
        const {jobs, isLoading, error} =  this.state;
        if (isLoading) {
            return (<span>Loading...</span>)
        }
        if (error) {
            return <span>{error.message}</span>
        }

        if (!jobs.length) {
            return <span>No records found!</span>
        }

        return (
            <div>
            <table className="table table-striped">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Arguments</th>
                <th scope="col">Status</th>
                <th scope="col">Result</th>
                <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
            {jobs.map(job => 
                <Item onDetailClick={this.showDetail} key={job.id} {...job} />
            )}
            </tbody>
            </table>
            <Detail handleClose={this.handleClose} show={this.state.detail.show} job={this.state.detail.job} />
            </div>
        )
    }
    componentWillReceiveProps(nextProps) {
        //clearInterval(this.interval);
        //this.fetchData(this.props.status)
    }
    componentDidMount = () => {
        this.props.setLoadingHandler(true)
        this.fetch(this.props.status)
        
        this.interval = setInterval(() => { this.props.setLoadingHandler(true); this.fetch.bind(this)(this.props.status) }, 2000)
    }

    fetch(status) {
        fetchData.get(
            '?format=json&status=' + status, 
            data => {this.props.setLoadingHandler(false); this.setState({jobs: data, isLoading: false})}
        )
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }
}

export default List;