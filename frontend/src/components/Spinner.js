import React, {Component} from 'react'

class Spinner extends Component {

    props = {
        spin:false
    }

    render = () => {
        return(
            <div className={"spinner-grow text-primary float-right " + ((this.props.spin) ? '' : 'd-none') } role="status">
                <span className="sr-only">Loading...</span>
            </div>
        )
    }
}

export default Spinner
