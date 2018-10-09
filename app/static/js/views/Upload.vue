<template>
  <div class="container modal-container modal-sm">
    <h2>UPLOAD</h2>
    <p>What are you uploading?</p>

    <Button className="btn-blue btn-block" label="Song" />
    <Button className="btn-blue btn-block" label="Pack" />
  </div>
</template>

<script>
  import Button from "~/components/Button";

  export default {
    components: { Button }
  };
</script>