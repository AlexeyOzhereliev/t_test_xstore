<template>
  <div>
    <b-table striped hover :items="actors" :fields="fields"></b-table>
  </div>
</template>

<script>
export default {
  name: 'Actors',
  props:["actors"],
  data() {
    return {
      fields: ["actor_name", 'movies_count', 'best_genre'],
    }
  }
}
</script>
