<template>
  <button
    :class="getClass"
    :type="submit ? 'submit' : 'button'"
    @click="$emit('click', $event.target)"
    >
      {{ label }}
  </button>
</template>

<script>
  export default {
    props: [ "className", "label", "submit" ],

    computed: {
      getClass() {
        return "btn " + this.className;
      }
    }
  };
</script>