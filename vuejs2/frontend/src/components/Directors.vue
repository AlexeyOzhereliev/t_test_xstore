<template>
  <div>
    <b-table-simple hover small caption-top responsive>
      <colgroup>
        <col>
        <col>
      </colgroup>
      <colgroup>
        <col>
        <col>
        <col>
      </colgroup>
      <colgroup>
        <col>
        <col>
      </colgroup>
      <b-thead head-variant="dark">
        <b-tr>
          <b-th>Director name</b-th>
          <b-th colspan="3">Favourite's actors and movies  count</b-th>
          <b-th>Best movies</b-th>
        </b-tr>
      </b-thead>
      <b-tbody>
        <b-tr v-for="director in directors" v-bind:key="director.director_name">
          {{director.director_name}}
          <b-td v-for="favourite_actors in director.favourite_actors" v-bind:key="favourite_actors.name">
            {{favourite_actors.name}}, {{favourite_actors.movies_count}}
          </b-td>
          <b-td v-for="best_movies in director.best_movies" v-bind:key="best_movies">
            {{best_movies}}
          </b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>
  </div>
</template>

<script>
export default {
  name: 'Directors',
  props:["directors"],
}
</script>
