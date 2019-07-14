import React, {Component} from 'react'
import Badge from './Badge'

class Item extends Component{

    props = {
        "onDetailClick": null
    }

    constructor(props) {
        super(props)
        
    }

    onDetailClick = () => {
        this.props.onDetailClick(this.props)
    }

    render() {
        
        return (

        <tr onClick={this.onDetailClick}>
            <th scope="row">{this.props.id.slice(0, 8)}</th>
            <td>
                <p className="card-text">
                    {this.props.json_data.slice(0, 50)}
                </p>
            </td>
            <td>
                <Badge status={this.props.status} />
            </td>
            <td>
                {this.props.result ? this.props.result.slice(0, 100):''}
            </td>
            <td>
                <a href="#"  className="badge badge-pill badge-danger">X </a>
                
            </td>
        </tr>

            

        )
    }
}

export default Item