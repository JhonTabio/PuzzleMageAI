<script>
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import Loading from './Loading.svelte';

	import { onMount } from 'svelte';

	let isLoading = true;

	onMount(() => {
		// Check if the user came from the About page
		if (sessionStorage.getItem('cameFromAbout') === 'true') {
			isLoading = false;
			sessionStorage.removeItem('cameFromAbout'); // Clear the flag
		} else {
			setTimeout(() => {
				isLoading = false;
			}, 2000);
		}
	});
</script>


{#if isLoading}
  <!-- Display the loading screen when isLoading is true -->
  <Loading />
{:else}
  <section>
    <h2>
      try editing SUP <strong>src/routes/+page.svelte</strong>
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
