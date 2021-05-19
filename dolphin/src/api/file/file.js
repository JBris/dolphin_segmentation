import client from '@/api/http/client'
import { COPY } from '@/api/endpoints'

class File {    
    async copy(host, inPAth, inFormat, outPath, outFormat) {
        return client.post(`${host}/${COPY}`, {
            in: inPAth,
            in_format: inFormat,
            out: outPath,
            out_format: outFormat
        })
    }
}

const file = new File()
export default file
