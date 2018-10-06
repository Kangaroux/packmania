<template>
  <div>
    <AppNav />

    <transition name="fade">
      <router-view></router-view>
    </transition>
  </div>
</template>

<script>
  import AppNav from "~/components/AppNav";
  import Loading from "~/views/Loading";

  export default {
    components: { AppNav, Loading }
  };
</script>