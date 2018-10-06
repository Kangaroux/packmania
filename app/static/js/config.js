import Axios from "axios";
import Cookies from "js-cookie";
import Promise from "promise";


// Add the CSRF token to each request. We can't cache the value of the CSRF token
// because it will change when the user logs in
Axios.interceptors.request.use(
  (config) => {
    config.headers["X-CSRFToken"] = Cookies.get("csrftoken");
    return config;
  }, (error) => {
    return Promise.reject(error);
  });