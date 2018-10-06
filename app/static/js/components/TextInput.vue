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

    <p v-if="fieldError">ERROR: {{ fieldError }}</p>
  </div>
</template>

<script>
  export default {
    props: [
      "class",
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
          cls += " " + this.class;

        return cls;
      }
    }
  };
</script>