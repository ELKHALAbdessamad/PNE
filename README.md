<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Profil GitHub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .header {
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }

        .header-content {
            position: relative;
            z-index: 1;
        }

        .profile-title {
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { filter: drop-shadow(0 0 5px rgba(255, 107, 107, 0.5)); }
            to { filter: drop-shadow(0 0 20px rgba(78, 205, 196, 0.5)); }
        }

        .profile-subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 10px;
        }

        .content {
            padding: 40px;
        }

        .intro-section {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
            transform: translateY(0);
            transition: transform 0.3s ease;
        }

        .intro-section:hover {
            transform: translateY(-5px);
        }

        .intro-text {
            font-size: 1.1em;
            line-height: 1.6;
            text-align: center;
        }

        .chart-section {
            background: #2d3748;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }

        .chart-title {
            color: white;
            font-size: 1.5em;
            font-weight: 600;
            text-align: center;
            margin-bottom: 30px;
        }

        .chart-container {
            position: relative;
            height: 200px;
            background: #1a202c;
            border-radius: 10px;
            padding: 20px;
            overflow: hidden;
        }

        .chart-grid {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 40px 40px;
        }

        .chart-svg {
            width: 100%;
            height: 100%;
            position: relative;
            z-index: 2;
        }

        .chart-bar {
            fill: #4ecdc4;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .chart-bar:hover {
            fill: #ff6b6b;
            transform: translateY(-2px);
        }

        .chart-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            color: #a0aec0;
            font-size: 0.8em;
        }

        .about-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        }

        .about-title {
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .about-items {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }

        .about-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 10px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .about-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        .about-item-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .about-item-title {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 1.1em;
        }

        .about-item-text {
            line-height: 1.5;
            opacity: 0.9;
        }

        .floating-elements {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .floating-element {
            position: absolute;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
        }

        .floating-element:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
        .floating-element:nth-child(2) { top: 20%; right: 10%; animation-delay: 1s; }
        .floating-element:nth-child(3) { bottom: 20%; left: 20%; animation-delay: 2s; }
        .floating-element:nth-child(4) { bottom: 10%; right: 20%; animation-delay: 3s; }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
        }

        @media (max-width: 768px) {
            .profile-title { font-size: 2em; }
            .content { padding: 20px; }
            .about-items { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="floating-elements">
        <div class="floating-element">🚀</div>
        <div class="floating-element">💻</div>
        <div class="floating-element">⚡</div>
        <div class="floating-element">🌟</div>
    </div>

    <div class="container">
        <div class="header">
            <div class="header-content">
                <div class="profile-subtitle">VotreNom-VotrePrenom-USERNAME / README.md</div>
                <h1 class="profile-title">Bienvenue sur Mon Profil GitHub 👨‍💻</h1>
            </div>
        </div>

        <div class="content">
            <div class="intro-section">
                <p class="intro-text">
                    Salut, je suis <strong>Votre Nom</strong> ! Je suis un "Futur Ingénieur IT & Réseau" actuellement en formation. 
                    Mon objectif est de créer des "solutions innovantes" qui comblent le fossé entre la technologie et les problèmes du monde réel. 
                    Je suis passionné par le "développement logiciel", l'"ingénierie réseau", et l'"innovation".
                </p>
            </div>

            <div class="chart-section">
                <h2 class="chart-title">USERNAME Votre Nom's Graphique de Contributions</h2>
                <div class="chart-container">
                    <div class="chart-grid"></div>
                    <svg class="chart-svg" viewBox="0 0 800 120">
                        <!-- Bars representing contributions -->
                        <rect class="chart-bar" x="20" y="100" width="15" height="20" rx="2"></rect>
                        <rect class="chart-bar" x="45" y="110" width="15" height="10" rx="2"></rect>
                        <rect class="chart-bar" x="70" y="105" width="15" height="15" rx="2"></rect>
                        <rect class="chart-bar" x="95" y="115" width="15" height="5" rx="2"></rect>
                        <rect class="chart-bar" x="120" y="110" width="15" height="10" rx="2"></rect>
                        <rect class="chart-bar" x="145" y="100" width="15" height="20" rx="2"></rect>
                        <rect class="chart-bar" x="170" y="90" width="15" height="30" rx="2"></rect>
                        <rect class="chart-bar" x="195" y="80" width="15" height="40" rx="2"></rect>
                        <rect class="chart-bar" x="220" y="70" width="15" height="50" rx="2"></rect>
                        <rect class="chart-bar" x="245" y="40" width="15" height="80" rx="2"></rect>
                        <rect class="chart-bar" x="270" y="20" width="15" height="100" rx="2"></rect>
                        <rect class="chart-bar" x="295" y="30" width="15" height="90" rx="2"></rect>
                        <rect class="chart-bar" x="320" y="50" width="15" height="70" rx="2"></rect>
                        <rect class="chart-bar" x="345" y="80" width="15" height="40" rx="2"></rect>
                        <rect class="chart-bar" x="370" y="95" width="15" height="25" rx="2"></rect>
                        <rect class="chart-bar" x="395" y="110" width="15" height="10" rx="2"></rect>
                        <rect class="chart-bar" x="420" y="115" width="15" height="5" rx="2"></rect>
                        <rect class="chart-bar" x="445" y="110" width="15" height="10" rx="2"></rect>
                        <rect class="chart-bar" x="470" y="100" width="15" height="20" rx="2"></rect>
                        <rect class="chart-bar" x="495" y="85" width="15" height="35" rx="2"></rect>
                        <rect class="chart-bar" x="520" y="75" width="15" height="45" rx="2"></rect>
                        <rect class="chart-bar" x="545" y="60" width="15" height="60" rx="2"></rect>
                        <rect class="chart-bar" x="570" y="70" width="15" height="50" rx="2"></rect>
                        <rect class="chart-bar" x="595" y="90" width="15" height="30" rx="2"></rect>
                        <rect class="chart-bar" x="620" y="105" width="15" height="15" rx="2"></rect>
                        <rect class="chart-bar" x="645" y="115" width="15" height="5" rx="2"></rect>
                        <rect class="chart-bar" x="670" y="110" width="15" height="10" rx="2"></rect>
                        <rect class="chart-bar" x="695" y="100" width="15" height="20" rx="2"></rect>
                        <rect class="chart-bar" x="720" y="90" width="15" height="30" rx="2"></rect>
                        <rect class="chart-bar" x="745" y="95" width="15" height="25" rx="2"></rect>
                    </svg>
                </div>
                <div class="chart-labels">
                    <span>Jan</span>
                    <span>Fév</span>
                    <span>Mar</span>
                    <span>Avr</span>
                    <span>Mai</span>
                    <span>Jun</span>
                    <span>Jul</span>
                    <span>Aoû</span>
                    <span>Sep</span>
                    <span>Oct</span>
                    <span>Nov</span>
                    <span>Déc</span>
                </div>
            </div>

            <div class="about-section">
                <h2 class="about-title">👨‍💻 À Propos de Moi</h2>
                <div class="about-items">
                    <div class="about-item">
                        <div class="about-item-icon">✨</div>
                        <div class="about-item-title">Passionné de Technologie</div>
                        <div class="about-item-text">
                            Je suis passionné par la résolution de problèmes et l'utilisation de la technologie pour avoir un impact significatif.
                        </div>
                    </div>
                    <div class="about-item">
                        <div class="about-item-icon">🚀</div>
                        <div class="about-item-title">Construire l'Avenir</div>
                        <div class="about-item-text">
                            Avec une base solide en programmation et en réseaux, je vise à contribuer à la création d'un monde plus connecté.
                        </div>
                    </div>
                    <div class="about-item">
                        <div class="about-item-icon">💡</div>
                        <div class="about-item-title">Innovation & Créativité</div>
                        <div class="about-item-text">
                            J'aime explorer de nouvelles technologies et créer des solutions innovantes pour des défis complexes.
                        </div>
                    </div>
                    <div class="about-item">
                        <div class="about-item-icon">🌐</div>
                        <div class="about-item-title">Ingénierie Réseau</div>
                        <div class="about-item-text">
                            Spécialisé dans la conception et l'optimisation d'infrastructures réseau modernes et sécurisées.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Animation des barres du graphique
        document.addEventListener('DOMContentLoaded', function() {
            const bars = document.querySelectorAll('.chart-bar');
            
            bars.forEach((bar, index) => {
                setTimeout(() => {
                    bar.style.opacity = '0';
                    bar.style.transform = 'scaleY(0)';
                    bar.style.transformOrigin = 'bottom';
                    bar.style.transition = 'all 0.5s ease';
                    
                    setTimeout(() => {
                        bar.style.opacity = '1';
                        bar.style.transform = 'scaleY(1)';
                    }, 100);
                }, index * 50);
            });

            // Effet de parallaxe sur le scroll
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const parallax = document.querySelector('.header');
                const speed = scrolled * 0.5;
                parallax.style.transform = `translateY(${speed}px)`;
            });

            // Animation des éléments au survol
            const aboutItems = document.querySelectorAll('.about-item');
            aboutItems.forEach(item => {
                item.addEventListener('mouseenter', function() {
                    this.style.background = 'rgba(255, 255, 255, 0.2)';
                });
                
                item.addEventListener('mouseleave', function() {
                    this.style.background = 'rgba(255, 255, 255, 0.1)';
                });
            });
        });
    </script>
</body>
</html>
