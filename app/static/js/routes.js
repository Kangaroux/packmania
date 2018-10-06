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
        name: "login",
        path: "login",
        component: require("./views/Account/Login").default,
        meta: {
          title: "Log in Page"
        }
      },
      {
        name: "logout",
        path: "logout",
        component: require("./views/Account/Logout").default,
        meta: {
          title: "Log out Page"
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