import client from './api/http/client'
import { OPTIONS } from './api/endpoints'

class Config {
    async get(){ 
        const host = process.env.VUE_APP_SERVER_HOST
        return client.get(`${host}/${OPTIONS}`)
    }
}

const config = new Config()
export default config