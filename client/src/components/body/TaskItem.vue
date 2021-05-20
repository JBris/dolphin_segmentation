<template>
  <section>
    <div class ="image-card" @click="onSelect(task)">

        <b-image
            v-if="task.status == 'complete'"
            :src="require('@/assets/images/task_complete.svg')"
            class="image is-64x64 is-inline-block"
        ></b-image>

        <b-image
            v-if="task.status == 'failed'"
            :src="require('@/assets/images/task_failed.svg')"
            class="image is-64x64 is-inline-block"
        ></b-image>

        <b-image
            v-else
            :src="require('@/assets/images/task_incomplete.svg')"
            class="image is-64x64 is-inline-block"
        ></b-image>

      <p>{{task.name}}</p>
      <p>{{task.status}}</p>
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
.image-card {
  transition: height 0.3s, box-shadow 0.3s;
  word-wrap: break-word;
}
.image-card:hover {
  box-shadow: 0.025em 0.025em 2.5px hsl(171, 100%, 41%);
  cursor: pointer;
}
</style>

