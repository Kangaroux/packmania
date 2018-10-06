<template>
  <nav class="header-nav">
    <div class="nav-links clearfix">
      <!-- LOGGED IN -->
      <template v-if="$store.state.loggedIn">
        <div class="pull-right">
          <a @click.prevent="logout">LOG OUT</a>
        </div>
      </template>

      <!-- LOGGED OUT -->
      <template v-else>
        <div class="pull-right">
          <router-link :to="{ name: 'login' }">
            LOG IN
          </router-link>
        </div>
      </template>
    </div>
  </nav>
</template>

<script>
  export default {
    data() {
      return {
        showProjectList: false
      };
    },
    methods: {
      logout() {
        this.$store.dispatch("logout")
        .then(() => this.$router.push({ name: "logout" }));
      }
    }
  }
</script>