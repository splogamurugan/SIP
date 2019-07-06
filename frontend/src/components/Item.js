import React, {Component} from 'react'

class Item extends Component{

    constructor(props) {
        super(props)
        this.statusClasses = {
            "queued":"info", 
            "started":"success", 
            "failed": "danger",
            "finished": "primary"
        }
    }

    render() {
        
        return (

            <div className="card bg-light mb-3">
            <div className="card-header">
                <span className={"badge badge-pill badge-" + (this.statusClasses[this.props.status]) }>
                    {this.props.status}
                </span>
                &nbsp;
                <a href="#"  className="badge badge-pill badge-danger">X</a>
            </div>
            <div className="card-body">
                <p className="card-text">
                    Result: {this.props.result}
                </p>
                <p className="card-text">{this.props.json_data.slice(0, 50)}</p>
            </div>
            </div>

        )
    }
}

export default Item