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
          <a v-if="$store.state.instance.id == 1" class="navbar-item" href="http://tesuji-club.ru">Клуб Тесудзи</a>
          <!--TODO: сделать нормально-->
        </div>
        <div class="navbar-end">
          <router-link to="/auth/login/" v-if="!user.authenticated" class="navbar-item">Войти</router-link>
          <div v-else class="navbar-item has-dropdown is-hoverable">
            <div class="navbar-link">
              {{ user.data.username }}
            </div>
            <div class="navbar-dropdown">
              <router-link to="/meetings/" class="navbar-item">Список встреч</router-link>
              <router-link to="/service/add-games/" class="navbar-item">Добавить игры</router-link>
              <a class="navbar-item" @click="logout()">Выход</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
  import auth from '@/utils/auth'
  export default {
    props: ['ratings'],
    data() {
      return {
        menuActive: false,
        user: auth.user,
      }
    },
    watch:{
      '$route': function(){this.menuActive = false}
    },
    methods: {
      logout(){
        auth.logout()
      }
    }
  }
</script>
