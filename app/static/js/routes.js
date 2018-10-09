import VueRouter from "vue-router";


const routes = [
  // Root level
  {
    path: "/",
    component: require("./layout/Main").default,
    children: [
      {
        name: "home",
        path: "",
        component: require("./views/Home").default,
        meta: {
          title: "Home Page"
        }
      },
      {
        name: "signup",
        path: "signup",
        component: require("./views/Account/Signup").default,
        meta: {
          title: "Sign Up Page"
        },
        beforeEnter(to, from, next) {
          next(!window.store.state.loggedIn);
        }
      },
      {
        name: "login",
        path: "login",
        component: require("./views/Account/Login").default,
        meta: {
          title: "Log in Page"
        },
        beforeEnter(to, from, next) {
          next(!window.store.state.loggedIn);
        }
      },
      {
        name: "logout",
        path: "logout",
        beforeEnter(to, from, next) {
          window.store.dispatch("logout")
          .then(() => next({ name: "login" }));
        }
      },
      {
        name: "upload",
        path: "upload",
        component: require("./views/Upload").default,
        meta: {
          title: "Upload Page",
          loginRequired: true
        }
      },
      {
        name: "songs",
        path: "songs",
        component: require("./views/Songs").default,
        meta: {
          title: "Songs Page"
        }
      },
      {
        name: "packs",
        path: "packs",
        component: require("./views/Packs").default,
        meta: {
          title: "Packs Page"
        }
      },
    ],
  },
];

const router = new VueRouter({ routes });

router.beforeEach((to, from, next) => {
  // Redirect the user to the login page if they try to visit a page and aren't
  // logged in
  if(to.meta.loginRequired && window.store.state.ready.session && !window.store.state.loggedIn) {
    window.store.commit("redirectedToLogin");
    next({ name: "login" });
  } else {
    next();
  }
});

router.afterEach((to, from) => {
  // Set the page title when the route changes
  document.title = to.meta.title;
});

export default router;