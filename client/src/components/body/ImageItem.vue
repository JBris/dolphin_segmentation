<template>
  <section>
    <div class ="image-card" @click="onSelect(file)">
      <img
        v-if="file.type == 'image'"
        :src="`${imagePath}/${file.file}`"
        lazy
        class="image is-64x64 is-inline-block"
      /> 

      <img
        v-if="file.type == 'dir'"
        :src="require('@/assets/images/folder.png')"
        lazy
        class="image is-64x64 is-inline-block"
        /> 

        <img
        v-if="file.type == 'zip' || file.type == 'tar'"
        :src="require('@/assets/images/archive.png')"
        lazy
        class="image is-64x64 is-inline-block"
        />

      <p>{{file.name}}</p>
    </div>
  </section>
</template>

<script>

export default {
  name: 'ImageItem',
  data() {
    return {
      isImageModalActive: false,
    }
  },
  props: {
    file: {
      type: Object,
      required: true
    },
    imagePath: {
      type: String,
      required: true
    }
  },
  methods: {
    onSelect (file) {
      if(file.type == "dir") { this.$emit('dir_selected', file); }
      else { this.$emit('file_selected', file); }
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

