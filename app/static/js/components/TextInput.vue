<template>
  <div>
    <input
      :class="getClass"
      :type="type || 'text'"
      :value="value"
      @input="$emit('input', $event.target.value)"
      :placeholder="placeholder"
      :maxlength="maxlength"
      />

    <p class="form-error-text" v-if="fieldError">{{ fieldError }}</p>
  </div>
</template>

<script>
  export default {
    props: [
      "className",
      "fieldError",
      "maxlength",
      "placeholder",
      "type",
      "value",
    ],

    computed: {
      getClass() {
        let cls = "form-input";

        if(this.class)
          cls += " " + this.className;

        if(this.fieldError)
          cls += " form-input-error";

        return cls;
      }
    }
  };
</script>