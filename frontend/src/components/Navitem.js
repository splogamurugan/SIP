import React, {Component} from 'react'


class Navitem extends Component {
    props = {
        itemName : "Active",
        itemId : "active",
        status: "active" 
    }

    clickHandler = () => {
        this.props.handleStatus(this.props.itemId)
        this.props.onClickHandler()
    }

    render = () => (
        <li className="nav-item">
            <a href="#" onClick={this.clickHandler} className={(this.props.status === this.props.itemId) ? 'nav-link active' : 'nav-link' }>
            {this.props.itemName}&nbsp;
            <span className={"badge badge-" + ((this.props.status === this.props.itemId) ? 'light' : 'primary') }>{this.props.count}</span>
            </a>
        </li>
    )
}

export default Navitem