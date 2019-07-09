import React, {Component} from 'react'

class Badge extends Component {
    props = {
        "status":""
    }
    
    statusClasses = {
        "queued":"primary", 
        "started":"success", 
        "failed": "danger",
        "finished": "primary",
        "deferred": "info"
    }

    render = ()=> {
        return(
            <span className={"badge badge-pill badge-" + (this.statusClasses[this.props.status]) }>
                {this.props.status}
            </span>
        )
    }
}

export default Badge