<template>
  <div class="home">
    <h1>Welcome to the {{ appName }} app</h1>
    <br/>
    <p>
      This application will allow you to create image processing tasks to automate the process of identifying individual dolphins.
    </p>
    <router-link to="/tasks"><h3>Tasks</h3></router-link>
    <p>
      Create and dispatch image processing tasks.
    </p>
    <router-link to="/images"><h3>Images</h3></router-link>
    <p>
      View your collection of uploaded images. 
    </p>
    <router-link to="/datasets"><h3>Datasets</h3></router-link>
    <p>
      Explore your available dolphin datasets. 
    </p>
    <router-link to="/outputs"><h3>Outputs</h3></router-link>
    <p>
      Examine the results of your pipelines and view your processed images.
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
    computed: {
        appName: {
            get() {
                return this.$store.state.appName
            }
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
  color:  hsl(171, 100%, 41%) 
}

ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
