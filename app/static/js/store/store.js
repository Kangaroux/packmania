import Actions from "./actions";
import Vue from "vue";
import Vuex from "vuex";


function createStore() {
  return new Vuex.Store({
    state: {
      loggedIn: false,
      user: null,

      users: {},

      ready: {
        session: false,
      }
    },

    mutations: {
      addUser(state, user) {
        Vue.set(state.users, user.id, user);
      },

      login(state, user) {
        Vue.set(state.users, user.id, user);
        state.user = user;
        state.loggedIn = true;

        this.commit("ready", "session");
      },

      logout(state) {
        state.user = null;
        state.loggedIn = false;
        state.users = {};
        state.projects = {};
      },

      ready(state, component) {
        if(state.ready[component] === undefined)
          console.error("Unknown component marked as ready:", component);

        Vue.set(state.ready, component, true);
      }
    },

    actions: Actions
  });
}

export default createStore;