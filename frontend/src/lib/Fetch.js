
const API_URL = 'http://localhost:8000/';

class Fetch {

    constructor(url) {
        this.url = url;

    }

    get = (param, cb) => {
        fetch(this.url+ 'tasks/tasks' + param, {headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }}
        )
        .then(response => response.json())
        .then(cb)
    }

    workers = (param, cb) => {
        fetch(this.url+ 'workers' + param, {headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }}
        )
        .then(response => response.json())
        .then(cb)
    }

    stats = (param, cb) => {
        fetch(this.url+ 'stats' + param, {headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }}
        )
        .then(response => response.json())
        .then(cb)
    }


    post = (data, cb, vcb) => {

        let formData = new FormData();
        formData.append('json_data', data['json_data']);

        fetch(this.url+'bulk', {
            method: 'POST', 
            body: formData
        })
        .then(res => res.json())
        .then(cb)
        .catch(vcb);
    }
}


export default new Fetch(API_URL)