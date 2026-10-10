import os
import json
import sqlite3
import smtplib
from email.message import EmailMessage
from functools import wraps
from flask import Flask, request, redirect, url_for, session, flash, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-before-production")
DB_PATH = os.environ.get("NEXORA_DB_PATH", "nexora.db")

CATEGORIES = {
    "Scholarships": ("🎓", "Funding and study"),
    "Competitions": ("🏆", "Show your skills"),
    "Hackathons": ("💻", "Build and solve problems"),
    "Research": ("🔬", "Explore questions with mentors"),
    "Internships": ("🚀", "Gain practical experience"),
    "Olympiads": ("🧠", "Academic and STEM challenges"),
    "Mentorship": ("🤝", "Learn from college-student mentors"),
}
INTERESTS = [
    "Technology & AI", "Science & STEM", "Business & Entrepreneurship",
    "Writing & Communication", "Research & Academics", "Social Impact",
    "Arts & Design", "General"
]

# Seed directory. Once saved in SQLite, you can add/update listings from /admin
# without replacing this file. Confirm dates and eligibility on the official sites.
SEED_ITEMS = [
  {
    "id": "1",
    "title": "KAIST International Undergraduate Scholarship",
    "organization": "KAIST",
    "category": "Scholarships",
    "location": "South Korea",
    "level": "Undergraduate",
    "funding": "Full tuition + monthly allowance + insurance",
    "deadline": "Check current admissions cycle",
    "status": "Check official page",
    "eligibility": "International undergraduate applicants; scholarship considered with admission",
    "official_url":
     "https://admission.kaist.ac.kr/intl-undergraduate/support/scholarships/kaist",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "2",
    "title": "MEXT Undergraduate Scholarship",
    "organization": "Government of Japan",
    "category": "Scholarships",
    "location": "Japan",
    "level": "Undergraduate",
    "funding": "Government-funded; terms vary by track",
    "deadline": "Check Japanese Embassy page",
    "status": "Check official page",
    "eligibility": "International students; apply through the current country-specific route",
    "official_url": "https://www.studyinjapan.go.jp/en/planning/scholarships/mext-scholarships/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "3",
    "title": "Global Korea Scholarship (GKS-U)",
    "organization": "Government of Korea",
    "category": "Scholarships",
    "location": "South Korea",
    "level": "Undergraduate",
    "funding": "Tuition, airfare, language training and allowance per official terms",
    "deadline": "2027 notice published; verify current route",
    "status": "Check official page",
    "eligibility": "International applicants; check the current guidelines and Bangladesh notices",
    "official_url": "https://www.studyinkorea.go.kr/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "4",
    "title": "Türkiye Scholarships",
    "organization": "Government of Türkiye",
    "category": "Scholarships",
      "location": "Türkiye",
    "level": "Undergraduate / Graduate",
    "funding": "Tuition, stipend, accommodation, insurance and travel per program",
    "deadline": "Usually Jan–Feb; check next cycle",
    "status": "Check official page",
    "eligibility": "International applicants meeting program age and academic criteria",
    "official_url": "https://www.turkiyeburslari.gov.tr/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "5",
    "title": "Stipendium Hungaricum",
    "organization": "Government of Hungary",
    "category": "Scholarships",
    "location": "Hungary",
    "level": "Undergraduate / Graduate",
    "funding": "Tuition support and other benefits per call",
    "deadline": "Check next call",
    "status": "Check official page",
    "eligibility": "Eligibility depends on sending-partner country and current call",
    "official_url": "https://stipendiumhungaricum.hu/apply/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "6",
    "title": "Reach Oxford Scholarship",
    "organization": "University of Oxford",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate",
    "funding": "Course fees, living costs and one return airfare for eligible students",
    "deadline": "Check official cycle",
    "status": "Check eligible students from low-income countries; very limited awards",
    "official_url": "https://www.ox.ac.uk/admissions/undergraduate/fees-and-funding/oxford-support/reach-oxford-scholarship",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "7",
    "title": "Cambridge Trust Scholarships",
    "organization": "Cambridge Trust",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate / Graduate",
    "funding": "Varies by award",
    "deadline": "Check official page",
    "status": "Check official page",
    "eligibility": "Eligibility and funding vary; undergraduate awards are limited",
    "official_url": "https://www.cambridgetrust.org/scholarships/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "8",
    "title": "MIT Undergraduate Financial Aid",
    "organization": "Massachusetts Institute of Technology",
    "category": "Scholarships",
    "location": "United States",
    "level": "Undergraduate",
    "funding": "Need-based aid; international students eligible",
    "deadline": "Apply with admission/aid materials",
    "status": "Check official page",
    "eligibility": "Not a separate merit scholarship; review MIT's current aid instructions",
    "official_url": "https://sfs.mit.edu/undergraduate-students/financial-aid/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
]

      },
  {
    "id": "9",
    "title": "Harvard College Financial Aid",
    "organization": "Harvard University",
    "category": "Scholarships",
    "location": "United States",
    "level": "Undergraduate",
    "funding": "Need-based financial aid",
    "deadline": "Apply with admission/aid materials",
    "status": "Check official page",
    "eligibility": "International applicants may apply for need-based aid",
    "official_url": "https://college.harvard.edu/financial-aid",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "10",
    "title": "Princeton Undergraduate Financial Aid",
    "organization": "Princeton University",
    "category": "Scholarships",
    "location": "United States",
    "level": "Undergraduate",
    "funding": "Need-based aid",
    "deadline": "Apply with admission/aid materials",
    "status": "Check official page",
    "eligibility": "International applicants may apply; admission is highly selective",
    "official_url": "https://admission.princeton.edu/cost-aid",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "11",
    "title": "Yale Undergraduate Financial Aid",
    "organization": "Yale University",
    "category": "Scholarships",
    "location": "United States",
    "level": "Undergraduate",
    "funding": "Need-based aid",
      "deadline": "Apply with admission/aid materials",
    "status": "Check official page",
    "eligibility": "International applicants may apply for need-based aid",
    "official_url": "https://admissions.yale.edu/financial-aid",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "12",
    "title": "Amherst College Financial Aid",
    "organization": "Amherst College",
    "category": "Scholarships",
    "location": "United States",
    "level": "Undergraduate",
    "funding": "Need-based aid",
    "deadline": "Check official page",
    "status": "Check official page",
    "eligibility": "International students can apply for financial aid",
    "official_url": "https://www.amherst.edu/admission/financial_aid",
    "interests": [
      "Technology & AI"
    ]
  },
  {
    "id": "13",
    "title": "Bowdoin College Financial Aid",
    "organization": "Bowdoin College",
    "category": "Scholarships",
    "location": "United States",
    "level": "Undergraduate",
    "funding": "Need-based aid",
    "deadline": "Check official page",
    "status": "Check official page",
    "eligibility": "Review current international applicant and aid policies",
    "official_url": "https://www.bowdoin.edu/admissions/tuition-aid/",
    "interests": [
      "Technology & AI"
    ]
  },
  {
    "id": "14",
    "title": "Lester B. Pearson International Scholarship",
    "organization": "University of Toronto",
    "category": "Scholarships",
    "location": "Canada",
    "level": "Undergraduate",
    "funding": "Tuition, books, incidental fees and residence support per award",
    "deadline": "Check current cycle",
    "status": "Check official page",
    "eligibility": "International high-school students; school nomination required",
    "official_url": "https://future.utoronto.ca/pearson/about/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "15",
    "title": "Global Futures Scholarships",
    "organization": "University of Manchester",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate / Master's",
    "funding": "Partial merit awards; amount varies",
    "deadline": "2027 entry page available; check country deadline",
    "status": "Check official page",
    "eligibility": "Bangladesh is listed among eligible countries; course offer required",
    "official_url": "https://www.manchester.ac.uk/study/international/finance-and-scholarships/funding/global-futures-scholarship/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "16",
    "title": "Vice-Chancellor's International Scholarship",
    "organization": "Newcastle University",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate",
    "funding": "£7,000 per academic year (2027 entry page)",
    "deadline": "Awards considered through the cycle",
    "status": "Check official page",
    "eligibility": "Bangladesh is among eligible domiciles; course/offer rules apply",
      "official_url": "https://www.ncl.ac.uk/undergraduate/fees-funding/scholarships-bursaries/vc-international/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "17",
    "title": "Undergraduate International Excellence Scholarship",
    "organization": "Cardiff University",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate",
    "funding": "£10,000 tuition discount (2027 entry)",
    "deadline": "2 April 2027 listed; verify official page",
    "status": "Check official page",
    "eligibility": "Eligible international students holding an offer; conditions apply",
    "official_url": "https://www.cardiff.ac.uk/study/international/funding-and-fees/international-scholarships/undergraduate-excellence-scholarships",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "18",
    "title": "Vice-Chancellor's Undergraduate International Scholarship",
    "organization": "Cardiff University",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate",
    "funding": "£3,500–£5,000 tuition discount (2027 entry)",
    "deadline": "30 June 2027 listed; verify official page",
    "status": "Check official page",
    "eligibility": "Eligible overseas-fee students; country/course rules apply",
    "official_url": "https://www.cardiff.ac.uk/study/international/funding-and-fees/international-scholarships/vice-chancellors-international-scholarship-ug",
    "interests": [
      "Research & Academics"
    ]
  },
    {
    "id": "19",
    "title": "South Asia Scholarship",
    "organization": "London Metropolitan University",
    "category": "Scholarships",
    "location": "United Kingdom",
    "level": "Undergraduate / Master's",
    "funding": "Tuition discount; terms vary",
    "deadline": "Check current entry cycle",
    "status": "Check official page",
    "eligibility": "Bangladesh and other South Asian citizenships; deposit and course conditions apply",
    "official_url": "https://www.londonmet.ac.uk/applying/funding-your-studies/scholarships/south-asia-scholarships/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "20",
    "title": "Egyptian Government / Al-Azhar Scholarships",
    "organization": "Bangladesh Ministry of Education",
    "category": "Scholarships",
    "location": "Egypt",
    "level": "Undergraduate / Islamic studies",
    "funding": "Varies by official notice",
    "deadline": "Check latest Bangladesh ministry notice",
    "status": "Check official page",
    "eligibility": "Bangladeshi applicants; eligibility depends on the current official notice",
    "official_url": "https://shed.gov.bd/pages/moedu-scholarships/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "21",
    "title": "Conrad Challenge",
    "organization": "Conrad Foundation / U.S. Space & Rocket Center",
    "category": "Competitions",
    "location": "Global",
    "level": "High-school teams",
      "funding": "Prizes and recognition vary by track",
    "deadline": "2026–27 Activation Stage ends 30 Oct 2026",
    "status": "Check official page",
    "eligibility": "International student teams; check team, fee and submission rules",
    "official_url": "https://conrad.spacecenter.org/",
    "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "22",
    "title": "Technovation Challenge",
    "organization": "Technovation",
    "category": "Competitions",
    "location": "Global / virtual",
    "level": "Ages 8–18",
    "funding": "Awards and global recognition",
    "deadline": "2026–27 season starts October 2026; verify registration",
    "status": "Check official page",
    "eligibility": "Free competition and curriculum; age and team rules apply",
    "official_url": "https://technovationchallenge.org/competition/",
    "interests": [
      "Technology & AI"
    ]
  },
  {
    "id": "23",
    "title": "GENIUS Olympiad",
    "organization": "Terra Science and Education",
    "category": "Olympiads",
    "location": "Global",
    "level": "Grades 8–12",
    "funding": "Awards; some scholarship/publication opportunities",
    "deadline": "Check 2027 registration and country route",
    "status": "Check official page",
    "eligibility": "High-school projects in environment-related fields",
    "official_url": "https://geniusolympiad.org/",
    "interests": [
      "Science & STEM"
]
      },
  {
    "id": "24",
    "title": "DSH Hacks V2 — AI × Healthcare",
    "organization": "NXT Horizon / STEMise",
    "category": "Hackathons",
    "location": "Online / global",
    "level": "Student builders",
    "funding": "In-kind prizes listed by organizer",
    "deadline": "Listed closing date 24 Oct 2026; verify event page",
    "status": "Check official page",
    "eligibility": "Student builders worldwide; read official rules",
    "official_url": "https://nxthorizon.org/competitions",
    "interests": [
      "Technology & AI",
      "Science & STEM",
      "Social Impact"
    ]
  },
  {
    "id": "25",
    "title": "Neighborhood Hacks 2026",
    "organization": "Neighborhood Hacks",
    "category": "Hackathons",
    "location": "Virtual / global",
    "level": "High school students",
    "funding": "Organizer lists prizes",
    "deadline": "16–24 Oct 2026 listed",
    "status": "Check official page",
    "eligibility": "High-school students worldwide; verify registration and team rules",
    "official_url": "https://neighborhoodhacks.org/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "26",
    "title": "World Challenger — Global IT, IoT & AI Challenge",
    "organization": "World Challenger",
    "category": "Competitions",
    "location": "Online / global",
    "level": "Grades 5–12 school teams",
    "funding": "Awards vary",
    "deadline": "Check next official cycle",
    "status": "Check official page",
    "eligibility": "School teams worldwide; school participation rules apply",
    "official_url": "https://www.worldchallenger.org/",
    "interests": [
      "Technology & AI"
    ]
  },
  {
    "id": "27",
    "title": "International Computer Science Competition",
    "organization": "ICSC",
    "category": "Competitions",
    "location": "Global / online",
    "level": "Middle school, high school and university",
    "funding": "Certificates/awards vary",
    "deadline": "2026 concluded; watch next edition",
    "status": "Check official page",
    "eligibility": "All countries; age division and computer access required",
    "official_url": "https://icscompetition.org/en/",
    "interests": [
      "Technology & AI",
      "Science & STEM"
    ]
  },
  {
    "id": "28",
    "title": "International Software Engineering Olympiad",
    "organization": "ISWEO",
    "category": "Olympiads",
    "location": "Online / global",
    "level": "Grades 9–12 or recent graduates",
    "funding": "Awards vary",
    "deadline": "Check next cycle; 2026 qualifier has passed",
    "status": "Check official page",
    "eligibility": "Organizer lists worldwide eligibility for grades 9–12/recent graduates, age 21 or younger",
    "official_url": "https://www.isweo.org/",
    "interests": [
      "Technology & AI",
        "Science & STEM"
    ]
  },
  {
    "id": "29",
    "title": "LBX Global Innovation Competition",
    "organization": "LBX",
    "category": "Competitions",
    "location": "Global",
    "level": "Middle and high school",
    "funding": "Regional/global showcases",
    "deadline": "Check 2026 season details",
    "status": "Check official page",
    "eligibility": "Check age, team, guardian and travel rules",
    "official_url": "https://www.lbx.org/",
    "interests": [
      "Business & Entrepreneurship"
    ]
  },
  {
    "id": "30",
    "title": "Sigma Olympics",
    "organization": "Sigma Olympics",
    "category": "Olympiads",
    "location": "Global",
    "level": "School students",
    "funding": "Medals/certificates per organizer",
    "deadline": "2026–27 registration Sep–Jan; verify country representative",
    "status": "Check official page",
    "eligibility": "Country representative and grade rules determine eligibility",
    "official_url": "https://sigmaolympics.com/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "31",
    "title": "STEMCo",
    "organization": "STEMCo",
    "category": "Competitions",
    "location": "International",
      "level": "School students",
    "funding": "Awards vary",
    "deadline": "Science rounds Dec 2026 / Jan 2027 listed; verify registration",
    "status": "Check official page",
    "eligibility": "Maths, science and English divisions; travel/fees may apply",
    "official_url": "https://stemco.org/",
    "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "32",
    "title": "XPERTSTEM International STEM Competition",
    "organization": "XPERTSTEM",
    "category": "Competitions",
    "location": "International",
    "level": "Grades 3–12",
    "funding": "Awards vary",
    "deadline": "2026–27 calendar on official site",
    "status": "Check official page",
    "eligibility": "Grade and event rules; in-person finals may require travel",
    "official_url": "https://xpertstem.org/",
    "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "33",
    "title": "Breakthrough Junior Challenge",
    "organization": "Breakthrough Prize Foundation",
    "category": "Competitions",
    "location": "Global",
    "level": "Ages 13–18",
    "funding": "Scholarship and prizes",
    "deadline": "Check next official cycle",
    "status": "Check official page",
    "eligibility": "Science explanation video; confirm current age and submission rules",
    "official_url": "https://breakthroughjuniorchallenge.org/",
      "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "34",
    "title": "Diamond Challenge",
    "organization": "University of Delaware Horn Entrepreneurship",
    "category": "Competitions",
    "location": "Global",
    "level": "High-school entrepreneurs",
    "funding": "Cash prizes/awards vary",
    "deadline": "Check 2026–27 cycle",
    "status": "Check official page",
    "eligibility": "High-school teams; track and team rules apply",
    "official_url": "https://diamondchallenge.org/",
    "interests": [
      "Business & Entrepreneurship",
      "Research & Academics"
    ]
  },
  {
    "id": "35",
    "title": "Blue Ocean Student Entrepreneur Competition",
    "organization": "Blue Ocean Entrepreneurship",
    "category": "Competitions",
    "location": "Global",
    "level": "High school students",
    "funding": "Cash prizes and recognition",
    "deadline": "Check next cycle",
    "status": "Check official page",
    "eligibility": "High-school students; pitch/video format",
    "official_url": "https://blueoceancompetition.org/",
    "interests": [
      "Business & Entrepreneurship"
    ]
  },
  {
    "id": "36",
    "title": "Congressional App Challenge",
    "organization": "U.S. House of Representatives",
    "category": "Competitions",
    "location": "United States",
    "level": "Middle/high school",
    "funding": "Recognition varies by district",
    "deadline": "Annual; check district deadline",
    "status": "Check official page",
      "eligibility": "Only eligible students in participating U.S. congressional districts",
    "official_url": "https://www.congressionalappchallenge.us/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "37",
    "title": "Regeneron International Science and Engineering Fair",
    "organization": "Society for Science",
    "category": "Competitions",
    "location": "International",
    "level": "Grades 9–12",
    "funding": "Awards vary",
    "deadline": "2027 fair dates listed; qualification required",
    "status": "Check official page",
    "eligibility": "Must qualify through an affiliated fair; local rules apply",
    "official_url": "https://www.societyforscience.org/isef/",
    "interests": [
      "Technology & AI",
      "Science & STEM"
    ]
  },
  {
    "id": "38",
    "title": "Regeneron Science Talent Search",
    "organization": "Society for Science",
    "category": "Olympiads",
    "location": "United States",
    "level": "High-school seniors",
    "funding": "Major research awards",
    "deadline": "2026 cycle deadline listed as 5 Nov 2026; verify rules",
    "status": "Check official page",
    "eligibility": "U.S. high-school seniors meeting citizenship/residency requirements; not global direct entry",
    "official_url": "https://www.societyforscience.org/regeneron-sts/",
    "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "39",
      "organization": "STEM Fellowship",
    "category": "Competitions",
    "location": "Canada / international details vary",
    "level": "High school / CEGEP",
    "funding": "Research and conference opportunities",
    "deadline": "Registration deadline listed as 18 Oct 2026; confirm fees",
    "status": "Check official page",
    "eligibility": "High school/CEGEP; participation may involve fees and travel",
    "official_url": "https://www.stemfellowship.org/hsbdc/2026-27",
    "interests": [
      "Technology & AI",
      "Science & STEM"
    ]
  },
  {
    "id": "40",
    "title": "International Astronomy and Astrophysics Competition",
    "organization": "IAAC",
    "category": "Competitions",
    "location": "International / online",
    "level": "School and university students",
    "funding": "Awards and certificates vary",
    "deadline": "Check current annual cycle",
    "status": "Check official page",
    "eligibility": "International participants; age and round rules apply",
    "official_url": "https://iaac.space/",
    "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "41",
    "title": "Google Summer of Code",
    "organization": "Google",
    "category": "Research",
    "location": "Global / remote",
    "level": "18+ contributors",
    "funding": "Stipend for accepted contributors",
    "deadline": "Annual cycle; check official page",
    "status": "Check official page",
    "eligibility": "Open-source mentored project program, not conventional employment",
      "official_url": "https://summerofcode.withgoogle.com/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "42",
    "title": "Outreachy Internships",
    "organization": "Outreachy",
    "category": "Internships",
    "location": "Remote; eligibility varies",
    "level": "18+",
    "funding": "Paid internship stipend",
    "deadline": "Check next application round",
    "status": "Check official page",
    "eligibility": "Applicants must meet Outreachy's eligibility rules and round requirements",
    "official_url": "https://www.outreachy.org/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "43",
    "title": "MLH Fellowship",
    "organization": "Major League Hacking",
    "category": "Hackathons",
    "location": "Remote / cohort-based",
    "level": "Students and recent graduates",
    "funding": "Program terms vary by cohort",
    "deadline": "Check next cohort",
    "status": "Check official page",
    "eligibility": "Eligibility, payment and time commitment vary by cohort",
    "official_url": "https://fellowship.mlh.io/",
    "interests": [
      "General"
    ]
  },
  {
    "id": "44",
    "title": "MIT PRIMES",
    "organization": "MIT",
    "category": "Research",
    "location": "United States / some remote research",
    "level": "High school students",
    "funding": "Research mentorship",
    "deadline": "Annual application cycle; check page",
    "status": "Check official page",
    "eligibility": "Specific geographic, grade and research-readiness requirements",
    "official_url": "https://math.mit.edu/research/highschool/primes/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "45",
    "title": "MIT Summer Research Program (MSRP)",
    "organization": "MIT",
    "category": "Internships",
    "location": "United States",
    "level": "Undergraduates",
    "funding": "Research experience; terms vary",
    "deadline": "Annual; check eligibility",
    "status": "Check official page",
    "eligibility": "Primarily for eligible undergraduates, not a general high-school internship",
    "official_url": "https://oge.mit.edu/msrp/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "46",
    "title": "Research Science Institute (RSI)",
      "organization": "Center for Excellence in Education / MIT",
    "category": "Internships",
    "location": "United States",
    "level": "High school students",
    "funding": "Research program",
    "deadline": "Annual cycle; check current dates",
    "status": "Check official page",
    "eligibility": "Highly selective; international eligibility and travel must be checked",
    "official_url": "https://www.cee.org/programs/research-science-institute",
    "interests": [
      "Technology & AI",
      "Science & STEM",
      "Research & Academics"
    ]
  },
  {
    "id": "47",
    "title": "Simons Summer Research Program",
    "organization": "Stony Brook University",
    "category": "Research",
    "location": "United States",
    "level": "High school juniors",
    "funding": "Research experience",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "Restrictions may include residency, grade and application requirements",
    "official_url": "https://www.stonybrook.edu/simons/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "48",
    "title": "Stanford SIMR",
    "organization": "Stanford University",
    "category": "Research",
    "location": "United States",
    "level": "High school students",
    "funding": "Research program",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "U.S. residency/citizenship and other restrictions may apply",
    "official_url": "https://simr.stanford.edu/",
      "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "49",
    "title": "UCSB Research Mentorship Program",
    "organization": "UC Santa Barbara",
    "category": "Research",
    "location": "United States",
    "level": "High school students",
    "funding": "Research mentorship; fees may apply",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "Check cost, age, course and visa requirements",
    "official_url": "https://summer.ucsb.edu/programs/research-mentorship-program",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "50",
    "title": "BU RISE Internship / Practicum",
    "organization": "Boston University",
    "category": "Internships",
    "location": "United States",
    "level": "High school students",
    "funding": "Research experience; cost/aid vary",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "Eligibility, fees and international participation rules apply",
    "official_url": "https://www.bu.edu/summer/high-school-programs/research-internship/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "51",
    "title": "Anson L. Clark Scholars Program",
    "organization": "Texas Tech University",
    "category": "Research",
    "location": "United States",
    "level": "High school juniors/seniors",
    "funding": "Research program; stipend terms on official page",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "Highly selective; check age, grade, citizenship and travel requirements",
    "official_url": "https://www.depts.ttu.edu/honors/academicsandenrichment/affiliatedandhighschool/clarks/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "52",
    "title": "Garcia Summer Research Program",
    "organization": "Stony Brook University",
    "category": "Internships",
    "location": "United States",
    "level": "High school students",
    "funding": "Research program; tuition may apply",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "Check program fees and international eligibility",
    "official_url": "https://www.stonybrook.edu/commcms/garcia/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "53",
    "title": "SHTEM Summer Internship Program",
    "organization": "Stanford University",
    "category": "Internships",
    "location": "United States / details vary",
    "level": "High school students",
    "funding": "Research experience",
    "deadline": "Annual cycle; check page",
    "status": "Check official page",
    "eligibility": "Eligibility and project availability vary",
    "official_url": "https://compression.stanford.edu/shtem-summer-internships",
    "interests": [
      "Technology & AI",
      "Research & Academics"
        ]
  },
  {
    "id": "54",
    "title": "AI4ALL Open Learning",
    "organization": "AI4ALL",
    "category": "Internships",
    "location": "Online",
    "level": "High school learners",
    "funding": "Free learning resources",
    "deadline": "Self-paced; check official page",
    "status": "Check official page",
    "eligibility": "Educational program, not necessarily a paid internship",
    "official_url": "https://ai-4-all.org/open-learning/",
    "interests": [
      "Technology & AI"
    ]
  },
  {
    "id": "55",
    "title": "NASA OSTEM Internships",
    "organization": "NASA",
    "category": "Internships",
    "location": "United States",
    "level": "Students",
    "funding": "Paid and unpaid roles vary",
    "deadline": "Multiple cycles; check each posting",
    "status": "Check official page",
    "eligibility": "Most positions require U.S. citizenship; do not assume international eligibility",
    "official_url": "https://intern.nasa.gov/",
    "interests": [
      "Science & STEM"
    ]
  },
  {
    "id": "56",
    "title": "CERN Student Opportunities",
    "organization": "CERN",
    "category": "Research",
    "location": "Switzerland / varies",
    "level": "University students",
    "funding": "Stipend/benefits vary",
    "deadline": "Multiple programs; check openings",
    "status": "Check official page",
    "eligibility": "Many roles require university enrollment and specific nationality/education conditions",
    "official_url": "https://careers.cern/",
    "interests": [
      "Research & Academics"
    ]
  },
  {
    "id": "57",
    "title": "UNICEF Internships",
    "organization": "UNICEF",
    "category": "Internships",
    "location": "Global / office-specific",
    "level": "Students and recent graduates",
    "funding": "Stipend may be provided under program rules",
    "deadline": "Apply to individual vacancies",
    "status": "Check official page",
    "eligibility": "Must meet vacancy education, age, language and work-authorization rules",
    "official_url": "https://www.unicef.org/careers/internships",
    "interests": [
      "General"
    ]
  },
  {
    "id": "58",
    "title": "World Bank Internship Program",
    "organization": "World Bank Group",
    "category": "Internships",
    "location": "Global / office-specific",
    "level": "Graduate students primarily",
    "funding": "Paid internship",
    "deadline": "Seasonal windows; check official page",
    "status": "Check official page",
    "eligibility": "Designed primarily for graduate students; requirements vary by posting",
    "official_url": "https://www.worldbank.org/en/about/careers/programs-and-internships",
    "interests": [
      "General"
    ]
  },
  {
    "id": "59",
    "title": "Pioneer Academics Research Program",
    "organization": "Pioneer Academics",
    "category": "Research",
    "location": "Online / global",
      "level": "High school students",
    "funding": "Mentored research; tuition/aid rules apply",
    "deadline": "Check current cohort",
    "status": "Check official page",
    "eligibility": "Selective academic research program, not a paid job; confirm fees and financial aid",
    "official_url": "https://pioneeracademics.com/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  },
  {
    "id": "60",
    "title": "Lumiere Research Scholar Program",
    "organization": "Lumiere Education",
    "category": "Internships",
    "location": "Online / global",
    "level": "High school students",
    "funding": "Mentored research; tuition/aid rules apply",
    "deadline": "Check current cohort",
    "status": "Check official page",
    "eligibility": "Not a paid internship; program fees and financial assistance vary",
    "official_url": "https://www.lumiere-education.com/",
    "interests": [
      "Technology & AI",
      "Research & Academics"
    ]
  }
]

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
            organization TEXT NOT NULL, category TEXT NOT NULL, location TEXT,
            level TEXT, funding TEXT, deadline TEXT, status TEXT, eligibility TEXT,
            official_url TEXT NOT NULL, interests TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, country TEXT DEFAULT '', education TEXT DEFAULT '',
            age INTEGER DEFAULT 0, interests TEXT DEFAULT '', newsletter TEXT DEFAULT 'weekly',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL,
            frequency TEXT DEFAULT 'weekly', created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS mentor_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            university TEXT NOT NULL, study_level TEXT NOT NULL, expertise TEXT NOT NULL,
            bio TEXT NOT NULL, status TEXT DEFAULT 'Pending review',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id))""")
        con.execute("""CREATE TABLE IF NOT EXISTS mentorship_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL,
            mentor_id INTEGER NOT NULL, topic TEXT NOT NULL, message TEXT NOT NULL,
            student_payment_status TEXT DEFAULT 'Not configured',
            mentor_payment_status TEXT DEFAULT 'Not configured',
            status TEXT DEFAULT 'Pending', created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        count = con.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
        if count == 0:
            for o in SEED_ITEMS:
                con.execute("""INSERT INTO opportunities
                   (title,organization,category,location,level,funding,deadline,status,eligibility,official_url,interests)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                    (o["title"],o["organization"],o["category"],o["location"],o["level"],o["funding"],
                     o["deadline"],o["status"],o["eligibility"],o["official_url"],json.dumps(o["interests"])))
init_db()

def all_items():
    with db() as con:
        rows=con.execute("SELECT * FROM opportunities ORDER BY title COLLATE NOCASE").fetchall()
    result=[]
    for r in rows:
        d=dict(r)
        try: d["interests"]=json.loads(d.get("interests") or "[]")
        except (ValueError, TypeError): d["interests"]=[]
        result.append(d)
    return result

def mail_settings_ready():
    return all(os.environ.get(k) for k in ("SMTP_HOST","SMTP_PORT","SMTP_USER","SMTP_PASSWORD","MAIL_FROM"))

def send_email(to, subject, body):
    if not mail_settings_ready():
        return False
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=os.environ["MAIL_FROM"]
    msg["To"]=to
    msg.set_content(body)
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.send_message(msg)
    return True

def notify_new_listing(item):
    if not mail_settings_ready(): return
    with db() as con:
        subscribers=con.execute("SELECT email FROM subscribers").fetchall()
    body=f"""A new opportunity was added to Nexora 0.2:

{item['title']}
Category: {item['category']}
Organizer: {item['organization']}
Deadline/cycle: {item['deadline']}
Official page: {item['official_url']}

Please verify the current deadline, eligibility and rules with the organizer.
"""
    for sub in subscribers:
        try: send_email(sub["email"], "New opportunity on Nexora: "+item["title"], body)
        except Exception as exc: print("Newsletter send failed:", exc)

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to use your profile.", "info")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped
    BASE = r"""
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title or 'Nexora 0.2 — Discover Your Next Opportunity' }}</title>
<style>
:root{--bg:#f5f6fc;--ink:#202943;--muted:#748097;--purple:#6045dc;--line:#e5e9f3}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif}
header{position:sticky;top:0;z-index:5;background:#ffffffed;border-bottom:1px solid var(--line)}.nav{max-width:1160px;margin:auto;padding:14px 18px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}.logo{font-weight:900;font-size:22px;color:var(--purple);text-decoration:none}.logo span{color:var(--ink)}nav{display:flex;gap:12px;flex-wrap:wrap}nav a{color:var(--ink);text-decoration:none;font-size:14px;font-weight:650}
main{max-width:1160px;margin:auto;padding:24px 18px 55px}.muted{color:var(--muted);font-size:13px;line-height:1.5}.hero{background:linear-gradient(125deg,#1d2751,#4934a4 62%,#8466ff);border-radius:26px;color:white;padding:clamp(25px,6vw,58px)}.eyebrow{text-transform:uppercase;font-weight:800;letter-spacing:2px;font-size:11px;opacity:.8}.hero h1{font-size:clamp(32px,6vw,55px);line-height:1.07;letter-spacing:-1.5px;max-width:760px;margin:16px 0}.hero p{max-width:720px;line-height:1.7;color:#e2e4ff}
h2{letter-spacing:-.5px}.head{display:flex;justify-content:space-between;align-items:end;gap:12px;margin:30px 0 14px}.head h2{font-size:24px;margin:0 0 4px}.categories{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.cat{border:1px solid var(--line);background:white;border-radius:16px;padding:17px;text-align:left;cursor:pointer;color:var(--ink);font:inherit;text-decoration:none;display:block}.cat.active,.cat:hover{border-color:#a99aff;box-shadow:0 7px 22px #4934a414}.emoji{font-size:25px}.cat strong{display:block;margin:8px 0 4px}.cat small{color:var(--muted)}
.toolbar{display:flex;gap:9px;flex-wrap:wrap;margin:16px 0}input,select,textarea{font:inherit;border:1px solid var(--line);border-radius:12px;padding:12px;background:white;color:var(--ink);min-width:0;width:100%}.toolbar input{flex:2;min-width:180px}.toolbar select{flex:1;min-width:150px}.btn{border:0;border-radius:11px;padding:11px 15px;background:var(--purple);color:white;font-weight:800;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:5px}.btn.secondary{background:#f0edff;color:#4b36b6}.btn.white{background:white;color:#38268d}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.card,.panel{background:white;border:1px solid var(--line);border-radius:17px;padding:18px;box-shadow:0 5px 18px #1b2b4d05}.card{display:flex;flex-direction:column;min-height:250px}.pill{display:inline-flex;align-self:flex-start;padding:5px 9px;border-radius:99px;background:#f0edff;color:#5139c4;font-size:11px;font-weight:800}.card h3{font-size:18px;line-height:1.3;margin:13px 0 6px}.org{font-size:12px;color:var(--muted)}.meta{margin:13px 0;display:grid;gap:7px;font-size:12px;color:#46516d}.bottom{margin-top:auto;display:flex;gap:8px;flex-wrap:wrap}.empty{background:white;border:1px dashed #cdd4e5;padding:30px;border-radius:17px;color:var(--muted);text-align:center;grid-column:1/-1}
form.stack{display:grid;gap:12px}.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}.checkgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.check{display:flex;gap:8px;align-items:center;background:#f7f8fd;border-radius:10px;padding:10px;font-size:13px}.check input{width:auto}.flash{padding:12px 15px;border-radius:12px;margin:12px 0;background:#e9e5ff;color:#35267f}.flash.error{background:#fff0ed;color:#96331e}.note{font-size:12px;color:var(--muted);line-height:1.6;margin-top:18px}footer{border-top:1px solid var(--line);padding:22px 15px;text-align:center;color:var(--muted);font-size:12px}
@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.categories{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){main{padding:14px 12px
40px}.nav{padding:12px}.hero{border-radius:20px}.grid,.categories,.two{grid-template-columns:1fr}.head{align-items:start;flex-direction:column}.toolbar input,.toolbar select{width:100%}}
</style></head><body><header><div class="nav"><a class="logo" href="{{ url_for('home') }}">🚀 Nexora<span> 0.2</span></a><nav><a href="{{ url_for('home') }}">Discover</a><a href="{{ url_for('eligibility') }}">Eligibility match</a><a href="{{ url_for('newsletter') }}">Newsletter</a><a href="{{ url_for('mentorship') }}">Mentorship</a>{% if session.get('user_id') %}<a href="{{ url_for('profile') }}">My profile</a><a href="{{ url_for('logout') }}">Log out</a>{% else %}<a href="{{ url_for('login') }}">Log in</a><a href="{{ url_for('signup') }}">Create account</a>{% endif %}</nav></div></header>
<main>{% with messages=get_flashed_messages(with_categories=true) %}{% for kind,message in messages %}<div class="flash {{ 'error' if kind=='error' else '' }}">{{ message }}</div>{% endfor %}{% endwith %}{{ content|safe }}</main><footer>© Nexora 0.2 · Discover. Learn. Build. Apply through official sources.</footer></body></html>
"""

HOME = r"""
<section class="hero"><div class="eyebrow">Your next step starts here</div><h1>Discover Your Next Opportunity.</h1><p>Find scholarships, competitions, hackathons, research programs, internships and Olympiads. Filter by your interests, then apply through the official organizer.</p><form action="{{ url_for('home') }}" class="toolbar"><input name="q" value="{{ q }}" placeholder="Search AI, business, science, country, age..." aria-label="Search"><button class="btn white">Search opportunities →</button></form></section>
<div class="head"><div><h2>Explore categories</h2><div class="muted">Choose a category to filter the real-world opportunity directory.</div></div><span class="muted">{{ items|length }} listings</span></div>
div class="categories"><a class="cat {{ 'active' if not category else '' }}" href="{{ url_for('home',q=q) }}"><span class="emoji">✨</span><strong>All opportunities</strong><small>Browse everything</small></a>{% for name,(emoji,desc) in categories.items() %}<a class="cat {{ 'active' if category==name else '' }}" href="{{ url_for('home',category=name,q=q) }}"><span class="emoji">{{ emoji }}</span><strong>{{ name }}</strong><small>{{ desc }}</small></a>{% endfor %}</div>
<div class="head"><div><h2>{{ category or 'All opportunities' }}</h2><div class="muted">Dates, fees and eligibility can change. Verify them on the official page.</div></div></div>
<form class="toolbar"><input type="hidden" name="category" value="{{ category }}"><input name="q" value="{{ q }}" placeholder="Search title, country, skill or eligibility"><select name="interest"><option value="">All interests</option>{% for interest in interests %}<option {{ 'selected' if chosen_interest==interest else '' }}>{{ interest }}</option>{% endfor %}</select><select name="sort"><option value="title" {{ 'selected' if sort=='title' else '' }}>Sort: A–Z</option><option value="category" {{ 'selected' if sort=='category' else '' }}>Sort: Category</option></select><button class="btn">Apply filters</button></form>
<div class="grid">{% for o in items %}<article class="card"><span class="pill">{{ o.category }}</span><h3>{{ o.title }}</h3><div class="org">{{ o.organization }} · {{ o.location }}</div><div class="meta"><div>🎯 {{ o.level }}</div><div>💰 {{ o.funding }}</div><div>📅 {{ o.deadline }}</div><div>ℹ️ {{ o.status }}</div></div><div class="bottom"><a class="btn secondary" href="{{ url_for('opportunity',item_id=o.id) }}">View details</a><a class="btn" href="{{ o.official_url }}" target="_blank" rel="noopener noreferrer">Official page ↗</a></div></article>{% else %}<div class="empty">No matches found. Try another keyword or category.</div>{% endfor %}</div>
<p class="note">Nexora is an independent discovery directory and is not affiliated with listed organizations. A listing does not guarantee eligibility, selection, funding or that applications are open. Never pay a third party claiming to guarantee selection.</p>
"""
DETAIL = r"""<div class="panel"><a href="{{ url_for('home') }}" class="muted">← Back to opportunities</a><span class="pill">{{ o.category }}</span><h1>{{ o.title }}</h1><div class="org">{{ o.organization }}</div>{% for label,value in [('Location',o.location),('Category',o.category),('Level',o.level),('Funding / benefits',o.funding),('Deadline / cycle',o.deadline),('Status',o.status),('Eligibility',o.eligibility),('Interests',o.interests|join(', '))] %}<p><b>{{ label }}</b><br>{{ value }}</p>{% endfor %}<a class="btn" href="{{ o.official_url }}" target="_blank" rel="noopener noreferrer">Open official organizer page ↗</a><p class="note">Always confirm eligibility and deadlines with the organizer.</p></div>"""
SIGNUP = r"""<div class="panel"><h1>Create your Nexora account</h1><p class="muted">Save your interests and get better opportunity matches.</p><form class="stack" method="post"><label>Your name<input name="name" required maxlength="80"></label><label>Email address<input name="email" type="email" required></label><label>Password (at least 8 characters)<input name="password" type="password" minlength="8" required></label><div class="two"><label>Country<input name="country" value="Bangladesh"></label><label>Age<input name="age" type="number" min="1" max="100" required></label></div><label>Current education level<select name="education"><option>High school student</option><option>Undergraduate</option><option>Graduate</option><option>Other</option></select></label><div><b>Interests</b><div class="checkgrid">{% for i in interests %}<label class="check"><input type="checkbox" name="interests" value="{{ i }}">{{ i }}</label>{% endfor %}</div></div><label>Newsletter frequency<select name="newsletter"><option value="weekly">Weekly</option><option value="daily">Daily (requires scheduled email setup)</option><option value="off">No newsletter</option></select></label><button class="btn">Create account</button></form><p class="muted">Already have an account? <a href="{{ url_for('login') }}">Log in</a></p></div>"""
LOGIN = r"""<div class="panel"><h1>Log in</h1><form class="stack" method="post"><label>Email<input name="email" type="email" required></label><label>Password<input name="password" type="password" required></label><button class="btn">Log in</button></form><p class="muted">New to Nexora? <a href="{{ url_for('signup') }}">Create an account</a></p></div>"""
ELIGIBILITY = r"""<div class="panel"><h1>Find opportunities that may fit you</h1><p class="muted">This is a practical first-pass match, not an official eligibility decision. Always check the organizer's rules.</p><form class="stack" method="post"><div class="two"><label>Age<input name="age" type="number" min="1" max="100" value="{{ age }}" required></label><label>Country<input name="country" value="{{ country or 'Bangladesh' }}" required></label></div><label>Education level<select name="education">{% for e in ['High school student','Undergraduate','Graduate','Other'] %}<option {{ 'selected' if education==e else '' }}>{{ e }}</option>{% endfor %}</select></label><label>Which types do you want? <div class="checkgrid">{% for c in categories %}<label class="check"><input type="checkbox" name="categories" value="{{ c }}" {{ 'checked' if c in chosen_categories else '' }}>{{ c }}</label>{% endfor %}</div></label><label>What are you interested in? <div class="checkgrid">{% for i in interests %}<label class="check"><input type="checkbox" name="interests" value="{{ i }}" {{ 'checked' if i in chosen_interests else '' }}>{{ i }}</label>{% endfor %}</div></label><button class="btn">Find my matches</button></form></div>{% if results is not none %}<div class="head"><div><h2>Possible matches: {{ results|length }}</h2><div class="muted">Matches are based on your choices and listing notes—not a guarantee of eligibility.</div></div></div><div class="grid">{% for o in results %}<article class="card"><span class="pill">{{ o.category }}</span><h3>{{ o.title }}</h3><div class="org">{{ o.organization }}</div><div class="meta"><div>🎯 {{ o.level }}</div><div>📅 {{ o.deadline }}</div><div>Why shown: {{ o.match_reason }}</div></div><div class="bottom"><a class="btn secondary" href="{{ url_for('opportunity',item_id=o.id) }}">View details</a><a class="btn" href="{{ o.official_url }}" target="_blank">Official page ↗</a></div></article>{% else %}<div class="empty">No likely matches with those filters. Try choosing more categories or interests.</div>{% endfor %}</div>{% endif %}"""
NEWSLETTER = r"""<div class = "panel"><h1>Nexora newsletter</h1><p>Get new opportunities and important directory updates by email.</p><p class="muted">Email delivery becomes active after SMTP settings are configured. We don't promise daily delivery until a scheduled job is configured.</p><form class="stack" method="post"><label>Email address<input name="email" type="email" required></label><label>Frequency<select name="frequency"><option value="weekly">Weekly</option><option value="daily">Daily</option></select></label><button class="btn">Subscribe</button></form></div>"""
PROFILE = r"""<div class="panel"><h1>Hello, {{ user.name }} 👋</h1><p>{{ user.email }} · {{ user.country }} · {{ user.education }}</p><p><b>Your interests:</b> {{ user.interests or 'Not selected' }}</p><p><b>Newsletter:</b> {{ user.newsletter }}</p><a class="btn" href="{{ url_for('eligibility') }}">Find my opportunities</a></div>"""
ADMIN = r"""<div class="panel"><h1>Add an opportunity</h1><p class="muted">This form saves listings to the database, so you don't need to replace app.py for each new competition. Keep your admin key private.</p><form class="stack" method="post"><input type="hidden" name="key" value="{{ key }}"><label>Opportunity title<input name="title" required></label><label>Organizer<input name="organization" required></label><label>Category<select name="category">{% for c in categories %}<option>{{ c }}</option>{% endfor %}</select></label><div class="two"><label>Location<input name="location" value="Online / global"></label><label>Level / age / grade<input name="level" required></label></div><label>Funding / benefits<input name="funding" value="See official page"></label><label>Deadline / cycle<input name="deadline" value="Check official page"></label><label>Eligibility notes<textarea name="eligibility" rows="3" required></textarea></label><label>Official URL<input name="official_url" type="url" placeholder="https://..." required></label><div class="checkgrid">{% for i in interests %}<label class="check"><input type="checkbox" name="interests" value="{{ i }}">{{ i }}</label>{% endfor %}</div><button class="btn">Save opportunity</button></form></div>"""
MENTORSHIP = r"""<section class="hero"><div class="eyebrow">Peer guidance</div><h1>Mentorship at Nexora</h1><p>Connect with college students for guidance on academics, applications, research, technology and career exploration. Mentors are student peers, not official admissions representatives.</p><p><b>Proposed fee: $5 from the student and $5 from the mentor per confirmed mentorship booking.</b></p><p class="muted" style="color:#eee">Payments are not active yet. A payment provider and refund/verification policies must be configured before anyone is charged.</p><a class="btn white" href="{{ url_for('mentor_apply') }}">Apply to become a mentor</a></section>
<div class="head"><div><h2>Student mentors</h2><div class="muted">Only approved mentor profiles appear here.</div></div></div><div class="grid">{% for m in mentors %}<article class="card"><span class="pill">{{ m.status }}</span><h3>{{ m.name }}</h3><div class="org">{{ m.university }} · {{ m.study_level }}</div><div class="meta"><div><b>Expertise:</b> {{ m.expertise }}</div><div>{{ m.bio }}</div></div><div class="bottom"><a class="btn" href="{{ url_for('mentor_request',mentor_id=m.user_id) }}">Request mentorship</a></div></article>{% else %}<div class="empty">No mentors have been approved yet. College students can apply to join the mentor community.</div>{% endfor %}</div><p class="note">Mentor applications are reviewed before profiles become public. Never share passwords, sensitive documents, or pay anyone who promises guaranteed admission, scholarships, or selection.</p>"""
MENTOR_APPLY = r"""<div class="panel"><h1>Apply to become a Nexora mentor</h1><p class="muted">For college/university students who want to support younger learners. Applications are reviewed before profiles go public.</p><p><b>Mentor platform fee:</b> $5 per confirmed booking (proposed; not charged until payment setup is active).</p><form class="stack" method="post"><label>College / university<input name="university" required maxlength="160"></label><label>Study level and year<input name="study_level" placeholder="e.g. Undergraduate, 2nd year" required maxlength="100"></label><label>Areas you can help with<input name="expertise" placeholder="e.g. CS, scholarships, study skills" required maxlength="200"></label><label>Short introduction and relevant experience<textarea name="bio" rows="5" maxlength="1200" required></textarea></label><button class="btn">Submit mentor application</button></form></div>"""
MENTOR_REQUEST = r"""<div class="panel"><h1>Request mentorship</h1><p class="muted">Requesting does not charge you. Payment is not enabled yet; both parties must see and agree to the fee before a booking is confirmed.</p><div class="meta"><div><b>Mentor:</b> {{ mentor.name }}</div><div><b>College:</b> {{ mentor.university }}</div><div><b>Expertise:</b> {{ mentor.expertise }}</div></div><p><b>Proposed platform fee:</b> $5 for the student and $5 for the mentor per confirmed booking.</p><form class="stack" method="post"><label>What would you like help with?<input name="topic" required maxlength="160" placeholder="e.g. Beginner Python or scholarship planning"></label><label>Message to the mentor<textarea name="message" rows="4" required maxlength="1200"></textarea></label><button class="btn">Send mentorship request</button></form></div>"""

def page(content, title=None, **context):
    values={"categories": CATEGORIES, "interests": INTERESTS}
    values.update(context)
    inner=render_template_string(content, **values)
    return render_template_string(BASE, content=inner, title=title)

@app.route("/")
def home():
    q=request.args.get("q","").strip().lower()
    category=request.args.get("category","")
    chosen_interest=request.args.get("interest","")
    sort=request.args.get("sort","title")
    rows=all_items()
    if category in CATEGORIES: rows=[o for o in rows if o["category"]==category]
    if q: rows=[o for o in rows if q in " ".join(str(o.get(k,"")) for k in ("title","organization","location","level","funding","deadline","eligibility","category","interests")).lower()]
    if chosen_interest: rows=[o for o in rows if chosen_interest in o["interests"]]
    rows.sort(key=(lambda o:(o["category"],o["title"].lower())) if sort=="category" else (lambda o:o["title"].lower()))
    return page(HOME, items=rows, q=request.args.get("q",""), category=category, sort=sort, chosen_interest=chosen_interest)
    @app.route("/opportunity/<int:item_id>")
def opportunity(item_id):
def opportunity(item_id):
    o=next((x for x in all_items() if int(x["id"])==item_id),None)
    if not o: return redirect(url_for("home"))



    
    return page(DETAIL, title=o["title"], o=o)

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name","").strip()
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        age=request.form.get("age","0")
        interests=request.form.getlist("interests")
        newsletter=request.form.get("newsletter","weekly")
        try: age=int(age)
        except ValueError: age=0
        if len(password)<8:
            flash("Please use a password with at least 8 characters.","error")
        else:
            try:
                with db() as con:
                    con.execute("INSERT INTO users(name,email,password_hash,country,education,age,interests,newsletter) VALUES(?,?,?,?,?,?,?,?)",
                        (name,email,generate_password_hash(password),request.form.get("country",""),request.form.get("education","High school student"),age,", ".join(interests),newsletter))
                    if newsletter!="off":
                        con.execute("INSERT OR IGNORE INTO subscribers(email,frequency) VALUES(?,?)",(email,newsletter))
                flash("Account created. You can now log in.","info")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("An account with that email already exists. Please log in.","error")
    return page(SIGNUP, title="Create account", interests=INTERESTS)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email","").strip().lower()
        with db() as con: user=con.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
        if user and check_password_hash(user["password_hash"],request.form.get("password","")):
            session.clear(); session["user_id"]=user["id"]
            flash("You are logged in.","info")
            return redirect(url_for("profile"))
        flash("Email or password is incorrect.","error")
    return page(LOGIN, title="Log in")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out.","info")
    return redirect(url_for("home"))

@app.route("/profile")
@login_required
def profile():
    with db() as con: user=con.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()
    return page(PROFILE, title="My profile", user=user)

@app.route("/eligibility", methods=["GET","POST"])
def eligibility():
    results=None
    age=18; country="Bangladesh"; education="High school student"
    chosen_categories=[]; chosen_interests=[]
    if request.method=="POST":
        try: age=int(request.form.get("age","18"))
        except ValueError: age=18
        country=request.form.get("country","Bangladesh").strip()
        education=request.form.get("education","High school student")
        chosen_categories=request.form.getlist("categories")
        chosen_interests=request.form.getlist("interests")
        results=[]
        for o in all_items():
            if chosen_categories and o["category"] not in chosen_categories: continue
            interest_overlap=set(chosen_interests).intersection(o["interests"])
            level=(o.get("level") or "").lower()
      #Simple age/education warnings; the official organizer still makes the final decision.
            if age<13 and any(w in level for w in ["undergraduate","university","graduate"]): continue
            if education=="High school student" and any(w in level for w in ["graduate student","postgraduate only"]): continue
            reason=[]
            if interest_overlap: reason.append("matches your interests")
            if country.lower() in (o.get("eligibility") or "").lower() or "international" in (o.get("eligibility") or "").lower() or "worldwide" in (o.get("eligibility") or "").lower(): reason.append("listing mentions international/country access")
            if not reason: reason.append("matches your selected category; check age and country rules")
            o["match_reason"]="; ".join(reason)
            if not chosen_interests or interest_overlap or len(chosen_categories)>0:
                results.append(o)
        results=results[:60]
    return page(ELIGIBILITY, title="Eligibility match", results=results, age=age, country=country, education=education, chosen_categories=chosen_categories, chosen_interests=chosen_interests)

@app.route("/newsletter", methods=["GET","POST"])
def newsletter():
    if request.method=="POST":
        email=request.form.get("email","").strip().lower()
        frequency=request.form.get("frequency","weekly")
        with db() as con: con.execute("INSERT INTO subscribers(email,frequency) VALUES(?,?) ON CONFLICT(email) DO UPDATE SET frequency=excluded.frequency",(email,frequency))
        flash("You're subscribed. Email delivery activates once the site owner configures email sending.","info")
        return redirect(url_for("newsletter"))
    return page(NEWSLETTER, title="Newsletter")
            @app.route("/admin", methods=["GET","POST"])
def admin():
    admin_key=os.environ.get("NEXORA_ADMIN_KEY")
    supplied=request.values.get("key","")
    if not admin_key or supplied!=admin_key:
        return "Admin access is not configured or the key is incorrect. Set NEXORA_ADMIN_KEY in your hosting environment.",403
    if request.method=="POST":
        title=request.form.get("title","").strip()
        url=request.form.get("official_url","").strip()
        if not url.startswith("https://") and not url.startswith("http://"):
            flash("Please enter a valid official URL.","error")
        else:
            selected=[x for x in request.form.getlist("interests") if x in INTERESTS]
            new={"title":title,"organization":request.form.get("organization","").strip(),"category":request.form.get("category","Competitions"),"location":request.form.get("location","Online / global"),"level":request.form.get("level",""),"funding":request.form.get("funding","See official page"),"deadline":request.form.get("deadline","Check official page"),"status":"Check official page","eligibility":request.form.get("eligibility",""),"official_url":url,"interests":selected or ["General"]}
            with db() as con:
                con.execute("""INSERT INTO opportunities(title,organization,category,location,level,funding,deadline,status,eligibility,official_url,interests)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)""",(new["title"],new["organization"],new["category"],new["location"],new["level"],new["funding"],new["deadline"],new["status"],new["eligibility"],new["official_url"],json.dumps(new["interests"])))
            notify_new_listing(new)
            flash("Opportunity saved. You did not need to replace app.py.","info")
            return redirect(url_for("admin",key=admin_key))
    return page(ADMIN, title="Add opportunity", key=admin_key)
@app.route("/mentorship")
def mentorship():
    with db() as con:
        mentors=con.execute("""SELECT ma.user_id, u.name, ma.university, ma.study_level,
            ma.expertise, ma.bio, ma.status FROM mentor_applications ma
            JOIN users u ON u.id=ma.user_id WHERE ma.status='Approved' ORDER BY ma.created_at DESC""").fetchall()
    return page(MENTORSHIP, title="Mentorship", mentors=mentors)

@app.route("/mentor/apply", methods=["GET", "POST"])
@login_required
def mentor_apply():
    if request.method == "POST":
        university=request.form.get("university", "").strip()
        study_level=request.form.get("study_level", "").strip()
        expertise=request.form.get("expertise", "").strip()
        bio=request.form.get("bio", "").strip()
        if not all([university, study_level, expertise, bio]):
            flash("Please complete every field.", "error")
        else:
            try:
                with db() as con:
                    con.execute("""INSERT INTO mentor_applications(user_id,university,study_level,expertise,bio)
                        VALUES(?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET university=excluded.university,
                        study_level=excluded.study_level, expertise=excluded.expertise, bio=excluded.bio,
                        status='Pending review'""", (session["user_id"], university, study_level, expertise, bio))
                flash("Your mentor application was submitted for review. It is not public yet.", "info")
                return redirect(url_for("mentorship"))
            except sqlite3.Error:
                flash("We couldn't save the application. Please try again.", "error")
    return page(MENTOR_APPLY, title="Become a mentor")

@app.route("/mentorship/request/<int:mentor_id>", methods=["GET", "POST"])
@login_required
def mentor_request(mentor_id):
    with db() as con:
        mentor=con.execute("""SELECT ma.user_id, u.name, ma.university, ma.expertise
            FROM mentor_applications ma JOIN users u ON u.id=ma.user_id
            WHERE ma.user_id=? AND ma.status='Approved'""", (mentor_id,)).fetchone()
    if not mentor:
        flash("That mentor profile is not available.", "error")
        return redirect(url_for("mentorship"))
    if int(mentor_id) == int(session["user_id"]):
        flash("You cannot request mentorship from your own account.", "error")
        return redirect(url_for("mentorship"))
    if request.method == "POST":
        topic=request.form.get("topic", "").strip()
        message=request.form.get("message", "").strip()
        if not topic or not message:
            flash("Please add a topic and message.", "error")
        else:
            with db() as con:
                con.execute("INSERT INTO mentorship_requests(student_id,mentor_id,topic,message) VALUES(?,?,?,?)",
                    (session["user_id"], mentor_id, topic, message))
            flash("Request sent. No payment was taken; payment processing is not configured yet.", "info")
            return redirect(url_for("mentorship"))
    return page(MENTOR_REQUEST, title="Request mentorship", mentor=mentor)

@app.route("/health")
def health():
    return {"status":"ok","opportunities":len(all_items())}

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","5000")),debug=False)
                                           

        
