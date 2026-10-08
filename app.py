
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

<title>Nexora — Opportunities</title>

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
    padding: 65px 20px 45px;
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
}

.section,
.scholarships,
.details {
    max-width: 1100px;
    margin: 20px auto 70px;
    padding: 0 20px;
}

.section h2,
.scholarships h2 {
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

.card p,
.opportunity p {
    color: #667085;
    font-size: 14px;
    line-height: 1.5;
}

.scholarships,
.details {
    display: none;
}

.subtitle {
    color: #667085;
    margin-bottom: 25px;
}

.opportunity {
    background: white;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 16px;
    border: 1px solid #e9ebf3;
}

.opportunity h3 {
    margin-bottom: 8px;
}

.opportunity p {
    margin-bottom: 12px;
}

.tag {
    display: inline-block;
    background: #eef2ff;
    color: #4f46e5;
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 13px;
    margin: 4px 4px 4px 0;
}

.view-button {
    display: inline-block;
    margin-top: 15px;
    background: #4f46e5;
    color: white;
    padding: 11px 18px;
    border-radius: 9px;
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
}

.back {
    display: inline-block;
    margin-bottom: 25px;
    color: #4f46e5;
    font-weight: bold;
    cursor: pointer;
}

.details-box {
    background: white;
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #e9ebf3;
}

.details-box h1 {
    margin-bottom: 12px;
}

.details-box h3 {
    margin-top: 25px;
    margin-bottom: 8px;
}

.details-box p {
    color: #667085;
    line-height: 1.6;
}

.apply-button {
    display: inline-block;
    margin-top: 25px;
    background: #16a34a;
    color: white;
    padding: 14px 22px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
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

    .details-box {
        padding: 22px;
    }
}
</style>
</head>

<body>

<nav>
    <div class="logo">🚀 Nexora</div>
    <a href="#" class="nav-button">Sign In</a>
</nav>

<section class="hero" id="home">

    <h1>Discover Your <span>Next Opportunity.</span></h1>

    <p>
        Find scholarships, competitions, hackathons, research,
        internships and other opportunities built for ambitious students.
    </p>

    <div class="search-box">
        <input type="text"
        placeholder="Search scholarships, hackathons, research...">
        <button>Search</button>
    </div>

</section>

<section class="section" id="categories">

<h2>Explore Opportunities</h2>

<div class="categories">

<a href="#scholarships" class="card"
onclick="showScholarships()">
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


<section class="scholarships" id="scholarships">

<div class="back" onclick="goHome()">← Back to opportunities</div>

<h2>🎓 Scholarships</h2>

<p class="subtitle">
Explore scholarships and financial opportunities for students.
</p>

<div class="opportunity">

<h3>Global Undergraduate Scholarship</h3>

<p>
Financial support opportunity for talented students
planning undergraduate study.
</p>

<span class="tag">Undergraduate</span>
<span class="tag">International</span>
<span class="tag">Financial Aid</span>

<br>

<a class="view-button"
onclick="showDetails()">
View Details →
</a>

</div>


<div class="opportunity">

<h3>STEM Student Scholarship</h3>

<p>
Scholarship opportunity for students interested in
science, technology, engineering and mathematics.
</p>

<span class="tag">STEM</span>
<span class="tag">Students</span>
<span class="tag">Scholarship</span>

</div>


<div class="opportunity">

<h3>Future Leaders Scholarship</h3>

<p>
Support for students demonstrating leadership,
community involvement and academic potential.
</p>

<span class="tag">Leadership</span>
<span class="tag">International</span>

</div>

</section>


<section class="details" id="details">

<div class="back" onclick="showScholarships()">
← Back to scholarships
</div>

<div class="details-box">

<h1>Global Undergraduate Scholarship</h1>

<p>
A scholarship opportunity designed to support talented
students pursuing undergraduate education.
</p>

<h3>🎓 Level</h3>
<p>Undergraduate</p>

<h3>🌎 Location</h3>
<p>International</p>

<h3>💰 Funding</h3>
<p>Financial support for eligible students.</p>

<h3>📅 Deadline</h3>
<p>Check the official opportunity website for the current deadline.</p>

<h3>👤 Eligibility</h3>
<p>
Eligibility depends on the specific scholarship requirements.
Applicants should verify all requirements before applying.
</p>

<h3>📋 Application</h3>
<p>
Nexora will provide the official application source
once the opportunity has been verified.
</p>

<a href="#" class="apply-button">
Official Apply →
</a>

</div>

</section>


<footer>
<p>© 2026 Nexora — Discover. Build. Grow.</p>
</footer>


<script>

function showScholarships() {

    document.getElementById("home").style.display = "none";
    document.getElementById("categories").style.display = "none";
    document.getElementById("details").style.display = "none";
    document.getElementById("scholarships").style.display = "block";

    window.scrollTo(0, 0);
}


function showDetails() {

    document.getElementById("home").style.display = "none";
    document.getElementById("categories").style.display = "none";
    document.getElementById("scholarships").style.display = "none";
    document.getElementById("details").style.display = "block";

    window.scrollTo(0, 0);
}


function goHome() {

    document.getElementById("details").style.display = "none";
    document.getElementById("scholarships").style.display = "none";
    document.getElementById("home").style.display = "block";
    document.getElementById("categories").style.display = "block";

    window.scrollTo(0, 0);
}

</script>

</body>
</html>
"""


