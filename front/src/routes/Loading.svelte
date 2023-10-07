<!-- Loading.svelte -->
<style>
    @font-face {
        font-family: 'Minecraft';
        font-style: normal;
        font-weight: normal;
        src: local('Minecraft'), url('Minecraft.woff') format('woff');
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
	    background-attachment: fixed;
	    background-color: var(--color-bg-1);
	    background-size: 100vw 100vh;
	    background-image: radial-gradient(
			50% 50% at 50% 50%,
			rgba(255, 255, 255, 0.75) 0%,
			rgba(255, 255, 255, 0) 100%
		),
		linear-gradient(180deg, var(--color-bg-0) 0%, var(--color-bg-1) 15%, var(--color-bg-2) 50%);

        z-index: 9999;
        font-family: 'Minecraft', sans-serif; /* Use the correct font family */
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
        font-size: 100px;
    }
    
    .loading-spinner {
        position: relative;
        width: 0px;
        height: 100px;
    }
    
    .center-image {
        width: 100px;
        height: 100px;
        animation: moveWandAround 2s linear infinite;
    }
    
    @keyframes moveWandAround {
        0% {
            transform: translateX(-50%) rotate(0deg) translateY(40px) rotate(0deg);
        }
        
        25% {
            transform: translateX(-50%) rotate(90deg) translateY(40px) rotate(-90deg);
        }
        50% {
            transform: translateX(-50%) rotate(180deg) translateY(40px) rotate(-180deg);
        }
        75% {
            transform: translateX(-50%) rotate(270deg) translateY(40px) rotate(-270deg);
        }
        100% {
            transform: translateX(-50%) rotate(360deg) translateY(40px) rotate(-360deg);
        }
    }
    
    </style>
    
    <div class="loading-screen">
        <div class="loading-title-container">
            <div class="loading-title">PuzzleMage.AI</div>
        </div>
        <div class="loading-spinner">
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <img src="wand.png" alt="Image" class="center-image" />
        </div>
    </div>
    