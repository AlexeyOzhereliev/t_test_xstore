<template>
  <div>
    <h2>Actors</h2>
    <Actors v-bind:actors="actors"/>
  </div>
</template>

<script>
import Actors from "@/components/Actors";
export default {
  name: 'App',
  components: {
    Actors
  },
  data() {
    return {
      actors: [],
    }
  },
  mounted() {
    fetch("http://127.0.0.1:8000/GETapi/actors/")
        .then(res => res.json())
        .then(json => this.actors = json)
  }
}
</script>