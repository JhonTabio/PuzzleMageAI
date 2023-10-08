<script>
	let text = "Goodbye World...";

	function getText(){
		fetch("./test")
		.then(p => p.text()) // Parse our promise (Expect text)
		.then(p =>(text = p)); // Manipulate our promise
	}
</script>

<main>
	<h1>{text}?</h1>
	<p>Visit the <button on:click={getText}>End this</button> to learn how to build Svelte apps.</p>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
