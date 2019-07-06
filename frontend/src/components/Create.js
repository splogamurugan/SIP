import React, {Component} from 'react'
import Alert from './Alert'
import Fetch from '../lib/Fetch'

class Create extends Component {

    state = {
        fields : {
            module: "Opportunities",
            json_data: ''
        },
        errors: {
            json_data: ''
        },

        showalert: false,
        alert_type:'',
        alert_message:''
    }

    props = {
        fields: {
            json_data: '[{"id": "12345", "created_by": "5678"}]'
        }
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
        if (!this.isValidJson(this.state.fields.json_data)) {
            err['json_data'] = 'Invalid JSON!';
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
        //postFields = {"json_data":'[{"data":"data"}]'}
        Fetch.post(postFields, (data)=>{
            console.log(data)
            if ('status' in data && data['status']==='error') {
                this.showAlertMessage('danger', data['message'])
            } else {
            this.showAlertMessage('success', 'Successfully Added')
            }
        }, (validation_err) => {
            this.showAlertMessage('danger', validation_err)
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
    }

    render() {
        return(
            <form onSubmit={this.onFormSubmit}>
                <div className="card">
                    <div className="card-header"><span>Add Tasks</span> <Alert isActive={this.state.showalert} type={this.state.alert_type} message={this.state.alert_message} /> </div>
                    <div className="card-body">
                        {/*
                        <div className="form-group">
                            <label htmlFor="sel1">Module:</label>
                            <select name="module" onChange={this.onInputChange} className="form-control" id="sel1">
                                <option value="Opportunities">Opportunities</option>
                                <option value="RevenueLineitems">Revenuelineitems</option>
                                <option value="Contacts">Contacts</option>
                            </select>
                        </div>
                        */}
                        <div className="form-group">
                            <label htmlFor="comment">Arguments[JSON Format]</label>
                            <textarea value={this.state.fields.json_data} name="json_data" onChange={this.onInputChange} className="form-control" rows="5" id="comment"></textarea>
                            {/*<span>{this.props.fields.json_data}</span>*/}
                            <span style={{ color: 'red' }}>{ this.state.errors.json_data }</span>
                        </div>
                    </div> 
                    <div className="card-footer"><input type="submit" value="Submit" className="btn btn-primary"></input></div>
                </div>
            </form>
        )
    }
}

export default Create
