<template>
  <nav class="navbar has-shadow">
    <div class="navbar-brand">
      <div @click="menuActive=!menuActive" class="navbar-burger burger" data-target="navMenu">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
    <div class="navbar-menu" :class="{'is-active': menuActive}" id="navMenu">
      <div class="navbar-start">
        <nuxt-link to="/games" class="navbar-item">Игры</nuxt-link>
        <div v-if="ratings" class="navbar-item has-dropdown is-hoverable">
          <nuxt-link to="/" class="navbar-link">
            Рейтинг
          </nuxt-link>
          <div class="navbar-dropdown">
            <nuxt-link v-for="rating in ratings" class="navbar-item" :to="`/rating/${rating.id}`" :key="rating.id">
              {{ rating.name }}
            </nuxt-link>
          </div>
        </div>
      </div>
      <div class="navbar-end">
        <nuxt-link to="/auth/login/" v-if="!user" class="navbar-item">Login</nuxt-link>
        <nuxt-link to="/auth/logout/" v-else class="navbar-item">Logout</nuxt-link>
      </div>
    </div>
  </nav>
</template>
<script>
  import NuxtChild from "../.nuxt/components/nuxt-child";
  import NuxtLink from "../.nuxt/components/nuxt-link";

  export default {
    components: {
      NuxtLink,
      NuxtChild
    },
    props: ['ratings', 'user'],
    data() {
      return {
        menuActive: false
      }
    }
  }
</script>
