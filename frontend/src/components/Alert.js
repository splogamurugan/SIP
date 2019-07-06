import React, {Component} from 'react'

class Alert extends Component {

    props = {
        message : '',
        type: 'success',
        isActive: false
    }

    htmlcodes = {
        "success": '!',
        'danger': 'X'
    }


    render = ()=> {
        if (this.props.isActive) {
            return(
                <span className={"badge badge-pill float-right badge-" + (this.props.type) }>
                    {this.htmlcodes[this.props.type]} {this.props.message}
                </span>
            )
        }
        return(<span />)

    }

}

export default Alert