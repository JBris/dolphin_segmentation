import client from './api/http/client'
import { HOST, OPTIONS } from './api/endpoints'

class Config {
    async get(){ 
        return client.get(`${HOST}/${OPTIONS}`)
    }

    async confirm(config) {
        return client.put(`${HOST}/${OPTIONS}`, config)
    }

    async reset() {
        return client.post(`${HOST}/${OPTIONS}`)
    }

    setHosts(config) {
        config["SERVER_HOST"] = process.env.VUE_APP_SERVER_HOST
        config["NOTEBOOK_HOST"] = process.env.VUE_APP_NOTEBOOK_HOST
        config["TASKS_HOST"] = process.env.VUE_APP_TASKS_HOST
        return config
    }
}

const config = new Config()
export default config