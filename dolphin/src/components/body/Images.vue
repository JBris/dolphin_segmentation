<template>
  <section>
      <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
      <p v-if="!this.fileList.length && !this.loading">No images currently available.</p>

      <div class="columns is-multiline">
        <div v-for="(file, index) in fileList" :key=index class="column is-one-third  has-text-centered">
              <b-image
                v-if="file.type == 'image'"
                :src="`${imagePath}/${file.file}`"
                class="image is-64x64 is-inline-block"
              ></b-image>
              <b-image
                v-if="file.type == 'dir'"
                :src="require('@/assets/images/folder.png')"
                class="image is-64x64 is-inline-block"
              ></b-image>
              <p>{{file.name}}</p>
        </div>
    </div>
  </section>
</template>

<script>
import collection from '@/api/file/collection'
import { IMAGE } from '@/api/endpoints'

export default {
  name: 'Images',
  data() {
    return {
      loading: true,
      error: false,
      fileList: [],
    }
  },
  computed: {
    imagePath: {
      get() {
        return `${this.$store.state.SERVER_HOST}/${IMAGE}`
      }
    }
  },
  mounted() {
    this.getFileList()
  },
  methods: {
    async getFileList() {
      try {
        this.fileList = await collection.getAll(this.$store.state.SERVER_HOST, this.$store.state.IMAGE_DIR)
        console.log(this.fileList)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
  }
}
</script>

<style scoped lang="css">
.is-horizontal-center {
  justify-content: center;
}
</style>

