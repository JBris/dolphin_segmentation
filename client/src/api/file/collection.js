import client from '@/api/http/client'

class Collection {
    async getAll(host, endpoint, path) {
        return client.post(`${host}/${endpoint}`, {path})
    }
}

const collection = new Collection()
export default collection