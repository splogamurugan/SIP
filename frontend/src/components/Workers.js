import React,  {Component} from 'react'
import fetchData from '../lib/Fetch'

class Workers extends Component {

    state = {
        workers:[]
    }

    status = {
        "?": ["", "btn-secondary"],
        "idle": ["", "btn-secondary"],
        "busy": ["spinner-grow spinner-grow-sm", "btn-success"]
    }

    componentDidMount = () => {
        fetchData.workers('', (data)=>{
            this.setState({'workers': data})
        })
        
        this.timeinterval = setInterval(() => {
            fetchData.workers('', (data)=>{
                this.setState({'workers': data})
            })
        }, 2000)
    }

    componentWillUnmount = () => {
        clearInterval(this.timeinterval);
    }

    render = ()=> {
        const { workers } =  this.state;
        return (
            <div className="card">
                <div className="card-header">Workers</div>
                <div className="card-body">

                <table className="table table-striped table-sm">
                <thead>
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Running Since</th>
                    <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody>
                {
                    workers.map((worker, i)=>
                        <tr key={i}>
                            <th scope="row">{i+1}</th>
                            <td>{worker.name.slice(0,10)}</td>
                            <td>{worker.birth_date}</td>
                            <td>
                                <button className={"btn "+this.status[worker.state][1]} type="button" disabled>
                                <span className={this.status[worker.state][0]} role="status" aria-hidden="true"></span>
                                {worker.state}
                                </button>
                            </td>
                        </tr>
                    )
                }
                </tbody>
                </table>
                </div> 
            </div>
        )
    }
}

export default Workers