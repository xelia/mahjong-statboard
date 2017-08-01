<template>
  <div class="container">
    <b-table :data="players">
      <template scope="props">
        <b-table-column label="Имя">
          {{ props.row.name }}
        </b-table-column>
        <b-table-column
          v-for="rating in instance.ratings"
          :label="rating.name"
          :key="rating.id"

          sortable
        >
          <rating-value
            :value="props.row.stats[rating.id]"
            :rating="rating"
          >
          </rating-value>
        </b-table-column>
        <b-table-column
          label="asdasdsda"
          :custom-sort="function(){return -1}"
          sortable
        >
          <rating-value
            :value="props.row.stats[1]"
            rating=""
          >
          </rating-value>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
  import RatingValue from "~/components/RatingValue"
  export default {
      async asyncData({app}) {
          let instance = await app.$axios.get('/instances/1/?format=json')
          let players = await app.$axios.get('/instances/1/players/?format=json')
          return {
              instance: instance.data,
              players: players.data
          }
      },
      data() {
          return {
              instance: null,
              players: [],
          }
      },
      methods:{
          getRatingComparator(rating) {
              let res = (a, b) => {
                if(!b.stats[index.id]){
                  return 1
                }
                if(!a.stats[index.id]){
                  return -1
                }
                return a.stats[index.id].place - b.stats[index.id].place
              }
              return res
          }
      },
      components: {
        RatingValue
      }
  }
</script>
