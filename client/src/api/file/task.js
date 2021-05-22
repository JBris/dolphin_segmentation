import client from '@/api/http/client'
import { SELECT, CHECK_PROGRESS } from '@/api/endpoints'

class Task {   
    
    taskRegistry = {}

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

    async registerTask(host, name, data, $store) {
        this.taskRegistry[data["task_id"]] = setInterval(async () => {
            const res = await client.get(`${host}/${CHECK_PROGRESS}/${data["task_id"]}`)
            if(res["status"] == "complete" || res["status"] == "failed") { 
                $store.commit('updateTaskStatus', `${name} ${res["status"]}`) 
                clearInterval(this.taskRegistry[data["task_id"]])
            } else if(res["status"] == "error") { 
                $store.commit('updateTaskStatus', `${name} failed`) 
                clearInterval(this.taskRegistry[data["task_id"]])
            }
          }, 5000)
    }
}

const task = new Task()
export default task
