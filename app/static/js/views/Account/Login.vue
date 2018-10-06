<template>
  <div>
    <h1>Login page</h1>
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

      <input type="submit" value="Log in" />
    </Form>
  </div>
</template>

<script>
  import Form from "~/components/Form";
  import TextInput from "~/components/TextInput";

  export default {
    components: { Form, TextInput },

    data() {
      return {
        email: "",
        password: "",
        formError: "",
        fieldErrors: {},
      };
    },

    methods: {
      /* Logs the user in and, if successful, redirects them to the projects page */
      login() {
        this.$store.dispatch("login", {
          email: this.email,
          password: this.password
        })
        .then(() => this.$router.push({ path: "projects" }))
        .catch((err) => {
          this.formError = err.formError;
          this.fieldErrors = err.fieldErrors;
        });
      }
    }
  };
</script>