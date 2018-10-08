<template>
  <div class="container login-container">
    <h2>LOG IN</h2>
    <Form :formError="formError" @submit="login">
      <TextInput
        type="email"
        v-model="email"
        placeholder="email"
        :fieldError="fieldErrors.email"
        />
      <TextInput
        type="password"
        v-model="password"
        placeholder="password"
        :fieldError="fieldErrors.password"
        />

      <CheckboxInput
        v-model="remember_me"
        label="Keep me logged in"
        className="remember-me"
        />

      <input type="submit" class="form-submit-btn" value="Log in" />
    </Form>

    <p class="footer-links">
      <router-link :to="{ name: 'signup' }">
        I need to create an account.
      </router-link>
      <router-link :to="{ name: 'forgot-password' }">
        I forgot my password.
      </router-link>
    </p>
  </div>
</template>

<script>
  import Form from "~/components/Form";
  import CheckboxInput from "~/components/CheckboxInput";
  import TextInput from "~/components/TextInput";

  export default {
    components: { Form, CheckboxInput, TextInput },

    data() {
      return {
        email: "",
        password: "",
        remember_me: false,

        formError: "",
        fieldErrors: {},
      };
    },

    methods: {
      /* Logs the user in and, if successful, redirects them to the projects page */
      login() {
        this.$store.dispatch("login", {
          email: this.email,
          password: this.password,
          remember_me: this.remember_me
        })
        .then(() => this.$router.push({ name: "home" }))
        .catch((err) => {
          this.formError = err.formError;
          this.fieldErrors = err.fieldErrors;
        });
      }
    }
  };
</script>