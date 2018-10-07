import Actions from "./actions";
import Vue from "vue";
import Vuex from "vuex";


function createStore() {
  return new Vuex.Store({
    state: {
      loggedIn: false,
      user: null,

      users: {},
    },

    mutations: {
      addUser(state, user) {
        Vue.set(state.users, user.id, user);
      },

      login(state, user) {
        Vue.set(state.users, user.id, user);
        state.user = user;
        state.loggedIn = true;
      },

      logout(state) {
        state.user = null;
        state.loggedIn = false;
      }
    },

    actions: Actions
  });
}

export default createStore;