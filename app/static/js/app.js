import "./config";
import Vue from "vue";
import Vuex from "vuex";
import VueRouter from "vue-router";


Vue.use(Vuex);
Vue.use(VueRouter);

import router from "./routes";
import createStore from "./store/store";

window.store = createStore();
const app = new Vue({
  router,
  store
});

// Load the user's session
store.dispatch("getCurrentSession")
.then(() => {
  // If the user isn't logged in but is trying to view a restricted page then
  // send them back to the login
  if(router.currentRoute.meta.loginRequired && !store.state.loggedIn)
    router.push({ name: "login" });

  const $el = document.getElementById("app");
  $el.innerHTML = "<router-view></router-view>";

  // Destroy the loading spinner and mount the app
  document.getElementById("loading-placeholder").remove();
  app.$mount($el);
});