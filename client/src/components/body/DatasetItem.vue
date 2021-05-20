<template>
  <section>
    <div class ="image-card" @click="onSelect(file)">

      <b-image
        v-if="file.type == 'dir'"
        :src="require('@/assets/images/folder.png')"
        class="image is-64x64 is-inline-block"
        ></b-image>

        <b-image
        v-if="file.type == 'csv'"
        :src="require('@/assets/images/csv.png')"
        class="image is-64x64 is-inline-block"
        ></b-image>

        <b-image
        v-if="file.type == 'json'"
        :src="require('@/assets/images/json.png')"
        class="image is-64x64 is-inline-block"
        ></b-image>

      <p>{{file.name}}</p>
    </div>
  </section>
</template>

<script>

export default {
  name: 'DatasetItem',
  props: {
    file: {
      type: Object,
      required: true
    },
  },
  methods: {
    onSelect (file) {
      if(file.type == "dir") { this.$emit('dir_selected', file); }
      if(file.type == "json" || file.type == "csv") { this.$emit('file_selected', file); }
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

