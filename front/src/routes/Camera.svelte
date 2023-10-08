<!-- src/Camera.svelte -->
<script>
  export let feedUrl = "";
</script>

<img src={feedUrl} alt="Camera feed" />

<style>
  img {
    width: 100%; /* Adjust as needed */
    height: auto;
  }
</style>