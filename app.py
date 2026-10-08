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

<a href="#scholarships"