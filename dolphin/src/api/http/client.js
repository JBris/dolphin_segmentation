import axios from 'axios'

class Client {
    async get(url, asJson = true) {
        if (asJson) return axios.get(url).then(res => res.data)
        else return axios.get(url)
    }

    async put(url, body = {}, asJson = true) {
        if (asJson) return axios.put(url, body).then(res => res.data)
        else return axios.post(url, body)
    }

    async post(url, body = {}, asJson = true) {
        if (asJson) return axios.post(url, body).then(res => res.data)
        else return axios.post(url, body)
    }
}

const client = new Client()
export default client
