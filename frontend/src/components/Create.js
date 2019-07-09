import React, {Component} from 'react'
import Alert from './Alert'
import Fetch from '../lib/Fetch'

class Create extends Component {

    state = {
        fields : {
            job: '',
            arguments: ''
        },
        errors: {
            arguments: ''
        },

        showalert: false,
        alert_type:'',
        alert_message:'',
        jobs: [],
        job_help: []
    }

    props = {
        fields: {
            arguments: '[{"id": "12345", "created_by": "5678"}]'
        }
    }

    componentDidMount = ()=> {
        Fetch.handlers((data)=>{
            this.setState({'jobs':data})
            if (data.length > 0) {
                this.setState({
                    'job_help': data[0]['arguments'],
                })

                const fields = this.state.fields
                fields['job'] = data[0]['name']
                this.setState({ fields })

            }
        }, (validation_err) => {
            this.showAlertMessage('danger', 'Not able to fetch jobs!')
        })
    }

    isValidJson = (json) => {
        try {
            JSON.parse(json);
            return true;
        } catch (e) {
            return false;
        }
    }

    resetFields = () => {
        const fields = this.state.fields
        for (var el in fields) {
            fields[el] = ''
        }
        this.setState({ fields })
    }

    validate = () => {
        const err = {}
        console.log(this.state.fields)
        if (!this.isValidJson(this.state.fields.arguments)) {
            err['arguments'] = 'Invalid JSON!';
        }
        return err
    }

    onFormSubmit = (evt) => {
        
        const errors = this.validate();
        this.setState({errors});
        
        if (Object.keys(errors).length) {
            this.showAlertMessage('danger', 'Validation Failed!')
            evt.preventDefault();
            return;
        }

        let postFields = this.state.fields;
        //postFields = {"arguments":'[{"data":"data"}]'}
        Fetch.post(postFields, (data)=>{
            console.log(data)
            if ('status' in data && data['status']==='error') {
                this.showAlertMessage('danger', data['message'])
            } else {
                this.showAlertMessage('success', 'Successfully Added')
            }
        }, (validation_err) => {
            this.showAlertMessage('danger', validation_err.message)
        })

        evt.preventDefault();
    }

    showAlertMessage = (type, message)=>{
        this.setState({showalert:true, alert_type:type, alert_message:message})

        setTimeout(()=>{
            this.setState({showalert:false})
        }, 3000)
    }

    onInputChange = (evt) => {
        const fields = this.state.fields
        fields[evt.target.name] = evt.target.value
        this.setState({ fields })

        if (evt.target.name === 'job') {
            const job_arguments = this.state.jobs
            let selected_job_arg = job_arguments.filter( 
                job => evt.target.value === job.name
            )
            if (selected_job_arg.length > 0) {
                this.setState({job_help: selected_job_arg[0]['arguments']})
                //console.log(this.state.job_help[0])
            }
        }
    }

    render() {
        return(
            <form onSubmit={this.onFormSubmit}>
                <div className="card">
                    <div className="card-header"><span>Add Queues</span> <Alert isActive={this.state.showalert} type={this.state.alert_type} message={this.state.alert_message} /> </div>
                    <div className="card-body">
                        
                        <div className="form-group">
                            <label htmlFor="sel1">Job Name:</label>
                            <select name="job" onChange={this.onInputChange} className="form-control" id="sel1">
                            {this.state.jobs.map((job,i)=>
                                <option data-args={job.arguments} key={i} value={job.name}>{job.name.slice(0, -3)}</option>
                            )}
                            </select>
                        </div>
                        
                        <div className="form-group">
                            <label htmlFor="comment">Arguments [JSON Format] <span style={{ color: 'red' }}>{ this.state.errors.arguments }</span></label>
                            <textarea value={this.state.fields.arguments} name="arguments" onChange={this.onInputChange} className="form-control" rows="5" id="comment"></textarea>
                            {/*<span>{this.props.fields.arguments}</span>*/}
                            <span>Accepts: {(this.state.job_help.length ? this.state.job_help.join(',') : '*')}</span>
                        </div>
                        <div className="form-group">
                        <input type="submit" value="Submit" className="btn btn-primary"></input>
                        </div>
                    </div> 
                </div>
            </form>
        )
    }
}

export default Create
