<script>
    import { onMount } from 'svelte';

    onMount(() => {
        // Set a flag in the session storage when the about page is loaded
        sessionStorage.setItem('cameFromAbout', 'true');
    });
</script>

<svelte:head>
    <title>About</title>
    <meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">
    <h1 class="about-heading">About this app</h1>

    <p>
        Welcome to the <strong>Sudoku Solver Web App</strong>! Our journey began at the <strong>KnightHacks UCF Hackathon</strong>, where a group of passionate individuals came together to create an <em>innovative solution</em> for Sudoku puzzle enthusiasts. Our mission is to provide an <em>interactive and engaging platform</em> for solving Sudoku puzzles using <strong>cutting-edge technology</strong>. With a blend of <strong>computer vision</strong> powered by <strong>OpenCV</strong> and <strong>augmented reality (AR)</strong> integration, we offer a <em>unique and immersive</em> Sudoku-solving experience.
    </p>

    <h2 class="about-subheading">Our Journey:</h2>

    <p>
        The inception of our Sudoku Solver Web App can be traced back to the <strong>KnightHacks UCF Hackathon</strong>, a dynamic and collaborative event that <em>encourages creativity and innovation</em>. Inspired by the challenge of combining technology and puzzles, our team embarked on a journey to create a platform that not only solves Sudoku puzzles but also makes the process <em>enjoyable and educational</em>.
    </p>

    <h2 class="about-subheading">Key Features:</h2>

    <ul class="about-features">
        <li><strong>Sudoku Solver:</strong> Our app can solve Sudoku puzzles of varying difficulty levels <em>quickly and accurately</em>. Simply hover your camera over the puzzle, and our app will do the rest.</li>
        <li><strong>AR Visualization:</strong> Experience Sudoku in a whole new way with our <strong>AR integration</strong>. Watch as the puzzle comes to life, making it easier than ever to track your progress.</li>
        <li><strong>Svelte-Powered Interface:</strong> Our user-friendly and responsive interface is built using <strong>Svelte</strong>, ensuring a <em>smooth and efficient</em> user experience.</li>
        <li><strong>Custom Puzzles:</strong> Import puzzles from newspapers, magazines, or online sources to solve and share.</li>
    </ul>

    <h2 class="about-subheading">Contributors:</h2>

    <ul class="about-contributors">
        <li><strong>Dario Sansotta</strong></li>
        <li><strong>Jhon Tabio</strong></li>
        <li><strong>Matthew Labrada</strong></li>
        <li><strong>Dennis Gorman</strong></li>
    </ul>

    <p>
        At the Sudoku Solver Web App, we believe in the power of <em>innovation</em> to transform traditional pastimes into exciting, modern experiences. Join us on this exciting journey, and let's <em>redefine the way you solve Sudoku puzzles</em>.
    </p>
</div>
