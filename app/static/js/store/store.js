import Actions from "./actions";
import Vue from "vue";
import Vuex from "vuex";


function createStore() {
  return new Vuex.Store({
    state: {
      wasRedirectedToLogin: false,

      loggedIn: false,
      user: null,

      users: {},

      ready: {
        session: false
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
      },

      logout(state) {
        state.user = null;
        state.loggedIn = false;
      },

      redirectedToLogin(state) {
        state.wasRedirectedToLogin = true;
      },

      redirectedToLoginReset(state) {
        state.wasRedirectedToLogin = false;
      },

      setReady(state, what) {
        if(state.ready[what] === undefined)
          console.error("Invalid ready component:", what);
        else
          state.ready[what] = true;
      }
    },

    actions: Actions
  });
}

export default createStore;