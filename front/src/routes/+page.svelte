<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import Loading from './Loading.svelte';
	import Camera from './Camera.svelte';
	import { onMount } from 'svelte';

    let feed = "http://10.32.212.235:5000/video_feed"; // replace with your webcam feed URL
	let isLoading = true;

	onMount(() => {
		// Check if the user came from the About page
		if (sessionStorage.getItem('cameFromAbout') === 'true') {
			isLoading = false;
			sessionStorage.removeItem('cameFromAbout'); // Clear the flag
		} else {
			setTimeout(() => {
				isLoading = false;
			}, 3000);
		}
	});
</script>


{#if isLoading}
  <!-- Display the loading screen when isLoading is true -->
  <Loading />
{:else}
  <section>
    <h2>
      <!--try editing SUP <strong>src/routes/+page.svelte</strong> -->
        <Camera feedUrl={feed} />
    </h2>
  </section>
{/if}

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}
</style>
