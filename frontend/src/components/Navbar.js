import React, {Component} from 'react'
import PropTypes from 'prop-types';
import Navitem from './Navitem'

class Navbar extends Component {

    props = {
        "status":"active",
    }

    handleStatus =  (status) => {
        this.props.setStatusHandler(status)
    }

    clickHandler = () => {
        this.props.setLoadingHandler(true)
    }
    

    render() {
        const navitems = [
            {"itemId": "active", "itemName":"Active"},
            {"itemId": "started", "itemName":"Started"},
            {"itemId": "finished", "itemName":"Finished"},
            {"itemId": "failed", "itemName":"Failed"}
        ]
        return (
            <ul className="nav nav-pills card-header-pills float-left">
                {navitems.map( item => 
                    <Navitem onClickHandler={this.clickHandler} key={item.itemId} handleStatus={this.handleStatus} status={this.props.status} {...item} />
                )}
            </ul>
        )
    }
}

Navbar.propTypes = {
    "setStatusHandler": PropTypes.any.isRequired
}

export default Navbar