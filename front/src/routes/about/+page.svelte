<script>
    import { onMount } from 'svelte';

    onMount(() => {
        document.title = "About Us";
    });
</script>

<svelte:head>
    <title>About Us</title>
    <meta name="description" content="Learn more about our team and mission." />
</svelte:head>

<style>
    .about-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px 20px;
        font-family: DragonHunter;
        
        background-color: rgba(0, 0, 0, 0.7); /* Black with 70% opacity */
        border-radius: 15px; /* Rounded corners */
        padding: 30px; /* Spacing inside the container */
        
        color: white; /* Set font color to white */
    }

    .about-heading {
        font-size: 2rem;
        margin-bottom: 20px;
    }

    .about-subheading {
        font-size: 1.5rem;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    .about-text {
        text-align: center;
        font-family: sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    .team-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap; /* Allows the items to wrap if the container is too narrow */
    gap: 20px; /* Spacing between team members */
}

.team-member {
    text-align: center; /* Center the content */
    flex: 1; /* Distribute space equally among team members */
    max-width: 200px; /* Maximum width for each team member container */
}

.team-member img {
    width: 100px; /* Adjust as needed */
    height: 100px; /* Adjust as needed */
    border-radius: 50%; /* Makes the image round */
    object-fit: cover; /* Ensures the image covers the entire space without distortion */
}

.team-member h3 {
    font-family: sans-serif;
    margin-top: 5px;
    font-size: 1.2rem;
}

.team-member p {
    font-family: sans-serif;
    font-size: 0.9rem;
    margin-top: 5px;
}

.team-member ul {
    font-family: sans-serif;
    list-style: none;
    text-align: center;
    padding: 0; /* Reset default padding */
    margin: 0; /* Reset default margin */
}

</style>

<div class="about-container">
    <h1 class="about-heading">About Us</h1>

    <p class="about-text">
        <nbsp>Welcome to the Puzzle Mage . AI ! Our journey began at the KnightHacks UCF Hackathon, 
        where a group of passionate individuals came together to create an innovative 
        solution for Sudoku puzzle enthusiasts. Our mission is to provide an interactive 
        and engaging platform for solving Sudoku puzzles using cutting-edge technology. 
        With a blend of computer vision powered by OpenCV and augmented reality (AR) 
        integration, we offer a unique and immersive Sudoku-solving experience .
    </p>

    <h2 class="about-subheading">Our Team</h2>

<div class="team-container">
    <div class="team-member">
        <a href="https://github.com/MatthewLabrada" target="_blank">
            <img src="./src/lib/images/Matthew.jpg" alt="Matthew Labrada">
        </a>
        <h3>Matthew Labrada</h3>
        <ul>
            <li>Project Manager</li>
            <li>FrontEnd</li>
            <li>BackEnd</li>
            <li>Database</li>
        </ul>
    </div>

    <div class="team-member">
        <a href="https://github.com/dotshix" target="_blank">
            <img src="./src/lib/images/Dario.jpeg" alt="Dario Sansotta">
        </a>
        <h3>Dario Sansotta</h3>
        <ul>
            <li>FrontEnd</li>
            <li>BackEnd</li>
            <li>Database</li>
        </ul>
    </div>

    <div class="team-member">
        <a href="https://github.com/JhonTabio" target="_blank">
            <img src="./src/lib/images/Jhon.jpeg" alt="Jhon Tabio">
        </a>
        <h3>Jhon Tabio</h3>
        <ul>
            <li>BackEnd</li>
            <li>Computer Vision</li>
            <li>Database</li>
        </ul>
    </div>

    <div class="team-member">
        <a href="https://github.com/sinneDelirium" target="_blank">
            <img src="./src/lib/images/Dennis.jpg" alt="Dennis Gorman">
        </a>
        <h3>Dennis Gorman</h3>
            <ul>
                <li>FrontEnd</li>
                <li>BackEnd</li>
                <li>Computer Vision</li>
                <li>Database</li>
            </ul>
    </div>
</div>
</div>
