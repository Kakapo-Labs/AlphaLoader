#
#
#
# --- START OF MODIFICATION ---

HTML_CONTENT = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AlphaLoader</title>
            <style>
                /* --- Rubik Font --- */
                @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap');

                /* --- Splash Screen CSS (New) --- */
                #splash-screen {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 1);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 10001; /* Ensure it's on top of everything */
                    font-family: 'Rubik', sans-serif;
                    overflow: hidden;
                    backdrop-filter: blur(0px);
                }

                .splash-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    gap: 0;
                    filter: blur(20px);
                    opacity: 0;
                    position: relative;
                    z-index: 10;
                }

                .main-svg-container {
                    width: 250px;
                    height: 250px;
                    overflow: visible;
                }

                .k-text {
                    font-family: 'Rubik', sans-serif;
                    font-size: 10rem;
                    font-weight: 700;
                    text-anchor: middle;
                    dominant-baseline: central;
                }

                #k-fill {
                    fill: #ffd83a;
                    filter: url(#k-glow);
                }

                #k-stroke {
                    fill: none;
                    stroke: #ffd83a;
                    /* MODIFIED: Increased stroke width for a thicker outline */
                    stroke-width: 2px;
                    opacity: 0;
                }

                #subtitle-stroke {
                    font-family: 'Rubik', sans-serif;
                    font-size: 2.8rem;
                    font-weight: 700;
                    letter-spacing: 2px;
                    text-anchor: middle;
                    dominant-baseline: central;
                    fill: none;
                    stroke: #ffd83a;
                    stroke-width: 1px;
                    opacity: 0;
                    filter: url(#k-glow);
                }

                /* --- Main Content CSS (Initially Hidden) --- */
                #main-content {
                    visibility: hidden;
                    opacity: 0;
                    transition: opacity 1.5s ease-in-out;
                }

                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }

                body {
                    background: linear-gradient(135deg, #0a0a0a 0%, #39200D 100%);
                    color: #ffffff;
                    min-height: 100vh;
                    overflow-x: hidden;
                    position: relative;
                }

                ::-webkit-scrollbar {
                    display: none;
                }

                body {
                    -ms-overflow-style: none;
                    scrollbar-width: none;
                }

                #custom-scrollbar {
                    position: fixed;
                    right: 5px;
                    top: 0;
                    width: 8px;
                    /* --- COLOR CHANGE --- */
                    background-color: #ffd83a;
                    border-radius: 4px;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    z-index: 9999;
                }

                #custom-scrollbar.visible {
                    opacity: 0.7;
                }


                body::before {
                    content: '';
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    /* --- COLOR CHANGE --- */
                    background:
                        radial-gradient(circle at 20% 50%, rgba(255, 216, 58, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 50%, rgba(255, 142, 55, 0.1) 0%, transparent 50%);
                    pointer-events: none;
                    z-index: 1;
                }

                #custom-tooltip {
                    position: fixed;
                    background-color: rgba(20, 20, 20, 0.9);
                    color: #eee;
                    padding: 8px 12px;
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    font-size: 14px;
                    z-index: 10000;
                    pointer-events: none;
                    display: none;
                    backdrop-filter: blur(5px);
                    max-width: 300px;
                    text-align: center;
                }

                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                    position: relative;
                    z-index: 2;
                }

                header {
                    text-align: center;
                    margin-bottom: 20px;
                    padding: 20px 0;
                }

                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                    /* --- COLOR CHANGE --- */
                    background: linear-gradient(90deg, #ffd83a 0%, #FF8E37 100%);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    text-shadow: 0 2px 10px rgba(255, 216, 58, 0.3);
                    font-weight: 700;
                }

                .subtitle {
                    font-size: 1.1rem;
                    color: #888;
                    margin-bottom: 20px;
                    font-weight: 400;
                }

                .controls {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin-bottom: 40px;
                }

                .search-container {
                    width: 100%;
                    max-width: 700px;
                    position: relative;
                    margin-bottom: 20px; /* Adjusted for even spacing */
                }

                .search-icon {
                    position: absolute;
                    left: 15px;
                    top: 50%;
                    transform: translateY(-50%);
                    color: #fff;
                    z-index: 2;   /* <-- ADD THIS LINE TO LIFT THE ICON UP */
                    transition: filter 0.3s ease; /* <-- ADD THIS LINE */


                }

                /* Add this new rule for the icon's glow */
                .search-container:focus-within .search-icon {
                    color: #ffd83a; /* Optional: Makes the icon itself golden */
                    filter: drop-shadow(0 0 8px rgba(255, 216, 58, 0.7));
                }


                .search-box {
                    width: 100%;
                    padding: 12px 20px 12px 45px;
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    color: #ffffff;
                    font-size: 14px;
                    transition: all 0.3s ease;
                    outline: none;
                }

                .search-box:focus {
                    background: rgba(255, 255, 255, 0.08);
                    /* --- COLOR CHANGE --- */
                    border-color: rgba(255, 216, 58, 0.5);
                    box-shadow: 0 0 20px rgba(255, 216, 58, 0.2);
                }

                .search-box::placeholder {
                    color: #666;
                }

                .filter-container {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    width: 100%;
                    max-width: 700px;
                }

                .filter-btn {
                    padding: 10px 20px;
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 25px;
                    color: #888;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-size: 14px;
                    font-weight: 500;
                    outline: none;
                    position: relative;
                    overflow: hidden;
                    flex-grow: 1;
                    text-align: center;
                    margin: 0 5px;
                }

                .filter-btn::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    /* --- COLOR CHANGE --- */
                    background: linear-gradient(90deg, #ffd83a 0%, #FF8E37 100%);
                    border-radius: 25px;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }

                .filter-btn:hover {
                    /* --- COLOR CHANGE --- */
                    border-color: rgba(255, 216, 58, 0.5);
                    color: #ffffff;
                    transform: translateY(-2px);
                }

                .filter-btn.active {
                    /* --- COLOR CHANGE --- */
                    background: rgba(255, 216, 58, 0.2);
                    border-color: #ffd83a;
                    color: #ffffff;
                }

                .filter-btn.active::before {
                    opacity: 0.2;
                }

                .filter-btn span {
                    position: relative;
                    z-index: 1;
                }

                .mod-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                    gap: 30px;
                    margin-top: 30px;
                }

                .mod-card {
                    background: rgba(28, 28, 30, 0.7);
                    border-radius: 20px;
                    overflow: hidden;
                    box-shadow:
                        0 8px 32px rgba(0, 0, 0, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    transition: transform 0.4s ease, box-shadow 0.4s ease;
                    will-change: transform, box-shadow;
                    position: relative;
                    display: flex;
                    flex-direction: column;
                }

                .mod-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    /* --- COLOR CHANGE --- */
                    background: linear-gradient(135deg,
                        rgba(255, 216, 58, 0.1) 0%,
                        rgba(255, 142, 55, 0.05) 100%);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    border-radius: 20px;
                }

                .mod-card:hover {
                    transform: translateY(-8px);
                    /* --- COLOR CHANGE --- */
                    box-shadow:
                        0 16px 48px rgba(255, 216, 58, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.2);
                }

                .mod-card:hover::before {
                    opacity: 1;
                }

                .card-image-container {
                    height: 150px;
                    position: relative;
                    overflow: hidden;
                    background: rgba(0, 0, 0, 0.2);
                }

                .card-image {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: transform 0.6s ease;
                }

                .mod-card:hover .card-image {
                    transform: scale(1.1);
                }

                .image-slider {
                    position: relative;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                }

                .slide {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    opacity: 0;
                    transition: opacity 1.2s ease;
                }

                .slide.active {
                    opacity: 1;
                }

                .slide img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }

                .slider-dots {
                    position: absolute;
                    bottom: 15px;
                    left: 0;
                    right: 0;
                    display: flex;
                    justify-content: center;
                    gap: 10px;
                }

                .dot {
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.3);
                    cursor: pointer;
                    transition: all 0.3s ease;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }

                .dot:hover {
                    background: rgba(255, 255, 255, 0.5);
                    transform: scale(1.2);
                }

                .dot.active {
                    background: #ffffff;
                    transform: scale(1.3);
                    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                }

                .card-content {
                    padding: 25px;
                    position: relative;
                    flex-grow: 1;
                    display: flex;
                    flex-direction: column;
                }

                .card-category {
                    display: inline-block;
                    padding: 6px 16px;
                    /* --- COLOR CHANGE --- */
                    background: rgba(255, 216, 58, 0.15);
                    border: 1px solid rgba(255, 216, 58, 0.3);
                    color: #c78c1e; /* Adjusted for readability */
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    font-size: 0.75rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 15px;
                }

                .card-title {
                    font-size: 1.4rem;
                    margin-bottom: 12px;
                    color: #ffffff;
                    font-weight: 700;
                    line-height: 1.3;
                    overflow: hidden;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                }

                .card-description {
                    color: #aaa;
                    margin-bottom: 18px;
                    font-size: 0.9rem;
                    line-height: 1.5;
                    overflow: hidden;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                }

                .card-author {
                    color: #888;
                    font-size: 0.8rem;
                    margin-bottom: 25px;
                    font-style: italic;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }

                .card-author a {
                    color: #888;
                    text-decoration: underline;
                    font-weight: bold;
                    transition: color 0.3s ease;
                }

                .card-author a:hover {
                    /* --- COLOR CHANGE --- */
                    color: #FF8E37;
                }

                .action-btn {
                    display: block;
                    width: 100%;
                    padding: 14px;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    position: relative;
                    overflow: hidden;
                    margin-top: auto;
                }

                .download-btn {
                    /* --- COLOR CHANGE --- */
                    background: linear-gradient(90deg, #ffd83a 0%, #FF8E37 100%);
                    box-shadow: 0 4px 15px rgba(255, 216, 58, 0.3);
                }

                .uninstall-btn {
                    background: linear-gradient(90deg, #c31432 0%, #240b36 100%);
                    box-shadow: 0 4px 15px rgba(195, 20, 50, 0.3);
                }

                .action-btn::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                    transition: left 0.5s ease;
                }

                .action-btn:hover {
                    transform: translateY(-3px);
                }

                .download-btn:hover {
                    /* --- COLOR CHANGE --- */
                    box-shadow: 0 8px 25px rgba(255, 216, 58, 0.5);
                }

                .uninstall-btn:hover {
                    box-shadow: 0 8px 25px rgba(195, 20, 50, 0.5);
                }

                .action-btn:hover::before {
                    left: 100%;
                }

                .action-btn:active {
                    transform: translateY(-1px);
                }

                .notification {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    padding: 15px 25px;
                    background: rgba(0, 0, 0, 0.8);
                    backdrop-filter: blur(20px);
                    color: white;
                    border-radius: 15px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    transform: translateY(100px);
                    opacity: 0;
                    transition: all 0.3s ease;
                    z-index: 1000;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }

                .notification.show {
                    transform: translateY(0);
                    opacity: 1;
                }

                .notification.success {
                    background: rgba(76, 175, 80, 0.2);
                    border-color: rgba(76, 175, 80, 0.3);
                    color: #81C784;
                }

                .notification.error {
                    background: rgba(244, 67, 54, 0.2);
                    border-color: rgba(244, 67, 54, 0.3);
                    color: #E57373;
                }

                /* --- Progress Bar CSS (New) --- */
                #progress-overlay {
                    position: fixed;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%) translateY(150%);
                    width: 500px;
                    padding: 10px 20px;
                    background-color: rgba(18, 18, 18, 0.9);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(10px);
                    transition: transform 0.4s ease-out, opacity 0.4s ease-out;
                    z-index: 9999;
                    opacity: 0;
                    visibility: hidden;
                }

                #progress-overlay.visible {
                    transform: translateX(-50%) translateY(0);
                    opacity: 1;
                    visibility: visible;
                }

                #progress-label {
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: center;
                    margin-bottom: 8px;
                }

                #progress-bar-container {
                    height: 10px;
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 5px;
                    overflow: hidden;
                }

                #progress-bar-fill {
                    height: 100%;
                    width: 0%;
                    background-color: #6a11cb;
                    border-radius: 5px;
                    transition: width 0.3s ease;
                }


                .loading-spinner {
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    border: 3px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    border-top-color: white;
                    animation: spin 1s ease-in-out infinite;
                    margin-right: 10px;
                }

                @keyframes spin {
                    to { transform: rotate(360deg); }
                }

                .hidden {
                    display: none;
                }

                .no-results {
                    text-align: center;
                    padding: 60px 20px;
                    color: #666;
                    font-size: 1.2rem;
                    background: rgba(255, 255, 255, 0.03);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }

                .pagination-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                    margin-top: 20px;
                }

                .pagination-btn, .pagination-page {
                    padding: 8px 16px;
                    margin: 0 4px;
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    color: #888;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .pagination-btn:hover, .pagination-page:hover {
                    /* --- COLOR CHANGE --- */
                    background: rgba(255, 216, 58, 0.3);
                    color: #fff;
                }

                .pagination-page.active {
                    /* --- COLOR CHANGE --- */
                    background: #ffd83a;
                    color: #fff;
                    font-weight: bold;
                }

                .pagination-btn:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }

                @media (max-width: 768px) {
                    .controls {
                        flex-direction: column;
                    }

                    .search-container {
                        min-width: 100%;
                    }

                    .mod-grid {
                        grid-template-columns: 1fr;
                    }
                }

                @media (max-width: 600px) {
                    .main-svg-container {
                        width: 180px;
                        height: 200px;
                    }
                    .k-text {
                        font-size: 8rem;
                    }
                    #subtitle-stroke {
                        font-size: 1.8rem;
                        letter-spacing: 1px;
                    }
                }
            </style>
        </head>
        <body>
            <div id="splash-screen">
                <div class="splash-container">
                    <svg class="main-svg-container" viewBox="0 0 200 200">
                        <defs>
                            <filter id="k-glow" x="-50%" y="-50%" width="200%" height="200%">
                                <feGaussianBlur in="SourceGraphic" stdDeviation="0" result="blur" />
                                <feFlood flood-color="#ffd83a" flood-opacity="0" result="flood" />
                                <feComposite in="flood" in2="blur" operator="in" result="coloredBlur" />
                                <feMerge>
                                    <feMergeNode in="coloredBlur" />
                                    <feMergeNode in="SourceGraphic" />
                                </feMerge>
                            </filter>

                            <filter id="ripple-filter">
                                <feTurbulence 
                                    id="turbulence" 
                                    baseFrequency="0.02 0.05" 
                                    numOctaves="2" 
                                    result="turbulence"
                                />
                                <feDisplacementMap 
                                    in="SourceGraphic" 
                                    in2="turbulence"
                                    scale="0" 
                                />
                            </filter>

                            <mask id="wave-mask">
                                <rect id="mask-rect" x="-100" y="200" width="400" height="400" fill="white" filter="url(#ripple-filter)" />
                            </mask>
                        </defs>

                        <text class="k-text" id="k-fill" x="50%" y="70" mask="url(#wave-mask)">K</text>
                        <text class="k-text" id="k-stroke" x="50%" y="70">K</text>
                        <text id="subtitle-stroke" x="50%" y="160">Kakapo Labs</text>
                    </svg>
                </div>
            </div>

            <div id="main-content">
                <div id="custom-scrollbar"></div>
                <div id="custom-tooltip"></div>
                <div class="container">
                    <header>
                        <h1>AlphaLoader</h1>
                        <p class="subtitle">The easiest way to install AlphaConsole mods with just one click :)</p>
                    </header>
                    <div class="controls">
                        <div class="search-container">
                            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="11" cy="11" r="8"></circle>
                                <path d="m21 21-4.35-4.35"></path>
                            </svg>
                            <input type="text" id="search-input" class="search-box" placeholder="Search mods...">
                        </div>
                        <div class="filter-container">
                            <button class="filter-btn active" data-category="all"><span>All</span></button>
                            <button class="filter-btn" data-category="balls"><span>Balls</span></button>
                            <button class="filter-btn" data-category="boost-meter"><span>Boost Meter</span></button>
                            <button class="filter-btn" data-category="decals"><span>Decals</span></button>
                            <button class="filter-btn" data-category="banner"><span>Banners</span></button>
                            <button class="filter-btn" data-category="profile-borders"><span>Profile Borders</span></button>
                        </div>
                    </div>
                    <div id="mod-grid" class="mod-grid"></div>
                    <div id="no-results" class="no-results hidden">
                        <h3>No mods found</h3>
                        <p>Try adjusting your search or filter criteria</p>
                    </div>
                    <div id="pagination-controls" class="pagination-container"></div>
                </div>
                <div id="notification" class="notification"></div>
                <div id="progress-overlay">
                    <div id="progress-label">Initializing...</div>
                    <div id="progress-bar-container">
                        <div id="progress-bar-fill"></div>
                    </div>
                </div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js"></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
            // --- Splash Screen Animation Logic (New) ---
            window.onload = function() {
                const splashScreen = document.getElementById('splash-screen');
                const mainContent = document.getElementById('main-content');

                const animationTimings = {
                    kFadeInDuration: 500,
                    initialDelay: 200,
                    liquidFillDuration: 2800,
                    glowAppearDelay: 200,
                    glowAppearDuration: 800,
                    subtitleAppearDuration: 1000,
                    blurFadeInDuration: 1000,
                    fadeOutDuration: 1500, 
                };

                const splashContainer = document.querySelector('.splash-container');
                const kStroke = document.getElementById('k-stroke');
                const subtitleStroke = document.getElementById('subtitle-stroke');
                const feGaussianBlur = document.querySelector('#k-glow feGaussianBlur');
                const feFlood = document.querySelector('#k-glow feFlood');

                const maskRect = document.getElementById('mask-rect');
                const turbulence = document.getElementById('turbulence');
                const displacementMap = document.querySelector('#ripple-filter feDisplacementMap');

                function transitionToPage() {
                    // Make main content available for the blur effect, but keep it invisible.
                    mainContent.style.visibility = 'visible';
                    mainContent.style.opacity = '0'; // Start transparent

                    const transitionTimeline = anime.timeline({
                        easing: 'easeInOutQuad',
                    });

                    // Step 1: Transition from black background to a blurred view of the UI.
                    transitionTimeline.add({
                        targets: splashScreen,
                        backgroundColor: 'rgba(0, 0, 0, 0)',
                        backdropFilter: 'blur(10px)',
                        duration: 1000,
                        delay: 100 // A short pause after the logo animation finishes
                    });

                    // Step 2: Fade out the splash screen (logo + blur) and fade in the main content.
                    transitionTimeline.add({
                        targets: splashScreen,
                        opacity: 0,
                        duration: 1500,
                        complete: function() {
                            splashScreen.remove();
                        }
                    }, '+=200'); // Start this shortly after the blur is complete

                    transitionTimeline.add({
                        targets: mainContent,
                        opacity: 1,
                        duration: 1500
                    }, '-=1500'); // Run this simultaneously with the splash screen fade out
                }


                const timeline = anime.timeline({
                    easing: 'easeOutQuad',
                    delay: animationTimings.initialDelay,
                    complete: function() {
                        transitionToPage();
                    }
                });

                timeline.add({
                    targets: splashContainer,
                    filter: ['blur(20px)', 'blur(0px)'],
                    opacity: [0, 1],
                    duration: animationTimings.blurFadeInDuration,
                    easing: 'easeOutQuad'
                });

                timeline.add({
                    targets: kStroke,
                    opacity: [0, 1],
                    duration: animationTimings.kFadeInDuration,
                    easing: 'easeOutQuad'
                }, '-=' + (animationTimings.blurFadeInDuration / 2));

                timeline.add({
                    targets: maskRect,
                    y: [140, -10],
                    duration: animationTimings.liquidFillDuration,
                    easing: 'easeOutSine',
                }, '+=100')
                .add({
                    targets: displacementMap,
                    scale: [
                        { value: 25, duration: 400, easing: 'easeOutQuad' },
                        { value: 25, duration: animationTimings.liquidFillDuration - 800 },
                        { value: 0, duration: 400, easing: 'easeInQuad' }
                    ],
                }, '-=' + animationTimings.liquidFillDuration) 
                .add({
                    targets: turbulence,
                    baseFrequency: ['0.02 0.05', '0.03 0.06'],
                    duration: animationTimings.liquidFillDuration,
                    easing: 'easeInOutSine',
                    direction: 'alternate'
                }, '-=' + animationTimings.liquidFillDuration);

                timeline.add({
                    targets: feGaussianBlur,
                    stdDeviation: [0, 8],
                    duration: animationTimings.glowAppearDuration,
                    easing: 'easeOutQuad',
                    delay: animationTimings.glowAppearDelay
                }, '-=700')
                .add({
                    targets: feFlood,
                    floodOpacity: [0, 1],
                    duration: animationTimings.glowAppearDuration,
                    easing: 'easeOutQuad',
                    delay: animationTimings.glowAppearDelay
                }, '-=800')
                .add({
                    targets: subtitleStroke,
                    opacity: [0, 1],
                    translateY: [-20, 0],
                    duration: animationTimings.subtitleAppearDuration,
                    easing: 'easeOutExpo'
                }, '-=800');
            };

            // --- Main Application Logic ---
            document.addEventListener("DOMContentLoaded", () => {
                let mods = [];
                let installedModIds = [];
                let backend = null;

                let isModListReady = false;
                let isInstalledListReady = false;

                let currentFilter = 'all';
                let searchTerm = '';
                let currentPage = 1;
                const modsPerPage = 20;

                // --- NEW: Progress Bar and Notification Functions ---
                const progressOverlay = document.getElementById('progress-overlay');
                const progressLabel = document.getElementById('progress-label');
                const progressBarFill = document.getElementById('progress-bar-fill');

                function updateProgress(status, progress) {
                    progressLabel.textContent = status;
                    progressBarFill.style.width = `${progress}%`;
                    progressOverlay.classList.add('visible');
                }

                function onInstallComplete(mod_id) {
                    const mod = mods.find(m => m.id === mod_id);
                    if (mod) {
                        mod.installed = true;
                        showNotification(`${mod.name} installed successfully!`, "success");
                    }
                    loadModCards(); // Refresh the UI to show the 'Uninstall' button

                    // Hide the progress bar after a delay
                    setTimeout(() => {
                        progressOverlay.classList.remove('visible');
                    }, 2000);
                }

                function onUninstallComplete(mod_id) {
                    const mod = mods.find(m => m.id === mod_id);
                    if (mod) {
                        mod.installed = false;
                        showNotification(`${mod.name} uninstalled successfully!`, "success");
                    }
                    loadModCards(); // Refresh the UI to show the 'Download' button
                }

                function onDownloadError(error) {
                    showNotification("Error: " + error, "error");
                    progressOverlay.classList.remove('visible');
                }


                setInterval(() => {
                    const sliders = document.querySelectorAll('.image-slider');
                    sliders.forEach(slider => {
                        let currentIndex = parseInt(slider.dataset.currentIndex || '0', 10);
                        const imageCount = parseInt(slider.dataset.imageCount, 10);
                        const modId = slider.dataset.modId;

                        if (imageCount > 1) {
                            const nextIndex = (currentIndex + 1) % imageCount;
                            slider.dataset.currentIndex = nextIndex;
                            showSlide(nextIndex, modId);
                        }
                    });
                }, 3000);

                function attemptRender() {
                    if (!isModListReady || !isInstalledListReady) {
                        return;
                    }

                    mods.forEach(mod => {
                        mod.installed = installedModIds.includes(mod.id);
                    });

                    loadModCards();
                }

                function onModListFetched(modsJsonString) {
                    console.log("--- DEBUG (JS): Received mod list from GitHub.");
                    if (!modsJsonString || modsJsonString.trim() === "") {
                        console.error("--- DEBUG (JS): CRITICAL ERROR - Received empty or null string from backend.");
                        showNotification("Received no data from the server.", "error");
                        return;
                    }

                    try {
                        mods = JSON.parse(modsJsonString);
                        isModListReady = true;
                        attemptRender();
                    } catch (e) {
                        console.error("--- DEBUG (JS): CRITICAL ERROR - Failed to parse JSON string.", e);
                        showNotification("Fatal Error: Could not parse mod list. See console for details.", "error");
                    }
                }

                function onInstalledModsChecked(installed_ids) {
                    console.log("--- DEBUG (JS): Received local installed mods list.");
                    installedModIds = installed_ids;
                    isInstalledListReady = true;
                    attemptRender();
                }

                new QWebChannel(qt.webChannelTransport, function(channel) {
                    backend = channel.objects.backend;
                    console.log("--- DEBUG (JS): WebChannel connected.");

                    // Connect backend signals to the new JS functions
                    backend.update_progress.connect(updateProgress);
                    backend.install_complete.connect(onInstallComplete);
                    backend.uninstall_complete.connect(onUninstallComplete);
                    backend.download_error.connect(onDownloadError);

                    // Existing connections
                    backend.mod_list_fetched.connect(onModListFetched);
                    backend.installed_mods_checked.connect(onInstalledModsChecked);

                    backend.textures_found.connect(function(path) {
                        showNotification("Mod folder found!", "success");
                    });

                    backend.textures_not_found.connect(function() {
                        showNotification("Mod folder not found. Please ensure BakkesMod is installed.", "error");
                        document.querySelectorAll('.action-btn').forEach(btn => {
                            btn.disabled = true;
                            btn.style.background = '#555';
                            btn.style.cursor = 'not-allowed';
                            btn.textContent = 'FOLDER NOT FOUND';
                        });
                    });

                    console.log("--- DEBUG (JS): Requesting both mod list and installed status from backend.");
                    backend.fetch_mod_list();
                    backend.check_installed_mods();
                    backend.check_textures_folder();
                });

                function loadModCards() {
                    const modGrid = document.getElementById('mod-grid');
                    modGrid.innerHTML = '';

                    const filteredMods = mods.filter(mod => {
                        const matchesCategory = currentFilter === 'all' || mod.category === currentFilter;
                        const matchesSearch = searchTerm === '' ||
                            mod.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            mod.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            mod.author.toLowerCase().includes(searchTerm.toLowerCase());
                        return matchesCategory && matchesSearch;
                    });

                    if (filteredMods.length === 0) {
                        document.getElementById('no-results').classList.remove('hidden');
                        document.getElementById('pagination-controls').classList.add('hidden');
                        return;
                    }

                    document.getElementById('no-results').classList.add('hidden');
                    document.getElementById('pagination-controls').classList.remove('hidden');

                    const indexOfLastMod = currentPage * modsPerPage;
                    const indexOfFirstMod = indexOfLastMod - modsPerPage;
                    const currentMods = filteredMods.slice(indexOfFirstMod, indexOfLastMod);

                    currentMods.forEach(mod => {
                        const card = createModCard(mod);
                        modGrid.appendChild(card);
                    });

                    renderPaginationControls(filteredMods.length);
                    updateScrollbar();
                }

                function renderPaginationControls(totalMods) {
                    const pageCount = Math.ceil(totalMods / modsPerPage);
                    const paginationContainer = document.getElementById('pagination-controls');
                    paginationContainer.innerHTML = '';

                    if (pageCount <= 1) return;

                    const prevButton = document.createElement('button');
                    prevButton.textContent = 'Previous';
                    prevButton.className = 'pagination-btn';
                    prevButton.disabled = currentPage === 1;
                    prevButton.onclick = () => changePage(currentPage - 1);
                    paginationContainer.appendChild(prevButton);

                    for (let i = 1; i <= pageCount; i++) {
                        const pageButton = document.createElement('button');
                        pageButton.textContent = i;
                        pageButton.className = 'pagination-page';
                        if (i === currentPage) {
                            pageButton.classList.add('active');
                        }
                        pageButton.onclick = () => changePage(i);
                        paginationContainer.appendChild(pageButton);
                    }

                    const nextButton = document.createElement('button');
                    nextButton.textContent = 'Next';
                    nextButton.className = 'pagination-btn';
                    nextButton.disabled = currentPage === pageCount;
                    nextButton.onclick = () => changePage(currentPage + 1);
                    paginationContainer.appendChild(nextButton);
                }

                function changePage(page) {
                    currentPage = page;
                    loadModCards();
                }


                function createModCard(mod) {
                    const card = document.createElement('div');
                    card.className = 'mod-card';

                    const imageContainer = document.createElement('div');
                    imageContainer.className = 'card-image-container';

                    if (mod.images && mod.images.length > 1) {
                        const slider = createImageSlider(mod);
                        imageContainer.appendChild(slider);
                    } else {
                        const img = document.createElement('img');
                        img.src = mod.images && mod.images.length > 0 ? mod.images[0] : '';
                        img.className = 'card-image';
                        img.alt = mod.name;
                        img.loading = 'lazy';
                        imageContainer.appendChild(img);
                    }

                    const content = document.createElement('div');
                    content.className = 'card-content';

                    const category = document.createElement('div');
                    category.className = 'card-category';
                    category.textContent = mod.category.charAt(0).toUpperCase() + mod.category.slice(1);

                    const title = document.createElement('h3');
                    title.className = 'card-title has-tooltip';
                    title.textContent = mod.name;

                    const description = document.createElement('p');
                    description.className = 'card-description has-tooltip';
                    description.textContent = mod.description;

                    const author = document.createElement('p');
                    author.className = 'card-author has-tooltip';
                    author.dataset.tooltipText = `By: ${mod.author}`;
                    author.innerHTML = `By:&nbsp;<a href="${mod.authorUrl}" class="author-link">${mod.author}</a>`;

                    const actionBtn = document.createElement('button');
                    actionBtn.className = 'action-btn';

                    if (mod.installed) {
                        actionBtn.textContent = 'Uninstall';
                        actionBtn.classList.add('uninstall-btn');
                        actionBtn.onclick = function() {
                            if (backend) {
                                backend.uninstall_mod(mod.id, mod.category);
                            }
                        };
                    } else {
                        actionBtn.textContent = 'Download';
                        actionBtn.classList.add('download-btn');
                        actionBtn.onclick = function() {
                            if (backend) {
                                let fileType = mod.fileType || "auto";

                                if (fileType === "auto") {
                                    const url = mod.downloadUrl.toLowerCase();
                                    if (url.includes('.zip')) {
                                        fileType = "zip";
                                    } else if (url.includes('.rar')) {
                                        fileType = "rar";
                                    } else if (url.includes('.png') || url.includes('.jpg') || url.includes('.jpeg')) {
                                        fileType = "png";
                                    } else if (url.includes('.dds')) {
                                        fileType = "dds";
                                    }
                                }

                                console.log(`--- DEBUG: Downloading ${mod.name} with file type: ${fileType} in category ${mod.category}`);
                                backend.start_download(mod.downloadUrl, mod.name, mod.id, mod.category, fileType);
                            }
                        };
                    }

                    content.appendChild(category);
                    content.appendChild(title);
                    content.appendChild(description);
                    content.appendChild(author);
                    content.appendChild(actionBtn);

                    card.appendChild(imageContainer);
                    card.appendChild(content);

                    return card;
                }

                function createImageSlider(mod) {
                    const slider = document.createElement('div');
                    slider.className = 'image-slider';
                    slider.dataset.modId = mod.id;
                    slider.dataset.imageCount = mod.images.length;
                    slider.dataset.currentIndex = '0';

                    const dotsContainer = document.createElement('div');
                    dotsContainer.className = 'slider-dots';

                    mod.images.forEach((image, index) => {
                        const slide = document.createElement('div');
                        slide.className = 'slide';
                        if (index === 0) slide.classList.add('active');

                        const img = document.createElement('img');
                        img.src = image;
                        img.alt = `${mod.name} image ${index + 1}`;
                        img.loading = 'lazy';

                        slide.appendChild(img);
                        slider.appendChild(slide);

                        const dot = document.createElement('div');
                        dot.className = 'dot';
                        if (index === 0) dot.classList.add('active');

                        dot.onclick = function(e) {
                            e.stopPropagation();
                            slider.dataset.currentIndex = index;
                            showSlide(index, mod.id);
                        };

                        dotsContainer.appendChild(dot);
                    });

                    slider.appendChild(dotsContainer);

                    return slider;
                }

                function showSlide(index, modId) {
                    const mod = mods.find(m => m.id === modId);
                    if (!mod) return;

                    const cards = document.querySelectorAll('.mod-card');
                    const card = Array.from(cards).find(c =>
                        c.querySelector('.card-title').textContent === mod.name
                    );

                    if (!card) return;

                    const slides = card.querySelectorAll('.slide');
                    const dots = card.querySelectorAll('.dot');
                    const slider = card.querySelector('.image-slider');

                    if (slider) {
                       slider.dataset.currentIndex = index;
                    }

                    slides.forEach((slide, i) => {
                        slide.classList.toggle('active', i === index);
                    });

                    dots.forEach((dot, i) => {
                        dot.classList.toggle('active', i === index);
                    });
                }

                function showNotification(message, type = 'success') {
                    const notification = document.getElementById('notification');
                    notification.textContent = message;
                    notification.className = 'notification ' + type;
                    notification.classList.add('show');

                    setTimeout(() => {
                        notification.classList.remove('show');
                    }, 5000);
                }

                document.getElementById('search-input').addEventListener('input', function(e) {
                    searchTerm = e.target.value;
                    currentPage = 1;
                    loadModCards();
                });

                document.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.addEventListener('click', function() {
                        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                        this.classList.add('active');
                        currentFilter = this.dataset.category;
                        currentPage = 1;
                        loadModCards();
                    });
                });

                document.addEventListener('click', function(e) {
                    if (e.target && e.target.classList.contains('author-link')) {
                        e.preventDefault();
                        if (backend) {
                            backend.open_link(e.target.href);
                        }
                    }
                });

                const scrollbar = document.getElementById('custom-scrollbar');
                const root = document.documentElement;
                let scrollTimeout;

                function updateScrollbar() {
                    const scrollHeight = root.scrollHeight;
                    const clientHeight = root.clientHeight;

                    if (scrollHeight <= clientHeight) {
                        scrollbar.style.display = 'none';
                        return;
                    }

                    scrollbar.style.display = 'block';
                    const scrollTop = root.scrollTop;
                    const scrollPercentage = scrollTop / (scrollHeight - clientHeight);

                    const thumbHeight = Math.max(30, clientHeight * (clientHeight / scrollHeight));
                    scrollbar.style.height = `${thumbHeight}px`;

                    const thumbPosition = (clientHeight - thumbHeight) * scrollPercentage;
                    scrollbar.style.top = `${thumbPosition}px`;

                    scrollbar.classList.add('visible');
                    clearTimeout(scrollTimeout);
                    scrollTimeout = setTimeout(() => {
                        scrollbar.classList.remove('visible');
                    }, 1500);
                }

                window.addEventListener('scroll', updateScrollbar, { passive: true });
                window.addEventListener('resize', updateScrollbar);

                const tooltip = document.getElementById('custom-tooltip');

                document.addEventListener('mouseover', function(e) {
                    if (e.target.classList.contains('has-tooltip')) {
                        const target = e.target;
                        const isTruncated = target.scrollHeight > target.clientHeight || target.scrollWidth > target.clientWidth;

                        if (isTruncated) {
                            const tooltipText = target.dataset.tooltipText || target.textContent;
                            tooltip.textContent = tooltipText;
                            tooltip.style.display = 'block';
                        }
                    }
                });

                document.addEventListener('mouseout', function(e) {
                    if (e.target.classList.contains('has-tooltip')) {
                        tooltip.style.display = 'none';
                    }
                });

                document.addEventListener('mousemove', function(e) {
                    if (tooltip.style.display === 'block') {
                        tooltip.style.left = (e.clientX + 15) + 'px';
                        tooltip.style.top = (e.clientY + 15) + 'px';
                    }
                });
            });
            </script>
        </body>
        </html>
"""
# --- END OF MODIFICATION ---