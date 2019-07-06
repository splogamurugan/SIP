import React, { Component } from 'react';
import Item from './Item'
import fetchData from '../lib/Fetch'
class List extends Component {
    
    props = {
        "status": "active"
    }

    state = {
        jobs : [],
        isLoading: true,
        error: false
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
            <div className="card-columns">
            
            {jobs.map(job => 
                <Item key={job.id} {...job} />
            )}
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