<template>
  <div>
    <p v-if="formError">ERROR: {{ formError }}</p>
    <form @submit.prevent="$emit('submit', $event.target)">
      <slot></slot>
    </form>
  </div>
</template>

<script>
  export default {
    props: [ "formError", "submit" ]
  };
</script>