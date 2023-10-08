<script>
  import github from "$lib/images/github.png";
</script>

<header>
  <div class="header-text-container">
    <div class="header-text">PuzzleMage.AI</div>
  </div>
  <div class="corner">
    <a href="https://github.com/JhonTabio/PuzzleMageAI/" target="_blank">
      <img src={github} alt="Our GitHub Repository" />
    </a>
  </div>
</header>

<style>
  /* Add the @font-face declaration for the 'DragonHunter' font */
  @font-face {
    font-family: "DragonHunter";
    src: url("./static/DragonHunter.otf") format("truetype");
    font-weight: normal;
    font-style: normal;
    font-display: swap; /* Add this line */
  }

  header {
    pointer-events: none;
    display: flex;
    justify-content: space-between;
    align-items: flex-start; /* Align child items to the top */
    visibility: visible;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 25px;
    position: relative; /* Make the container relative */
    height: 5px;
    width: 100%; /* Ensure the header takes up the full width */
  }

  .header-text-container {
	pointer-events: none;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .header-text {
	pointer-events: none;
    font-family: "DragonHunter"; /* Use the custom font here */
    font-size: 25px;
    text-align: center;
    color: white;
    letter-spacing: 5px;
    margin: 0;
    padding-bottom: 10px;
  }

  .corner {
	pointer-events: none;
    position: absolute;
    top: 0;
    bottom: 0.5;
    right: 75px;
    left: 0;
  }

  .corner a {
    pointer-events: none;
    display: flex;
    padding-top: 17px;
    align-items: center;
    justify-content: right;
  }

  .corner img {
	pointer-events: auto;
    max-width: 3%; /* Adjust the max-width as needed */
    max-height: 3%; /* Adjust the max-height as needed */
    object-fit: contain;
  }
</style>
