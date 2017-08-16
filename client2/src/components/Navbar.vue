<template>
  <nav class="navbar has-shadow">
    <div class="container">
      <div class="navbar-brand">
        <div @click="menuActive=!menuActive" class="navbar-burger burger" data-target="navMenu">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
      <div class="navbar-menu" :class="{'is-active': menuActive}" id="navMenu">
        <div class="navbar-start">
          <router-link to="/games" class="navbar-item">Игры</router-link>
          <div v-if="ratings" class="navbar-item has-dropdown is-hoverable">
            <router-link to="/" class="navbar-link">
              Рейтинг
            </router-link>
            <div class="navbar-dropdown">
              <router-link v-for="rating in ratings" class="navbar-item" :to="`/rating/${rating.id}`" :key="rating.id">
                {{ rating.name }}
              </router-link>
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <router-link to="/auth/login/" v-if="!user" class="navbar-item">Войти</router-link>
          <div v-else class="navbar-item has-dropdown is-hoverable">
            <div class="navbar-link">
              {{ user.username }}
            </div>
            <div class="navbar-dropdown">
              <router-link to="/service/add-games/" class="navbar-item">Добавить игры</router-link>
              <router-link to="/auth/logout/" class="navbar-item">Выход</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
  export default {
    props: ['ratings', 'user'],
    data() {
      return {
        menuActive: false
      }
    }
  }
</script>
