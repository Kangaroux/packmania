<template>
  <div>
    <AppNav />
    <router-view></router-view>
  </div>
</template>

<script>
  import AppNav from "~/components/AppNav";
  import Loading from "~/views/Loading";

  export default {
    components: { AppNav, Loading }
  };
</script>