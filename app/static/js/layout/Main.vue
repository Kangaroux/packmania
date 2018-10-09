<template>
  <div>
    <AppNav />

    <div class="container">
      <transition name="fade">
          <router-view></router-view>
      </transition>
    </div>

    <!-- Preload the elusive icons font -->
    <i class="el el-ok" style="position:absolute;z-index:-1;opacity:0;"></i>
  </div>
</template>

<script>
  import AppNav from "~/components/AppNav";
  import Loading from "~/views/Loading";

  export default {
    components: { AppNav, Loading }
  };
</script>