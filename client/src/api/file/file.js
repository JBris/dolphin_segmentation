import client from '@/api/http/client'
import { COPY, COPY_DATA, DATASET_VIEW, ARCHIVE, VISUALISATION, SORT, DELETE } from '@/api/endpoints'

class File {    
    async copy(host, inPAth, out) {
        return client.post(`${host}/${COPY}`, {
            in: inPAth,
            out
        })
    }

    async copyData(host, inPAth, inFormat, outPath, outFormat) {
        return client.post(`${host}/${COPY_DATA}`, {
            in: inPAth,
            in_format: inFormat,
            out: outPath,
            out_format: outFormat
        })
    }

    async viewDataset(host, path, format) {
        return client.post(`${host}/${DATASET_VIEW}`, { path, format})
    }

    async archive(host, task, type, inFile, out) {
        return client.post(`${host}/${ARCHIVE}`, { task, type, in: inFile, out })
    }

    async visualise(host, file, format, method) {
        return client.post(`${host}/${VISUALISATION}`, { file, format, method })
    }

    async sort(host, file, format, out) {
        return client.post(`${host}/${SORT}`, { file, format, out })
    }

    async delete(host, files) {
        return client.delete(`${host}/${DELETE}`, {files})
    }
}

const file = new File()
export default file
