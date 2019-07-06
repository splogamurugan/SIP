import React,  {Component} from 'react'
import fetchData from '../lib/Fetch'

class Workers extends Component {

    state = {
        workers:[]
    }

    status = {
        "idle": "secondary",
        "busy": "success"
    }

    componentDidMount = () => {
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
                                <div className={"spinner-grow text-" + this.status[worker.state] } role="status">
                                <span className="sr-only">Loading...</span>
                                </div>
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