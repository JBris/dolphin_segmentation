import client from '@/api/http/client'
import { SELECT } from '@/api/endpoints'

class Task {    
    async select(host, name, task, module, solver, type, file, out, cacheDuration, autodownload) {
        return client.post(`${host}/${SELECT}`, {
            name,
            task,
            module,
            solver,
            type,
            files : [file],
            out, 
            cache_duration: cacheDuration,
            autodownload
        })
    }
}

const task = new Task()
export default task
