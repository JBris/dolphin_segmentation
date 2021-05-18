import axios from 'axios'

class Client {
    async get(url, asJson = true) {
        if (asJson) return axios.get(url).then(res => res.data)
        else return axios.get(url)
    }
}

const client = new Client()
export default client
