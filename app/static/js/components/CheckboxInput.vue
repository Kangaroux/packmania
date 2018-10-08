<template>
  <div :class="className">
    <label class="form-input-checkbox" @click="onChange">
      <input
        type="checkbox"
        :checked="value"
        @change="onChange"
        />

      <div class="fake-checkbox">
        <i class="el el-ok" v-if="value"></i>
      </div>

      <span>{{ label }}</span>
    </label>

    <p class="form-error-text" v-if="fieldError">{{ fieldError }}</p>
  </div>
</template>

<script>
  export default {
    props: [
      "className",
      "fieldError",
      "value",
      "label"
    ],

    methods: {
      onChange() {
        this.$emit('input', !this.value);
      }
    }
  };
</script>