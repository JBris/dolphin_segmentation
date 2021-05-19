<template>
  <div class="container">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'Body',
  }
</script>

<style scoped lang="css">
.container {
    padding-top: 0.5vh;
    padding-left: 1.5vw;
    padding-right: 1.5vw;
    padding-bottom: 2.5vh;
}
</style>