<script>
	import Loading from './Loading.svelte';

	let isLoading = true;
	setTimeout(() => {
		isLoading = false;
	}, 2000); // Replace this with your actual data loading logic
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

{#if isLoading}
  <!-- Display the loading screen when isLoading is true -->
  <Loading />
{:else}
  <section>
    <!-- Content that remains when isLoading is false -->
    <h2>
      try editing <strong>src/routes/+page.svelte</strong>
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

	h1 {
		width: 100%;
	}
</style>
