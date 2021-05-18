import client from '@/api/http/client'
import { IMAGES } from '@/api/endpoints'

class Collection {
    async getAll(host, path) {
        return client.post(`${host}/${IMAGES}`, {path})
    }
}

const collection = new Collection()
export default collection