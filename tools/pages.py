"""Page manifest — hand-edited. One entry per URL.

`tools/build.py` reads this to write the canonical / Open Graph / Twitter /
JSON-LD block into each page. Nothing here controls page *content*; it only
describes the page to machines.

Adding a page: add an entry here, run `python3 tools/build.py`.

Fields
  title, desc   — used for <title>, meta description, og:*, twitter:*
  kind          — home | hub | case | post | project | form | util
  crumbs        — [(label, url-path), ...]; the page itself is appended
                  automatically and is not a link
  published /
  modified      — ISO date, posts and cases only
  image         — OG image path, defaults to /og-default.png
  noindex       — keep out of the sitemap and set robots noindex
"""

SITE = "https://www.arshadhossain.com"

# Google Analytics 4 measurement ID. Set to None to strip the tag from
# every page in one run.
GA_ID = "G-9K49EJGCFB"
AUTHOR = "Arshad Hossain"

# The identity statement. One string, used everywhere, so the entity
# resolves to one person across the whole graph.
IDENTITY = (
    "Arshad Hossain is an independent Meta Ads and SEO specialist based in "
    "Dhaka, Bangladesh, working directly with clients in the United States, "
    "Canada and Singapore. Since 2020 he has managed more than $250,000 in "
    "ad spend across 40+ client accounts."
)

SAME_AS = [
    "https://www.linkedin.com/in/arshad-hossain-8a6241130/",
    "https://www.upwork.com/freelancers/~01dafacb23c9b9555f",
]

CASES = "cases/"
BLOG = "blog/"
PROJECTS = "projects/"

PAGES = {
    "index.html": dict(
        kind="home",
        title="Arshad Hossain · Freelance Meta Ads & SEO Specialist",
        desc="Independent Meta Ads and SEO specialist. $250K+ ad spend managed across 40+ accounts. Cost per lead cut by up to 95%, organic traffic grown 4.2x.",
        crumbs=[],
    ),

    # ---- hubs
    "cases/index.html": dict(
        kind="hub",
        title="Case Studies · Real Meta Ads & SEO Results",
        desc="Documented campaigns across Meta Ads, Messenger and SEO. Every number comes from a real client account, with the reporting behind it.",
        crumbs=[("Home", "")],
    ),
    "blog/index.html": dict(
        kind="hub",
        title="Blog · Notes From Live Meta Ads & SEO Accounts",
        desc="Long-form breakdowns of real campaigns: what worked, what didn't, and the numbers behind both. Written from accounts I ran myself.",
        crumbs=[("Home", "")],
    ),
    "projects/index.html": dict(
        kind="hub", noindex=True,
        title="Projects · Tools I Built With AI",
        desc="Side projects built to solve real problems: civic accountability, parenting tools, invoice generation, and an AI prompt library.",
        crumbs=[("Home", "")],
    ),

    # ---- entity anchor
    "about/index.html": dict(
        kind="about",
        title="About Arshad Hossain · Meta Ads & SEO Freelancer",
        desc="Independent Meta Ads and SEO specialist based in Dhaka, Bangladesh, working with clients in the US, Canada and Singapore. $250K+ ad spend managed since 2020.",
        crumbs=[("Home", "")],
    ),

    # ---- services
    "services/index.html": dict(
        kind="hub",
        title="Services · Freelance Meta Ads & SEO",
        desc="Meta Ads, click-to-Messenger campaigns and SEO. How engagements work, what's included, what isn't, and the evidence behind each service.",
        crumbs=[("Home", "")],
    ),
    "services/meta-ads-management/index.html": dict(
        kind="service",
        title="Freelance Facebook & Instagram Ads Manager",
        desc="Freelance Meta Ads management: campaign structure, Conversions API, creative testing and daily optimisation. Documented cost per lead from $86 down to $3.91.",
        crumbs=[("Home", ""), ("Services", "services/")],
        service_name="Meta Ads Management",
        service_type="Facebook and Instagram advertising management",
    ),
    "services/messenger-ads/index.html": dict(
        kind="service",
        title="Click-to-Messenger Ad Campaigns",
        desc="Click-to-Messenger campaign management. Conversations at two to four cents each in conversational-commerce markets, and an honest account of where it does not fit.",
        crumbs=[("Home", ""), ("Services", "services/")],
        service_name="Click-to-Messenger Ads",
        service_type="Conversational advertising campaign management",
    ),
    "services/seo/index.html": dict(
        kind="service",
        title="Freelance SEO Consultant for Small Businesses",
        desc="Independent SEO consultant for small businesses: technical, local and e-commerce SEO, plus the Google Business Profile. Documented zero to Page 1 in three months.",
        crumbs=[("Home", ""), ("Services", "services/")],
        service_name="Freelance SEO Consulting",
        service_type="Search engine optimisation",
    ),

    # ---- benchmarks: first-party data, the AI-citation play
    "benchmarks/index.html": dict(
        kind="hub",
        title="Advertising Benchmarks From Real Client Accounts",
        desc="First-party Meta Ads and SEO figures from accounts I managed directly, each linked to the reporting it came from. Not an aggregate of other surveys.",
        crumbs=[("Home", "")],
    ),
    "benchmarks/facebook-ads-cost-per-lead/index.html": dict(
        kind="dataset",
        title="Facebook Ads Cost Per Lead: 5 Real Client Accounts",
        desc="Observed Meta cost per lead across five accounts I managed from 2023 to 2026, ranging $3.91 to $12.23, with vertical, country, spend and sample size.",
        crumbs=[("Home", ""), ("Benchmarks", "benchmarks/")],
        modified="2026-08-07",
        dataset_name="Facebook Ads cost per lead, 5 client accounts, 2023-2026",
        coverage="2023/2026",
        places=["United States"],
        technique="Meta Ads Manager reporting, account level, USD",
        variables=[
            ("Cost per lead", "3.91", "Hair and scalp clinic, El Paso TX, 35 campaigns, down from $86"),
            ("Cost per lead", "5.08", "B2B access solutions, Nevada, 64 leads, 63% below Meta benchmark"),
            ("Cost per lead", "7.98", "Lending, US, part of 45 leads across two accounts"),
            ("Cost per lead", "11.21", "Lease buyout, US, part of 45 leads across two accounts"),
            ("Cost per lead", "12.23", "B2B merchandise, US, 64 leads in 7 days on $782.84"),
        ],
    ),
    "benchmarks/click-to-messenger-ads-cost/index.html": dict(
        kind="dataset",
        title="Click-to-Messenger Ad Costs: $0.02 to $0.04 Per Chat",
        desc="Click-to-Messenger costs from three campaigns run in Bangladesh in 2025, including one producing 12,813 conversations for $576.51. Plus why they don't travel.",
        crumbs=[("Home", ""), ("Benchmarks", "benchmarks/")],
        modified="2026-08-07",
        dataset_name="Click-to-Messenger conversation cost, 3 campaigns, Bangladesh, 2025",
        coverage="2024/2025",
        places=["Bangladesh"],
        technique="Meta Ads Manager reporting, campaign level, USD",
        variables=[
            ("Cost per messaging conversation", "0.04", "Eid ul Adha campaign, 12,813 conversations on $576.51, 514,208 reach"),
            ("Cost per messaging conversation", "0.03", "Eid message campaign, 16 creatives across 4 ad sets, $135.49 spend"),
            ("Cost per messaging conversation", "0.02", "Best single ad set within the Eid message campaign"),
        ],
    ),

    # ---- conversion
    "free-audit/index.html": dict(
        kind="form",
        title="Free Facebook Ads & SEO Audit · No Cost, No Pitch",
        desc="Send me your ad account or your site. I'll review it before we speak and come back with what's costing you money and what I'd change first. No cost.",
        crumbs=[("Home", "")],
    ),
    "contact/index.html": dict(
        kind="form",
        title="Contact Arshad Hossain · Meta Ads & SEO Freelancer",
        desc="Ask a question, or tell me what isn't working in your ads or your search rankings. I reply within one business day.",
        crumbs=[("Home", "")],
    ),

    # ---- blog posts
    "blog/meta-ads-cost-per-lead/index.html": dict(
        kind="post",
        title="How I Cut a Facebook Ads Cost Per Lead From $86 to $3.91",
        desc="How I took a US hair clinic's Facebook Ads cost per lead down 95% across 35 campaigns: what I changed, in what order, and the two rounds that made it worse.",
        crumbs=[("Home", ""), ("Blog", BLOG)],
        published="2026-06-18", modified="2026-07-30",
    ),
    "blog/messenger-ads-bangladesh/index.html": dict(
        kind="post",
        title="Why Click-to-Messenger Beats Conversion Ads in Bangladesh",
        desc="12,813 Messenger conversations on $576.51 of spend, four cents each. Why conversational objectives win in F-commerce markets, and the four cases where they fail.",
        crumbs=[("Home", ""), ("Blog", BLOG)],
        published="2026-07-09", modified="2026-07-09",
    ),
    "blog/local-seo-clinic-page-one/index.html": dict(
        kind="post",
        title="Ranking a Medical Clinic on Page 1 in Three Months",
        desc="What it actually took to rank a Singapore clinic from zero organic traffic: the order of work, why healthcare SEO has a higher bar, and realistic timelines.",
        crumbs=[("Home", ""), ("Blog", BLOG)],
        published="2026-07-28", modified="2026-07-28",
    ),
}

# ---- case studies: result-led titles, because "[Client] Case Study"
#      targets a name nobody searches.
_CASES = [
    ("scalp-shop",           "$86 to $3.91 Cost Per Lead: Facebook Ads, US Hair Clinic",
     "How 35 Facebook Ads campaigns took a US hair and scalp clinic's cost per lead from $86 to $3.91, a 95% reduction, with a 94/100 Meta Opportunity Score."),
    ("nevada",               "$5.08 B2B Cost Per Lead: Facebook Ads for Nevada Access",
     "A full-funnel B2B Facebook Ads campaign producing 64 leads at $5.08 each, 63% below Meta's own benchmark, on a $100 awareness spend reaching 43,927 people."),
    ("wardrobe-by-syra",     "Wardrobe By Syra: 4 Meta Campaigns, 4 Objectives",
     "Four campaigns for one Bangladeshi fashion brand: 12,813 Messenger conversations at $0.04, 121 purchases at $0.71, and a Reel that hit 333,110 views."),
    ("lending",              "45 Facebook Ads Leads at $7.98 and $11.21 CPL, US Lender",
     "Two Facebook Ads lead gen campaigns for a US lending company: 45 leads at $7.98 and $11.21 cost per lead, with a 100/100 Meta Opportunity Score on both accounts."),
    ("roofing",              "70 Roofing Leads at $66.60 Cost Per Lead",
     "Facebook Ads for a US roofing company: 70 leads at $66.60 cost per lead, well under the $115+ published benchmark for the category. Campaign still running."),
    ("tombizmerch",          "64 B2B Leads in 7 Days at $12.23 Cost Per Lead",
     "Meta Ads for a FIFA World Cup merchandise store: 64 qualified B2B leads at $12.23 average cost per lead on $782.84 of spend, inside the first week of launch."),
    ("alami-clinic",         "Zero to Page 1 in Three Months: Medical SEO in Singapore",
     "Medical SEO for a Singapore clinic: Page 1 rankings within three months from a standing start, a 75% organic traffic increase, 516 clicks and 25,000 impressions."),
    ("gettakaful",           'Fintech SEO: #1 for "Takaful Insurance in Canada"',
     "SEO for a Canadian Islamic insurance startup: #1 rankings for takaful insurance in canada and shariah insurance in canada, through a blog-driven content strategy."),
    ("aifarming",            "AgriTech SEO: Page 1 for AI in Home Farming, Toronto",
     "SEO for a Toronto AgriTech platform: Page 1 for AI in home farming, plus rankings across balcony gardening and crop-growth queries. Topic authority from zero."),
    ("hills-harvest",        "39 to 700+ Visits: Local SEO for a Sydney Halal Grocer",
     "Local SEO for a Western Sydney halal delivery business: organic visits from 39 to 700+, keywords ranking from 49 to 202, and #1 for two suburb delivery terms."),
    ("pretty-party-platters", "670 to 2,800 Organic Visits: SEO for Pretty Party Platters",
     "SEO for Pretty Party Platters, a US caterer: organic traffic from 670 to 2,800 a month, keywords from 669 to 1,400, and 262 pages cited by AI assistants."),
]
for slug, title, desc in _CASES:
    PAGES[f"cases/{slug}/index.html"] = dict(
        kind="case", title=title, desc=desc,
        crumbs=[("Home", ""), ("Case Studies", CASES)],
    )

_PROJECTS = [
    ("daag",               "Daag · Civic Accountability Archive",
     "A crowdsourced platform documenting misogynistic online commentary in Bangladesh, with evidence submission, a moderation system and a searchable archive."),
    ("ismybabyalright",    "Is My Baby Alright? · Parenting Companion App",
     "A parenting app with milestone tracking, symptom triage, sleep logs, growth charts and mental health screening, built after becoming a father."),
    ("quillbill",          "QuillBill · Free Invoice & Proposal Generator",
     "A free invoice and proposal generator: 15+ templates, PDF export, shareable links and multi-currency support, with no account required."),
    ("prompt-black-magic", "Prompt Black Magic · AI Prompt Library for Marketers",
     "100+ curated AI prompts for Google Ads, SEO, social media, email marketing and productivity, with search, filter and one-click copy."),
]
# Side projects stay on the site for human visitors but out of the index.
# Each runs 134-190 words against a 489-word median: on a 32-page site they
# were an eighth of the indexable surface carrying no commercial intent.
for slug, title, desc in _PROJECTS:
    PAGES[f"projects/{slug}/index.html"] = dict(
        kind="project", title=title, desc=desc, noindex=True,
        crumbs=[("Home", ""), ("Projects", PROJECTS)],
    )

PAGES["404.html"] = dict(
    kind="util", title="Page Not Found", desc="That page doesn't exist.",
    crumbs=[], noindex=True,
)
