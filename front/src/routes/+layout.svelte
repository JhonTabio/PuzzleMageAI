<script>
	import Header from './Header.svelte';
	import './styles.css';
</script>

<div class="app">
	<Header />

	<main>
		<slot />
	</main>

	<footer>
		<p>
			<a href="/" rel="prefetch">Home</a> | <a href="/about" rel="prefetch">About</a>
		</p>
	</footer>
	
	<!-- Add the image tag at the bottom of your .app div -->
	<img src="wizard.png" alt="Description of Image" class="corner-image"/>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		position: relative; /* Add relative positioning to .app to position image absolutely within it */
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	footer a {
		font-weight: bold;
	}

	/* Styles for the corner image */
	.corner-image {
		position: fixed; /* changed from absolute to fixed */
		bottom: 0;
		left: 0;
		width: 150px; /* adjust the size as needed */
		height: auto;
		z-index: 10;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
