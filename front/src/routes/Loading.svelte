<!-- Loading.svelte -->

<script>
  let quotes = [
    "A wizard is never late, he arrives precisely when he means to.",
    "Tell me, old friend, when did you abandon wisdom for madness?",
    "Be silent. Keep your forked tongue behind your teeth. I did not pass through fire and death to bandy crooked words with a witless worm.",
    "50 points for Gryffindor... Oh wait...",
    "There is nothing you can do that I cannot simply deny.",
    "The good news is, we figured out how the wand works. The bad news is, we figured out how the wand works.",
    "If you only follow where the paths lead, you merely go where others have gone before you.",
    "I didn’t realize you’d put your finger in it…",
    "Just pay them with magic.",
    "Magic is distilled laziness. Put that on my gravestone.",
  ];

  // Function to select a random quote
  function getRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    return quotes[randomIndex];
  }

  // Initialize a variable to store the random quote
  let randomQuote = getRandomQuote();

  let loading = true;
  let loadingProgress = 0;
  let loadingCompleted = false;
  // Create a computed property to check if loading is completed
  $: loadingCompleted = loadingProgress >= 100;

  // Simulate loading process
  const loadingInterval = setInterval(() => {
    loadingProgress += 1; // Increase the progress
    if (loadingProgress >= 300) {
      // Mark loading as completed and clear the interval
      loading = false;
      clearInterval(loadingInterval);
    }
  }, 30); // 100 increments × 30 milliseconds = 3000 milliseconds = 3 seconds
</script>

{#if loading && !loadingCompleted}
  <!-- Loading screen content -->
  <div class="loading-screen">
    <!-- Background loading bar -->
    <div class="loading-background-bar">
      <!-- Progress loading bar -->
      <div class="loading-bar" style="width: {loading ? loadingProgress + '%' : '0%'}">
        <!-- GIF overlay -->
        <div class="loading-gif"></div>
      </div>
    </div>

    <div class="loading-title-container">
      <div class="loading-title">PuzzleMage.AI</div>
    </div>

    <div class="loading-spinner">
      <!-- svelte-ignore a11y-img-redundant-alt -->
    </div>
    <div class="quote-container">
        <div class="loading-quote">{randomQuote}</div>
    </div>
  </div>
{/if}


<style>
  @font-face {
    font-family: "DragonHunter", sans-serif;
    src: url("/static/DragonHunter.otf"); /* Update the path as needed */
  }

  :root {
    --color-bg-0: #5c3d86; /* Deep purple */
    --color-bg-1: #a17eb8; /* Medium purple */
    --color-bg-2: #d1aee3; /* Light purple */
  }

  .loading-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column; /* Stack items vertically */
    justify-content: center; /* Center content vertically */
    align-items: center; /* Center content horizontally */

    min-height: 100vh;
    margin: 0;
    background-image: url("./src/lib/images/loading-background.jpeg"); /* Corrected property and URL */
    background-size: cover;
    background-repeat: no-repeat;
    font-family: "DragonHunter"; /* Use the correct font family */
    padding-top: 20px; /* Provide a little padding for aesthetics */
  }

  .loading-title-container {
    position: absolute;
    top: 20px; /* Positioning the title 20px from the top */
    left: 50%; /* Centering horizontally */
    transform: translateX(-50%);
    text-align: center;
  }

  .loading-title {
    font-family: "DragonHunter", sans-serif;
    font-size: 20px;
    letter-spacing: 5px;
    color: white;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
    padding: 10px;
  }

  .loading-spinner {
    position: relative;
    width: 0px;
    height: 100px;
    top: 35px;
  }

  .quote-container {
    max-width: 75%; /* Limit the width to 75% of the page width */
    margin: 0 auto; /* Center the container horizontally */
    padding: 10px; /* Add padding to create space around the text */
    background-color: rgba(0, 0, 0, 0.7); /* Adjust the opacity as needed */
    border-radius: 10px; /* Add rounded corners */
  }

  /* Style for the quote text */
  .loading-quote {
    font-size: 24px;
    text-align: center;
    color: white;
  }

  .loading-background-bar {
    position: relative; /* Make it a container for .loading-bar and .loading-gif */
    height: 10px;
    background-color: white;
    border-radius: 5px;
    width: 60%;
  }

  .loading-bar {
    height: 100%;
    background-color: white;
    border-radius: 5px;
    position: absolute;
    top: 0;
    left: 0;
  }

  .loading-gif {
  /* Position the GIF inside the loading bar */
  position: absolute;
  top: -85px;
  left: 0;
  width: 1000%;
  height: 1000%;
  background-image: url('/src/lib/images/fireball.gif'); /* Specify the URL of your GIF */
  background-size: contain; /* Ensure the GIF maintains its aspect ratio */
  background-repeat: no-repeat; /* Ensure the GIF doesn't repeat */
  background-position: center; /* Center the GIF within the container */
  z-index: 2;
  animation: moveFireball 38s linear infinite; /* Adjust the animation duration */
}

@keyframes moveFireball {
  0% {
    transform: translateX(-50%) translateY(40px); /* Initial position */
  }
  100% {
    transform: translateX(70%) translateY(40px); /* Move to the right */
  }
}

</style>
