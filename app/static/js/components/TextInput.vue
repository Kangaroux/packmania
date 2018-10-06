<template>
  <div>
    <input
      :type="type || 'text'"
      :value="value"
      @input="$emit('input', $event.target.value)"
      :placeholder="placeholder"
      />

    <p v-if="fieldError">ERROR: {{ fieldError }}</p>
  </div>
</template>

<script>
  export default {
    props: [ "value", "placeholder", "fieldError", "type" ]
  };
</script>