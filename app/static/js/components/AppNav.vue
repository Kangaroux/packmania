<template>
  <nav class="header-nav">
    <router-link :to="{ name: 'home' }" class="banner">
      <img src="/static/img/banner.png" />
    </router-link>

    <div class="nav-links">
      <router-link class="nav-link nav-link-highlighted" :to="{ name: 'upload' }">
        <span>Upload</span>
      </router-link>

      <router-link class="nav-link" :to="{ name: 'songs' }">
        <span>Songs</span>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'packs' }">
        <span>Packs</span>
      </router-link>

      <!-- LOGGED IN -->
      <template v-if="$store.state.loggedIn">
        <router-link class="nav-link" :to="{ name: 'logout' }">
          <span>Log out</span>
        </router-link>
      </template>

      <!-- LOGGED OUT -->
      <template v-else>
        <router-link class="nav-link" :to="{ name: 'signup' }">
          <span>Sign Up</span>
        </router-link>
      </template>
    </div>
  </nav>
</template>

<script>
  export default {
    methods: {
      logout() {
        this.$store.dispatch("logout")
        .then(() => this.$router.push({ name: "logout" }));
      }
    }
  }
</script>