from flask import Flask, render_template_string
import json

app = Flask(__name__)

# Real program pages. Dates and eligibility change; confirm on the official site.
# Format: title, organization, category, location, level, funding/benefit, cycle/status, eligibility note, official URL
DATA = [
# 20 SCHOLARSHIPS
("KAIST International Undergraduate Scholarship","KAIST","Scholarship","South Korea","Undergraduate","Full tuition + monthly allowance + insurance","Check current admissions cycle","International undergraduate applicants; scholarship considered with admission","https://admission.kaist.ac.kr/intl-undergraduate/support/scholarships/kaist"),
("MEXT Undergraduate Scholarship","Government of Japan","Scholarship","Japan","Undergraduate","Government-funded; terms vary by track","Check Japanese Embassy page","International students; apply through the current country-specific route","https://www.studyinjapan.go.jp/en/planning/scholarships/mext-scholarships/"),
("Global Korea Scholarship (GKS-U)","Government of Korea","Scholarship","South Korea","Undergraduate","Tuition, airfare, language training and allowance per official terms","2027 notice published; verify current route","International applicants; check the current guidelines and Bangladesh notices","https://www.studyinkorea.go.kr/"),
("Türkiye Scholarships","Government of Türkiye","Scholarship","Türkiye","Undergraduate / Graduate","Tuition, stipend, accommodation, insurance and travel per program","Usually Jan–Feb; check next cycle","International applicants meeting program age and academic criteria","https://www.turkiyeburslari.gov.tr/"),
("Stipendium Hungaricum","Government of Hungary","Scholarship","Hungary","Undergraduate / Graduate","Tuition support and other benefits per call","Check next call","Eligibility depends on sending-partner country and current call","https://stipendiumhungaricum.hu/apply/"),
("Reach Oxford Scholarship","University of Oxford","Scholarship","United Kingdom","Undergraduate","Course fees, living costs and one return airfare for eligible students","Check official cycle","For eligible students from low-income countries; very limited awards","https://www.ox.ac.uk/admissions/undergraduate/fees-and-funding/oxford-support/reach-oxford-scholarship"),
("Cambridge Trust Scholarships","Cambridge Trust","Scholarship","United Kingdom","Undergraduate / Graduate","Varies by award","Check official page","Eligibility and funding vary; undergraduate awards are limited","https://www.cambridgetrust.org/scholarships/"),
("MIT Undergraduate Financial Aid","Massachusetts Institute of Technology","Scholarship","United States","Undergraduate","Need-based aid; international students eligible","Apply with admission/aid materials","Not a separate merit scholarship; review MIT's current aid instructions","https://sfs.mit.edu/undergraduate-students/financial-aid/"),
("Harvard College Financial Aid","Harvard University","Scholarship","United States","Undergraduate","Need-based financial aid","Apply with admission/aid materials","International applicants may apply for need-based aid","https://college.harvard.edu/financial-aid"),
("Princeton Undergraduate Financial Aid","Princeton University","Scholarship","United States","Undergraduate","Need-based aid","Apply with admission/aid materials","International applicants may apply; admission is highly selective","https://admission.princeton.edu/cost-aid"),
("Yale Undergraduate Financial Aid","Yale University","Scholarship","United States","Undergraduate","Need-based aid","Apply with admission/aid materials","International applicants may apply for need-based aid","https://admissions.yale.edu/financial-aid"),
("Amherst College Financial Aid","Amherst College","Scholarship","United States","Undergraduate","Need-based aid","Check official page","International students can apply for financial aid","https://www.amherst.edu/admission/financial_aid"),
("Bowdoin College Financial Aid","Bowdoin College","Scholarship","United States","Undergraduate","Need-based aid","Check official page","Review current international applicant and aid policies","https://www.bowdoin.edu/admissions/tuition-aid/"),
("Lester B. Pearson International Scholarship","University of Toronto","Scholarship","Canada","Undergraduate","Tuition, books, incidental fees and residence support per award","Check current cycle","International high-school students; school nomination required","https://future.utoronto.ca/pearson/about/"),
("Global Futures Scholarships","University of Manchester","Scholarship","United Kingdom","Undergraduate / Master's","Partial merit awards; amount varies","2027 entry page available; check country deadline","Bangladesh is listed among eligible countries; course offer required","https://www.manchester.ac.uk/study/international/finance-and-scholarships/funding/global-futures-scholarship/"),
("Vice-Chancellor's International Scholarship","Newcastle University","Scholarship","United Kingdom","Undergraduate","£7,000 per academic year (2027 entry page)","Awards considered through the cycle","Bangladesh is among eligible domiciles; course/offer rules apply","https://www.ncl.ac.uk/undergraduate/fees-funding/scholarships-bursaries/vc-international/"),
("Undergraduate International Excellence Scholarship","Cardiff University","Scholarship","United Kingdom","Undergraduate","£10,000 tuition discount (2027 entry)","2 April 2027 listed; verify official page","Eligible international students holding an offer; conditions apply","https://www.cardiff.ac.uk/study/international/funding-and-fees/international-scholarships/undergraduate-excellence-scholarships"),
("Vice-Chancellor's Undergraduate International Scholarship","Cardiff University","Scholarship","United Kingdom","Undergraduate","£3,500–£5,000 tuition discount (2027 entry)","30 June 2027 listed; verify official page","Eligible overseas-fee students; country/course rules apply","https://www.cardiff.ac.uk/study/international/funding-and-fees/international-scholarships/vice-chancellors-international-scholarship-ug"),
("South Asia Scholarship","London Metropolitan University","Scholarship","United Kingdom","Undergraduate / Master's","Tuition discount; terms vary","Check current entry cycle","Bangladesh and other South Asian citizenships; deposit and course conditions apply","https://www.londonmet.ac.uk/applying/funding-your-studies/scholarships/south-asia-scholarships/"),
("Egyptian Government / Al-Azhar Scholarships","Bangladesh Ministry of Education","Scholarship","Egypt","Undergraduate / Islamic studies","Varies by official notice","Check latest Bangladesh ministry notice","Bangladeshi applicants; eligibility depends on the current official notice","https://shed.gov.bd/pages/moedu-scholarships/"),

# 20 COMPETITIONS
("Conrad Challenge","Conrad Foundation / U.S. Space & Rocket Center","Competition","Global","High-school teams","Prizes and recognition vary by track","2026–27 Activation Stage ends 30 Oct 2026","International student teams; check team, fee and submission rules","https://conrad.spacecenter.org/"),
("Technovation Challenge","Technovation","Competition","Global / virtual","Ages 8–18","Awards and global recognition","2026–27 season starts October 2026; verify registration","Free competition and curriculum; age and team rules apply","https://technovationchallenge.org/competition/"),
("GENIUS Olympiad","Terra Science and Education","Competition","Global","Grades 8–12","Awards; some scholarship/publication opportunities","Check 2027 registration and country route","High-school projects in environment-related fields","https://geniusolympiad.org/"),
("DSH Hacks V2 — AI × Healthcare","NXT Horizon / STEMise","Competition","Online / global","Student builders","In-kind prizes listed by organizer","Listed closing date 24 Oct 2026; verify event page","Student builders worldwide; read official rules","https://nxthorizon.org/competitions"),
("Neighborhood Hacks 2026","Neighborhood Hacks","Competition","Virtual / global","High school students","Organizer lists prizes","16–24 Oct 2026 listed","High-school students worldwide; verify registration and team rules","https://neighborhoodhacks.org/"),
("World Challenger — Global IT, IoT & AI Challenge","World Challenger","Competition","Online / global","Grades 5–12 school teams","Awards vary","Check next official cycle","School teams worldwide; school participation rules apply","https://www.worldchallenger.org/"),
("International Computer Science Competition","ICSC","Competition","Global / online","Middle school, high school and university","Certificates/awards vary","2026 concluded; watch next edition","All countries; age division and computer access required","https://icscompetition.org/en/"),
("International Software Engineering Olympiad","ISWEO","Competition","Online / global","Grades 9–12 or recent graduates","Awards vary","Check next cycle; 2026 qualifier has passed","Organizer lists worldwide eligibility for grades 9–12/recent graduates, age 21 or younger","https://www.isweo.org/"),
("LBX Global Innovation Competition","LBX","Competition","Global","Middle and high school","Regional/global showcases","Check 2026 season details","Check age, team, guardian and travel rules","https://www.lbx.org/"),
("Sigma Olympics","Sigma Olympics","Competition","Global","School students","Medals/certificates per organizer","2026–27 registration Sep–Jan; verify country representative","Country representative and grade rules determine eligibility","https://sigmaolympics.com/"),
("STEMCo","STEMCo","Competition","International","School students","Awards vary","Science rounds Dec 2026 / Jan 2027 listed; verify registration","Maths, science and English divisions; travel/fees may apply","https://stemco.org/"),
("XPERTSTEM International STEM Competition","XPERTSTEM","Competition","International","Grades 3–12","Awards vary","2026–27 calendar on official site","Grade and event rules; in-person finals may require travel","https://xpertstem.org/"),
("Breakthrough Junior Challenge","Breakthrough Prize Foundation","Competition","Global","Ages 13–18","Scholarship and prizes","Check next official cycle","Science explanation video; confirm current age and submission rules","https://breakthroughjuniorchallenge.org/"),
("Diamond Challenge","University of Delaware Horn Entrepreneurship","Competition","Global","High-school entrepreneurs","Cash prizes/awards vary","Check 2026–27 cycle","High-school teams; track and team rules apply","https://diamondchallenge.org/"),
("Blue Ocean Student Entrepreneur Competition","Blue Ocean Entrepreneurship","Competition","Global","High school students","Cash prizes and recognition","Check next cycle","High-school students; pitch/video format","https://blueoceancompetition.org/"),
("Congressional App Challenge","U.S. House of Representatives","Competition","United States","Middle/high school","Recognition varies by district","Annual; check district deadline","Only eligible students in participating U.S. congressional districts","https://www.congressionalappchallenge.us/"),
("Regeneron International Science and Engineering Fair","Society for Science","Competition","International","Grades 9–12","Awards vary","2027 fair dates listed; qualification required","Must qualify through an affiliated fair; local rules apply","https://www.societyforscience.org/isef/"),
("Regeneron Science Talent Search","Society for Science","Competition","United States","High-school seniors","Major research awards","2026 cycle deadline listed as 5 Nov 2026; verify rules","U.S. high-school seniors meeting citizenship/residency requirements; not global direct entry","https://www.societyforscience.org/regeneron-sts/"),
("National High School Big Data & AI Challenge","STEM Fellowship","Competition","Canada / international details vary","High school / CEGEP","Research and conference opportunities","Registration deadline listed as 18 Oct 2026; confirm fees","High school/CEGEP; participation may involve fees and travel","https://www.stemfellowship.org/hsbdc/2026-27"),
("International Astronomy and Astrophysics Competition","IAAC","Competition","International / online","School and university students","Awards and certificates vary","Check current annual cycle","International participants; age and round rules apply","https://iaac.space/"),

# 20 INTERNSHIPS / RESEARCH / LEARNING PROGRAMS
("Google Summer of Code","Google","Internship / Research","Global / remote","18+ contributors","Stipend for accepted contributors","Annual cycle; check official page","Open-source mentored project program, not conventional employment","https://summerofcode.withgoogle.com/"),
("Outreachy Internships","Outreachy","Internship / Research","Remote; eligibility varies","18+","Paid internship stipend","Check next application round","Applicants must meet Outreachy's eligibility rules and round requirements","https://www.outreachy.org/"),
("MLH Fellowship","Major League Hacking","Internship / Research","Remote / cohort-based","Students and recent graduates","Program terms vary by cohort","Check next cohort","Eligibility, payment and time commitment vary by cohort","https://fellowship.mlh.io/"),
("MIT PRIMES","MIT","Internship / Research","United States / some remote research","High school students","Research mentorship","Annual application cycle; check page","Specific geographic, grade and research-readiness requirements","https://math.mit.edu/research/highschool/primes/"),
("MIT Summer Research Program (MSRP)","MIT","Internship / Research","United States","Undergraduates","Research experience; terms vary","Annual; check eligibility","Primarily for eligible undergraduates, not a general high-school internship","https://oge.mit.edu/msrp/"),
("Research Science Institute (RSI)","Center for Excellence in Education / MIT","Internship / Research","United States","High school students","Research program","Annual cycle; check current dates","Highly selective; international eligibility and travel must be checked","https://www.cee.org/programs/research-science-institute"),
("Simons Summer Research Program","Stony Brook University","Internship / Research","United States","High school juniors","Research experience","Annual cycle; check page","Restrictions may include residency, grade and application requirements","https://www.stonybrook.edu/simons/"),
("Stanford SIMR","Stanford University","Internship / Research","United States","High school students","Research program","Annual cycle; check page","U.S. residency/citizenship and other restrictions may apply","https://simr.stanford.edu/"),
("UCSB Research Mentorship Program","UC Santa Barbara","Internship / Research","United States","High school students","Research mentorship; fees may apply","Annual cycle; check page","Check cost, age, course and visa requirements","https://summer.ucsb.edu/programs/research-mentorship-program"),
("BU RISE Internship / Practicum","Boston University","Internship / Research","United States","High school students","Research experience; cost/aid vary","Annual cycle; check page","Eligibility, fees and international participation rules apply","https://www.bu.edu/summer/high-school-programs/research-internship/"),
("Anson L. Clark Scholars Program","Texas Tech University","Internship / Research","United States","High school juniors/seniors","Research program; stipend terms on official page","Annual cycle; check page","Highly selective; check age, grade, citizenship and travel requirements","https://www.depts.ttu.edu/honors/academicsandenrichment/affiliatedandhighschool/clarks/"),
("Garcia Summer Research Program","Stony Brook University","Internship / Research","United States","High school students","Research program; tuition may apply","Annual cycle; check page","Check program fees and international eligibility","https://www.stonybrook.edu/commcms/garcia/"),
("SHTEM Summer Internship Program","Stanford University","Internship / Research","United States / details vary","High school students","Research experience","Annual cycle; check page","Eligibility and project availability vary","https://compression.stanford.edu/shtem-summer-internships"),
("AI4ALL Open Learning","AI4ALL","Internship / Research","Online","High school learners","Free learning resources","Self-paced; check official page","Educational program, not necessarily a paid internship","https://ai-4-all.org/open-learning/"),
("NASA OSTEM Internships","NASA","Internship / Research","United States","Students","Paid and unpaid roles vary","Multiple cycles; check each posting","Most positions require U.S. citizenship; do not assume international eligibility","https://intern.nasa.gov/"),
("CERN Student Opportunities","CERN","Internship / Research","Switzerland / varies","University students","Stipend/benefits vary","Multiple programs; check openings","Many roles require university enrollment and specific nationality/education conditions","https://careers.cern/"),
("UNICEF Internships","UNICEF","Internship / Research","Global / office-specific","Students and recent graduates","Stipend may be provided under program rules","Apply to individual vacancies","Must meet vacancy education, age, language and work-authorization rules","https://www.unicef.org/careers/internships"),
("World Bank Internship Program","World Bank Group","Internship / Research","Global / office-specific","Graduate students primarily","Paid internship","Seasonal windows; check official page","Designed primarily for graduate students; requirements vary by posting","https://www.worldbank.org/en/about/careers/programs-and-internships"),
("Pioneer Academics Research Program","Pioneer Academics","Internship / Research","Online / global","High school students","Mentored research; tuition/aid rules apply","Check current cohort","Selective academic research program, not a paid job; confirm fees and financial aid","https://pioneeracademics.com/"),
("Lumiere Research Scholar Program","Lumiere Education","Internship / Research","Online / global","High school students","Mentored research; tuition/aid rules apply","Check current cohort","Not a paid internship; program fees and financial assistance vary","https://www.lumiere-education.com/"),
]

ITEMS = []
for i, row in enumerate(DATA):
    title, org, category, location, level, funding, cycle, eligibility, url = row
    ITEMS.append({
        "id": f"opportunity-{i+1}", "title": title, "organization": org,
        "category": category, "location": location, "level": level,
        "funding": funding, "deadline": cycle, "eligibility": eligibility,
        "official_url": url,
        "status": "Open / upcoming — verify details" if any(x in cycle.lower() for x in ["2027", "oct 2026", "october 2026", "registration announced", "dec 2026", "jan 2027"]) else "Check official page"
    })

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nexora 0.2 — Discover Your Next Opportunity</title>
<style>
:root{--ink:#17213c;--muted:#64708b;--bg:#f5f7fc;--purple:#6c4cf1;--line:#e5e9f3}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif}
header{position:sticky;top:0;z-index:5;background:#ffffffed;border-bottom:1px solid var(--line)}.nav{max-width:1160px;margin:auto;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;gap:10px}.logo{font-weight:900;font-size:22px;color:var(--purple)}.logo span{color:var(--ink)}.muted{color:var(--muted);font-size:13px;line-height:1.5}
main{max-width:1160px;margin:auto;padding:24px 20px 55px}.hero{background:linear-gradient(125deg,#1d2751,#4934a4 62%,#8466ff);border-radius:26px;color:white;padding:clamp(25px,6vw,60px)}
.eyebrow{text-transform:uppercase;font-weight:800;letter-spacing:2px;font-size:11px;opacity:.8}.hero h1{font-size:clamp(32px,6vw,58px);line-height:1.05;letter-spacing:-1.7px;max-width:720px;margin:16px 0}.hero p{max-width:650px;line-height:1.7;color:#e2e4ff}
.search{display:flex;gap:8px;max-width:720px;margin-top:23px}input,select{font:inherit;border:1px solid var(--line);border-radius:12px;padding:13px;background:white;color:var(--ink);min-width:0}.search input{flex:1;border:0}
.btn{border:0;border-radius:11px;padding:11px 15px;background:var(--purple);color:white;font-weight:800;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:5px}.hero .btn{background:white;color:#38268d}
.head{display:flex;justify-content:space-between;align-items:end;gap:12px;margin:32px 0 15px}.head h2{font-size:24px;margin:0;letter-spacing:-.5px}
.categories{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.cat{border:1px solid var(--line);background:white;border-radius:16px;padding:17px;text-align:left;cursor:pointer;color:var(--ink);font:inherit}.cat.active,.cat:hover{border-color:#a99aff;box-shadow:0 7px 22px #4934a414}.cat .emoji{font-size:24px}.cat strong{display:block;margin:8px 0 4px}.cat small{color:var(--muted)}
.toolbar{display:flex;gap:9px;flex-wrap:wrap;margin:16px 0}.toolbar input{flex:1;min-width:180px}.toolbar select{min-width:150px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.card{background:white;border:1px solid var(--line);border-radius:17px;padding:18px;display:flex;flex-direction:column;min-height:260px;box-shadow:0 5px 18px #1b2b4d05}.pill{display:inline-flex;align-self:flex-start;padding:5px 9px;border-radius:99px;background:#f0edff;color:#5139c4;font-size:11px;font-weight:800}.card h3{font-size:18px;line-height:1.3;margin:13px 0 6px}.org{font-size:12px;color:var(--muted)}.meta{margin:13px 0;display:grid;gap:7px;font-size:12px;color:#46516d}.bottom{margin-top:auto;display:flex;gap:8px;flex-wrap:wrap}.btn.secondary{background:#f0edff;color:#4b36b6}.btn.small{font-size:12px;padding:10px 12px}.empty{background:white;border:1px dashed #cdd4e5;padding:30px;border-radius:17px;color:var;padding:30px;border-radius:17px;color:var(--muted);text-align:center;grid-column:1/-1}
footer{border-top:1px solid var(--line);padding:22px 15px;text-align:center;color:var(--muted);font-size:12px}.modalback{display:none;position:fixed;inset:0;background:#111a33a8;z-index:10;padding:18px;overflow:auto}.modal{background:white;border-radius:20px;max-width:650px;margin:5vh auto;padding:24px}.close{float:right;border:0;background:#f0f2f8;border-radius:50%;width:36px;height:36px;font-size:20px;cursor:pointer}.row{padding:12px 0;border-bottom:1px solid var(--line)}.row strong{display:block;font-size:12px;color:var(--muted);margin-bottom:5px}.note{font-size:12px;color:var(--muted);line-height:1.6;margin-top:18px}
@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.categories{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){main{padding:14px 12px 40px}.nav{padding:13px}.hero{border-radius:20px}.search{flex-direction:column}.grid{grid-template-columns:1fr}.head{align-items:start;flex-direction:column}.toolbar input,.toolbar select{width:100%}}
</style></head><body>
<header><div class="nav"><div class="logo">🚀 Nexora<span> 0.2</span></div><small class="muted">Discover your next opportunity</small></div></header>
<main><section class="hero"><div class="eyebrow">Your next step starts here</div><h1>Discover Your Next Opportunity.</h1>
<p>Explore scholarships, competitions, internships and research programs. Read the details, then apply directly through the official organizer.</p>
<div class="search"><input id="heroSearch" placeholder="Search AI, scholarship, coding, research..." aria-label="Search opportunities"><button class="btn" onclick="runSearch()">Search opportunities →</button></div></section>
<div class="head"><div><h2>Explore categories</h2><div class="muted">Choose what you want to discover.</div></div><span class="muted" id="total"></span></div>
<div class="categories">
button class="cat active" data-cat="All" onclick="choose('All')"><span class="emoji">✨</span><strong>All opportunities</strong><small>Browse everything</small></button>
<button class="cat" data-cat="Scholarship" onclick="choose('Scholarship')"><span class="emoji">🎓</span><strong>Scholarships</strong><small>Funding and study</small></button>
<button class="cat" data-cat="Competition" onclick="choose('Competition')"><span class="emoji">🏆</span><strong>Competitions</strong><small>Show your skills</small></button>
<button class="cat" data-cat="Internship / Research" onclick="choose('Internship / Research')"><span class="emoji">🔬</span><strong>Internships & research</strong><small>Build experience</small></button>
</div>
<div class="head"><div><h2 id="listTitle">All opportunities</h2><div class="muted">Confirm dates, fees, and eligibility on the official website.</div></div></div>
<div class="toolbar"><input id="q" placeholder="Search title, country, skill or eligibility..." oninput="render()"><select id="status" onchange="render()"><option value="">All status labels</option><option>Open / upcoming — verify details</option><option>Check official page</option></select><select id="sort" onchange="render()"><option value="title">Sort: A–Z</option><option value="category">Sort: Category</option></select></div>
<div class="grid" id="cards"></div>
<p class="note">Nexora is an independent discovery directory and is not affiliated with listed organizations. A listing does not guarantee eligibility, selection, funding, or that applications are open. Always read the organizer’s rules. Never pay a third party claiming to guarantee selection.</p>
</main><footer>© Nexora 0.2 · Discover. Learn. Build. Apply through official sources.</footer>
<div class="modalback" id="back" onclick="backdrop(event)"><div class="modal"><button class="close" onclick="closeModal()">×</button><div id="details"></div></div></div>
<script>
const opportunities = __DATA__;
let category="All";
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function choose(c){category=c;document.querySelectorAll(".cat").forEach(b=>b.classList.toggle("active",b.dataset.cat===c));document.getElementById("listTitle").textContent=c==="All"?"All opportunities":c==="Internship / Research"?"Internships & research":c+" "s";render();}
function runSearch(){document.getElementById("q").value=document.getElementById("heroSearch").value;render();document.getElementById("cards").scrollIntoView({behavior:"smooth"});}
function render(){
 let q=document.getElementById("q").value.trim().toLowerCase(),s=document.getElementById("status").value;
 let rows=opportunities.filter(o=>(category==="All"||o.category===category)&&(!s||o.status===s)&&(!q||Object.values(o).join(" ").toLowerCase().includes(q)));
 rows.sort((a,b)=>document.getElementById("sort").value==="category"?(a.category+a.title).localeCompare(b.category+b.title):a.title.localeCompare(b.title));
 document.getElementById("total").textContent=opportunities.length+" listings";
 document.getElementById("cards").innerHTML=rows.length?rows.map(o=>`<article class="card"><span class="pill">${esc(o.category)}</span><h3>${esc(o.title)}</h3><div class="org">${esc(o.organization)} · ${esc(o.location)}</div><div class="meta"><div>🎯 ${esc(o.level)}</div><div>💰 ${esc(o.funding)}</div><div>📅 ${esc(o.deadline)}</div><div>ℹ️ ${esc(o.status)}</div></div><div class="bottom"><button class="btn secondary small" onclick="detail('${esc(o.id)}')">View details</button><a class="btn small" href="${esc(o.official_url)}" target="_blank" rel="noopener noreferrer">Official page ↗</a></div></article>`).join(""):'<div class="empty">No matches found. Try another keyword or category.</div>';
}
function detail(id){let o=opportunities.find(x=>x.id===id);if(!o)return;let fields=[["Organization",o.organization],["Category",o.category],["Location",o.location],["Level",o.level],["Funding / benefits",o.funding],["Deadline / cycle",o.deadline],["Status",o.status],["Eligibility notes",o.eligibility]];
document.getElementById("details").innerHTML=`<span class="pill">${esc(o.category)}</span><h2>${esc(o.title)}</h2><div class="org">${esc(o.organization)}</div>${fields.map(([k,v])=>`<div class="row"><strong>${esc(k)}</strong>${esc(v)}</div>`).join("")}<p class="note">These notes are a starting point, not a guarantee of eligibility. Confirm the latest rules and dates on the official page.</p><a class="btn" href="${esc(o.official_url)}" target="_blank" rel="noopener noreferrer">Open official page ↗</a>`;
document.getElementById("back").style.display="block";document.body.style.overflow="hidden";}
function closeModal(){document.getElementById("back").style.display="none";document.body.style.overflow="";}
function backdrop(e){if(e.target.id==="back")closeModal();}
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeModal();});render();
</script></body></html>"""

@app.route("/")
def home():
    return render_template_string(PAGE.replace("__DATA__", json.dumps(ITEMS, ensure_ascii=False)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
