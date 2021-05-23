import client from '@/api/http/client'
import { SELECT, CHECK_PROGRESS, CANCEL_TASKS } from '@/api/endpoints'

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
                clearInterval(this.taskRegistry[data["task_id"]])
                $store.commit('updateTaskStatus', `${name} ${res["status"]}`) 
            } else if(res["status"] == "error") { 
                clearInterval(this.taskRegistry[data["task_id"]])
                $store.commit('updateTaskStatus', `${name} failed`) 
            }
          }, $store.state.TASK_POLLING_INTERVAL)
    }

    async cancel(host, id) {
        clearInterval(this.taskRegistry[id])
        return client.get(`${host}/${CANCEL_TASKS}/${id}`)
    }
}

const task = new Task()
export default task
