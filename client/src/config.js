import client from './api/http/client'
import { OPTIONS } from './api/endpoints'

class Config {
    async get(host){ 
        return client.get(`${host}/${OPTIONS}`)
    }

    async confirm(host, config) {
        return client.put(`${host}/${OPTIONS}`, config)
    }

    async reset(host) {
        return client.post(`${host}/${OPTIONS}`)
    }
}

const config = new Config()
export default config