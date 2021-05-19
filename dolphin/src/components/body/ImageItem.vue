<template>
  <section>
    <div class ="image-card" @click="onSelect(file)">
      <b-image
        v-if="file.type == 'image'"
        :src="`${imagePath}/${file.file}`"
        lazy="true"
        class="image is-64x64 is-inline-block"
      ></b-image>
      <b-image
        v-if="file.type == 'dir'"
        :src="require('@/assets/images/folder.png')"
        class="image is-64x64 is-inline-block"
        ></b-image>
      <p>{{file.name}}</p>
    </div>
    
    <b-modal v-if="file.type == 'image' && isImageModalActive" v-model="isImageModalActive">
      <p class="image is-4by3">
        <img :src="`${imagePath}/${file.file}`">
      </p>
    </b-modal>
  </section>
</template>

<script>

export default {
  name: 'ImageList',
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
      if(file.type == "image") { this.isImageModalActive = !this.isImageModalActive ; }
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

