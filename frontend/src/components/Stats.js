import React, {Component} from 'react'

class Stats extends Component {

    props = {
        stat_items: {
            "finished_jobs": 0,
            "started_jobs":0,
            "deferred_jobs":0,
            "failed_jobs":0,
            "workers":0,
            "queued_jobs":0
        }
    }

    decors = {
        "active_jobs": ['# of Active Jobs', 'dark'],
        "queued_jobs":['# of Queued Jobs', 'primary'],
        "finished_jobs": ['# of Finished Jobs', 'light'],
        "started_jobs": ['# of Started Jobs', 'success'],
        "deferred_jobs":['# of Deferred Jobs', 'info'],
        "failed_jobs":['# of Failed Jobs', 'danger'],
        "workers":['# of Workers', 'warning'],
        
    }

    
    /*
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
    */

    render = ()=>{
        const {stat_items} = this.props

        return (
            <div className="card">
                <div className="card-header">Stats</div>
                <div className="card-body">
                {
                    Object.keys(this.decors).map((key, i)=>
                    <div key={i} className={"alert alert-"+  this.decors[key][1] } role="alert">
                        {this.decors[key][0]} <strong>{stat_items[key]}</strong>
                    </div>
                    )
                }
                </div> 
            </div>
        )
    }
}

Stats.defaultProps = {
    "stat_items": {
        "finished_jobs": 0,
        "started_jobs":0,
        "deferred_jobs":0,
        "failed_jobs":0,
        "workers":0,
        "queued_jobs":0
    }
}

export default Stats