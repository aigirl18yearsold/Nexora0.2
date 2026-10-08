from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Nexora — Discover Your Next Opportunity</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f6f8ff;
            color: #172033;
        }

        nav {
            background: white;
            padding: 18px 7%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e8eaf2;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .logo {
            font-size: 25px;
            font-weight: bold;
            color: #4f46e5;
        }

        .nav-button {
            background: #4f46e5;
            color: white;
            padding: 10px 18px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: bold;
        }

        .hero {
            text-align: center;
            padding: 70px 20px 50px;
        }

        .hero h1 {
            font-size: 46px;
            margin-bottom: 18px;
        }

        .hero h1 span {
            color: #4f46e5;
        }

        .hero p {
            font-size: 19px;
            color: #667085;
            max-width: 650px;
            margin: auto;
            line-height: 1.6;
        }

        .search-box {
            max-width: 650px;
            margin: 30px auto 0;
            display: flex;
            background: white;
            padding: 8px;
            border-radius: 14px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }

        .search-box input {
            flex: 1;
            border: none;
            outline: none;
            padding: 15px;
            font-size: 16px;
        }

        .search-box button {
            border: none;
            background: #4f46e5;
            color: white;
            padding: 0 22px;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
        }

        .section {
            max-width: 1100px;
            margin: 20px auto 70px;
            padding: 0 20px;
        }

        .section h2 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 30px;
        }

        .categories {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
        }

        .card {
            background: white;
            padding: 28px 20px;
            border-radius: 16px;
            text-align: center;
            text-decoration: none;
            color: #172033;
            border: 1px solid #e9ebf3;
            transition: 0.2s;
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }

        .icon {
            font-size: 35px;
            margin-bottom: 12px;
        }

        .card h3 {
            margin-bottom: 8px;
        }

        .card p {
            color: #667085;
            font-size: 14px;
            line-height: 1.4;
        }

        footer {
            text-align: center;
            padding: 30px;
            background: #111827;
            color: #cbd5e1;
        }

        @media (max-width: 800px) {
            .categories {
                grid-template-columns: repeat(2, 1fr);
            }

            .hero h1 {
                font-size: 36px;
            }
        }

        @media (max-width: 500px) {
            .categories {
                grid-template-columns: 1fr;
            }

            .search-box {
                flex-direction: column;
                gap: 8px;
            }

            .search-box button {
                padding: 14px;
            }
        }
    </style>
</head>

<body>

<nav>
    <div class="logo">🚀 Nexora</div>
    <a href="#" class="nav-button">Sign In</a>
</nav>

<section class="hero">

    <h1>Discover Your <span>Next Opportunity.</span></h1>

    <p>
        Find scholarships, competitions, hackathons, research,
        internships and other opportunities built for ambitious students.
    </p>

    <div class="search-box">
        <input
            type="text"
            placeholder="Search scholarships, hackathons, research..."
        >
        <button>Search</button>
    </div>

</section>

<section class="section">

    <h2>Explore Opportunities</h2>

    <div class="categories">

        <a href="#" class="card">
            <div class="icon">🎓</div>
            <h3>Scholarships</h3>
            <p>Find financial support for your education.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">🏆</div>
            <h3>Competitions</h3>
            <p>Discover challenges where your skills can shine.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">💻</div>
            <h3>Hackathons</h3>
            <p>Build, compete and solve real-world problems.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">🔬</div>
            <h3>Research</h3>
            <p>Explore research programs and opportunities.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">💼</div>
            <h3>Internships</h3>
            <p>Find opportunities to gain real experience.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">🥇</div>
            <h3>Olympiads</h3>
            <p>Discover academic and STEM competitions.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">🌎</div>
            <h3>Global Programs</h3>
            <p>Explore international student opportunities.</p>
        </a>

        <a href="#" class="card">
            <div class="icon">✨</div>
            <h3>Featured</h3>
            <p>See opportunities selected for Nexora users.</p>
        </a>

    </div>

</section>

<footer>
    <p>© 2026 Nexora — Discover. Build. Grow.</p>
</footer>

</body>
</html>
"""


if __name__ == "__main__":
    app.run()