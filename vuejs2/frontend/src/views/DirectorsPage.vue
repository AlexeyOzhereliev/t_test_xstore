<template>
  <div>
    <h2>Directors</h2>
    <Directors v-bind:directors="directors"/>
  </div>
</template>

<script>
import Directors from "@/components/Directors";
export default {
  name: 'App',
  components: {
    Directors
  },
  data() {
    return {
      directors: [],
    }
  },
  mounted() {
    fetch("http://127.0.0.1:8000/GETapi/directors/")
        .then(res => res.json())
        .then(json => this.directors = json)
  }
}
</script>

