import React from 'react'
import {Modal} from 'react-bootstrap'
import Badge from './Badge'


class Detail extends React.Component {


    
    render() {
      return (
        <div>
          
          <Modal size="lg" centered dialogClassName="modal-90w" show={this.props.show} onHide={this.props.handleClose}>
            
                <Modal.Header closeButton>
                <Modal.Title>{this.props.job.id}</Modal.Title>
                </Modal.Header>
                

                <Modal.Body>
                <h5>
                    Status <Badge status={this.props.job.status} />
                </h5>
                <h5>
                    Result
                </h5>
                <p>{this.props.job.result}</p>
                
                <h5>Arguments</h5>
                <p>{this.props.job.json_data}</p>
            </Modal.Body>
            
          </Modal>
        </div>
      );
    }
  }
export default Detail
  