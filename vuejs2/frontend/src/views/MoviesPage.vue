<template>
  <div>
    <h2>Movies</h2>
    <Movies v-bind:movies="movies"/>
  </div>
</template>

<script>
import Movies from "@/components/Movies";
export default {
  name: 'App',
  components: {
    Movies
  },
  data() {
    return {
      movies: [],
    }
  },
  mounted() {
    fetch("http://127.0.0.1:8000/GETapi/movies/")
        .then(res => res.json())
        .then(json => this.movies = json)
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
