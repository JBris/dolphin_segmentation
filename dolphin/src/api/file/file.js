import client from '@/api/http/client'
import { COPY, DELETE } from '@/api/endpoints'

class File {    
    async copy(host, inPAth, inFormat, outPath, outFormat) {
        return client.post(`${host}/${COPY}`, {
            in: inPAth,
            in_format: inFormat,
            out: outPath,
            out_format: outFormat
        })
    }

    async delete(host, files) {
        return client.delete(`${host}/${DELETE}`, {files})
    }
}

const file = new File()
export default file
