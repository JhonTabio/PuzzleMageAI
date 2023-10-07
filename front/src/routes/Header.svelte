<script>
	import github from '$lib/images/github.svg';
</script>

<header>
	<div class="header-text-container">
		<div class="header-text">PuzzleMage.AI</div>
	</div>
	<div class="corner">
		<a href="https://github.com/JhonTabio/PuzzleMageAI/">
			<img src={github} alt="GitHub" />
		</a>
	</div>
</header>

<style>
	/* Add the @font-face declaration for the 'Minecraft' font */
	@font-face {
	    font-family: 'Minecraft';
	    font-style: normal;
	    font-weight: normal;
	    src: local('Minecraft'), url('Minecraft.woff') format('woff');
	}

	header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start; /* Align child items to the top */
    height: 150px; 
	padding-top: 20px;
}

.header-text-container {
    flex: 1; 
    display: flex;
    align-items: center; 
    justify-content: center;
}

.header-text {
	font-family: 'Minecraft', sans-serif;
	font-size: 100px;
	text-align: center;
	margin: 0;
}

.corner {
	/* No need for explicit width and height */
	position: absolute; /* This will position it absolutely within the header */
	top: 0; /* Place it at the top */
	right: 0; /* Place it at the right */
}

.corner a {
	display: flex;
	width: 100%;
	height: 100%;
	padding-top: 20px;

}

.corner img {
	width: 5em;
	height: 5em;
	object-fit: contain;
}

</style>
