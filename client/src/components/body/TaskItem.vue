<template>
  <section>
    <div class ="image-card" @click="onSelect(task)">

        <img
            v-if="task.status == 'complete'"
            :src="require('@/assets/images/task_complete.svg')"
            lazy
            class="image is-64x64 is-inline-block"
        /> 

        <img
            v-else-if="task.status == 'failed'"
            :src="require('@/assets/images/task_failed.svg')"
            lazy
            class="image is-64x64 is-inline-block"
        /> 

        <img
            v-else
            :src="require('@/assets/images/task_incomplete.svg')"
            lazy
            class="image is-64x64 is-inline-block"
        /> 

      <p>{{task.name}}</p>
      <p class="task-status">{{task.status}}</p>
    </div>
  </section>
</template>

<script>

export default {
  name: 'TaskItem',
  props: {
    task: {
      type: Object,
      required: true
    },
  },
  methods: {
    onSelect(task) {
      this.$emit('task_selected', task)
    }
  }
}
</script>

<style scoped lang="css">
.task-status {
  text-transform:capitalize;
}

.image-card {
  transition: height 0.3s, box-shadow 0.3s;
  word-wrap: break-word;
}
.image-card:hover {
  box-shadow: 0.025em 0.025em 2.5px hsl(171, 100%, 41%);
  cursor: pointer;
}
</style>

