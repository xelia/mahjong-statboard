<template>
  <b-table
    :data="stats"
    :narrowed="true"
    :mobileCards="false"
  >
    <template slot-scope="props">
      <b-table-column label="Рейтинг">
        <router-link :to="`/rating/${props.row.rating.id}`">{{ props.row.rating.name }}</router-link>
      </b-table-column>
      <b-table-column label="Значение">
        <rating-value :rating="props.row.rating" :value="props.row.value"/>
      </b-table-column>
      <b-table-column label="Позиция в рейтинге">
        {{ props.row.place }}
      </b-table-column>
    </template>
  </b-table>
</template>

<script>
  import RatingValue from '@/components/RatingValue'
  export default {
    props: ['stats'],
    components: {
      RatingValue
    }
  }
</script>
