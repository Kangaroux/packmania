<template>
  <div>
    <p class="form-error-text" v-if="formError">{{ formError }}</p>
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