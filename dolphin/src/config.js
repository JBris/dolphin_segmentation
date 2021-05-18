import client from './api/http/client'
import { OPTIONS } from './api/endpoints'

class Config {
    async get(){ 
        const host = process.env.VUE_APP_SERVER_HOST
        return client.get(`${host}/${OPTIONS}`)
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