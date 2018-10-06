<template>
  <div class="container signup-container">
    <h2>SIGN UP</h2>

    <p>
      With a Packmania account, you'll be able to...
      <ul>
        <li>upload songs and packs,</li>
        <li>participate in comments,</li>
        <li>create and share playlists,</li>
        <li>save your favorite songs and packs,</li>
        <li>...and much more!</li>
      </ul>
    </p>

    <Form :formError="formError" @submit="signup">
      <TextInput
        v-model="username"
        placeholder="username"
        :fieldError="fieldErrors.username"
        maxlength="20"
        />
      <TextInput
        v-model="email"
        placeholder="email"
        :fieldError="fieldErrors.email"
        />
      <TextInput
        v-model="password"
        placeholder="password"
        :fieldError="fieldErrors.password"
        type="password" />
      <TextInput
        v-model="confirmPassword"
        placeholder="confirm password"
        :fieldError="fieldErrors.confirmPassword"
        type="password"
        />

      <input type="submit" class="form-submit-btn" value="Create Account" />
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
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        formError: "",
        fieldErrors: {}
      }
    },

    methods: {
      signup() {
        this.$store.dispatch("signup", {
          username: this.username,
          email: this.email,
          password: this.password,
          confirmPassword: this.confirm_password
        })
        .then(() => this.$router.push({ path: "home" }))
        .catch((err) => {
          this.formError = err.formError;
          this.fieldErrors = err.fieldErrors;
        });
      }
    }
  };
</script>