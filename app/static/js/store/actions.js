import Axios from "axios";
import Promise from "promise";
import Qs from "qs";
import Transform from "./transform";


export default {
  /* Verifies the user's credentials and then loads the user's data */
  login({ commit, dispatch }, data) {
    return new Promise((resolve, reject) => {
      if(data.remember_me !== true)
        delete data["remember_me"];

      Axios.post(API.session, Qs.stringify(data))
      .then((resp) => {
        commit("login", Transform.user(resp.data.user));
        resolve();
      })
      .catch((err) => reject(Transform.form(err)));
    });
  },

  /* Logs the user out */
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      if(!state.loggedIn) {
        resolve();
        return;
      }

      Axios.delete(API.session)
      .then((resp) => {
        commit("logout");
        resolve();
      })
      .catch((err) => {
        console.error(err)
        reject();
      });
    });
  },

  /* Retrieves the user's current active session (if there is one) */
  getCurrentSession({ commit, dispatch }) {
    return new Promise((resolve, reject) => {
      Axios.get(API.session)
      .then((resp) => {
        if(resp.data.authenticated) {
          commit("login", Transform.user(resp.data.user));
        resolve();
        } else {
          resolve();
        }
      })
      .catch((err) => {
        console.error(err);
        reject();
      });
    });
  },

  /* Gets information about a user */
  getUser({ commit }, { userId }) {
    return new Promise((resolve, reject) => {
      Axios.get(API.user + userId)
      .then((resp) => {
        const user = Transform.user(resp.data.user);
        commit("addUser", user);
        resolve(user);
      })
      .catch((err) => {
        console.error(err);
        reject();
      });
    });
  },

  /* Registers the user */
  signUp({ commit }, data) {
    return new Promise((resolve, reject) => {
      Axios.post(API.user, Qs.stringify(data))
      .then((resp) => {
        resolve();
      })
      .catch((err) => reject(Transform.form(err)));
    });
  }
};