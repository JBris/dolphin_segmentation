<template>
  <section>
      <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
      <p v-if="!this.fileList.length && !this.loading">No images currently available.</p>
      <div v-else>
      <section class="image-dir-path level-left">
        <a v-for="(dir, index) in imageDirList" :key=index @click="getFileList(joinImageDirList(imageDirList, index))">
          /{{dir}}
        </a>         
      </section>
      <section class="image-dir-path">
        <div class="columns is-multiline">
          <div v-for="(file, index) in fileList" :key=index class="column is-one-fifth  has-text-centered">
            <ImageItem v-bind:file="file" v-bind:imagePath="imagePath" v-on:dir_selected="changeDir(file)" />
          </div>
        </div>  
        </section>    
      </div>
  </section>
</template>

<script>
import collection from '@/api/file/collection'
import { IMAGE } from '@/api/endpoints'
import ImageItem from '@/components/body/ImageItem'

export default {
  name: 'Outputs',
  components: {
    ImageItem
  },
  data() {
    return {
      loading: true,
      error: false,
      imageDir: "",
      fileList: [],
    }
  },
  computed: {
    imagePath: {
      get() {
        return `${this.$store.state.SERVER_HOST}/${IMAGE}`
      }
    },
    imageDirList: {
      get() {
        return this.imageDir.split("/").filter(ele => ele != "")
      }
    },
  },
  mounted() {
    this.getFileList()
  },
  methods: {
    async getFileList(imageDir = this.$store.state.OUT_DIR) {
      this.loading = true
      try {
        this.imageDir = imageDir
        console.log(this.imageDirList )
        this.fileList = await collection.getAll(this.$store.state.SERVER_HOST, this.imageDir)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
    async changeDir(file) {
      return this.getFileList(file.file)
    },
    joinImageDirList(imageDirList, index) {
      const blah =  `/${imageDirList.slice(0, index + 1).join("/")}`
      console.log(blah)
    }
  }
}
</script>

<style scoped lang="css">
.image-dir-path {
  padding-top: 1.5vh;
  padding-bottom: 1.5vh;
}
</style>



