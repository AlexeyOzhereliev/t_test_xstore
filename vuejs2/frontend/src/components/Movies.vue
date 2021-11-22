<template>
  <div>
    <b-table striped hover :items="movies" :fields="fields"></b-table>
  </div>
</template>

<script>
export default {
  name: 'Movies',
  props:["movies"],
  data() {
    return {
      fields: ["genre", 'movies_count', 'avg_rating'],
    }
  }
}
</script>

