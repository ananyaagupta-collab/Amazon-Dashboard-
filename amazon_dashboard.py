import json, os, datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Native Products — Amazon Dashboard",
    page_icon="💧",
    layout="wide",
)

# ── Load JSON data files ──────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "history_data.json"))     as f: HISTORY     = json.load(f)
with open(os.path.join(BASE, "trends_data.json"))      as f: TRENDS      = json.load(f)
with open(os.path.join(BASE, "competitors_data.json")) as f: COMPETITORS = json.load(f)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .big-rating { font-size:2.2rem; font-weight:800; line-height:1; }
  .stars      { font-size:1.1rem; color:#ff9500; letter-spacing:2px; }
  .badge { display:inline-block; padding:2px 10px; border-radius:12px; font-size:.75rem; font-weight:600; }
  .badge-purifier { background:#e8f5e9; color:#2e7d32; }
  .badge-lock     { background:#e3f2fd; color:#1565c0; }
  .badge-instock  { background:#e8f5e9; color:#2e7d32; }
  .badge-unavail  { background:#fce4ec; color:#c62828; }
  .tag { display:inline-block; background:#f2f2f7; border-radius:12px; padding:2px 9px; font-size:.75rem; margin:2px; }
  hr.divider { border:none; border-top:1px solid #f0f0f0; margin:8px 0; }
  .section-label { font-size:.7rem; color:#8e8e93; text-transform:uppercase; letter-spacing:.7px; font-weight:600; margin-bottom:4px; }
  .ai-box { background:#fafafa; border-radius:10px; padding:12px 14px; border:1px solid #e5e5ea; font-size:.85rem; color:#3a3a3c; line-height:1.55; }
  .review-box { background:#fff; border-radius:8px; padding:10px 12px; border:1px solid #f0f0f0; margin-bottom:6px; }
  .review-author { font-weight:600; font-size:.82rem; }
  .review-date   { color:#8e8e93; font-size:.75rem; }
  .review-text   { font-size:.82rem; color:#3a3a3c; line-height:1.45; margin-top:4px; }
  .hist-note { font-size:.8rem; color:#8e8e93; line-height:1.55; padding:6px 0 12px; }
</style>
""", unsafe_allow_html=True)

# ── Product data ──────────────────────────────────────────────────────────────
PRODUCTS = [
    {
        "id":"m0","name":"Native M0 RO","category":"purifier",
        "rating":4.4,"review_count":532,"reviews_note":None,
        "monthly_buys":"500+","price":13499,"price_display":"₹13,499",
        "status":"in-stock","status_label":"In Stock",
        "url":"https://www.amazon.in/Native-RO-Mineraliser-Purifier-Unconditional/dp/B0FB3L3FSH",
        "stars":{5:75,4:12,3:3,2:1,1:9},
        "ai_summary":"Customers find this water purifier to be a very good product with reliable RO filtration and professional installation. They appreciate its value for money, great taste, and premium matte finish. The purifier is easy to maintain and hassle-free. However, several customers report issues with water leakage from the unit.",
        "sentiment_tags":[("Quality",166),("Filter performance",50),("Installation",43),("Value for money",36),("Water taste",27),("Water leakage",16)],
        "reviews":[
            {"author":"Gaurav","rating":5,"date":"14 Jun 2026","text":"Using this RO for about a month. Delivery by Amazon and installation by UC was fantastic — the technician was a thorough professional. Water filtration is good, TDS meter provided. Sleek and blends with any kitchen. Unconditional 2-year warranty incl. filters."},
            {"author":"Margi Buch (M1)","rating":5,"date":"13 Jun 2026","text":"Very good filtration and good taste of water. Compact and looks good."},
            {"author":"viswanath","rating":4,"date":"9 Jun 2026","text":"Really best product within the budget. Installation also very smooth. Overall value for the money."},
            {"author":"Ghintoxon Shamaddar","rating":5,"date":"14 May 2026","text":"Good buy. Worth the cost. Satisfied after using for a couple of weeks. Installation was seamless and the technician was extremely competent."},
        ],
    },
    {
        "id":"m1","name":"Native M1 RO","category":"purifier",
        "rating":4.4,"review_count":6495,"reviews_note":None,
        "monthly_buys":"2K+","price":15999,"price_display":"₹15,999",
        "status":"in-stock","status_label":"In Stock",
        "url":"https://www.amazon.in/Native-Purifier-RO-Copper-Alkaline/dp/B0D79G62J3",
        "stars":{5:76,4:13,3:2,2:0,1:9},
        "ai_summary":"Customers find this water purifier to be the best in the market, with excellent installation and professional service. The product offers good value for money, with one customer noting the TDS value is below 100, and they appreciate its well-designed appearance. The water quality receives positive feedback — consistently reducing TDS for a crisp taste.",
        "sentiment_tags":[("Quality","1.5K"),("Installation",389),("Value for money",273),("Reliability",246),("Appearance",203),("Water taste",184)],
        "reviews":[
            {"author":"Nandan Kumar","rating":5,"date":"15 Jun 2026","text":"The Native M1 has proven to be an excellent choice. Build quality feels sturdy and well-designed. Purification performance is impressive, delivering great-tasting water consistently."},
            {"author":"Margi Buch","rating":5,"date":"13 Jun 2026","text":"Very good filtration and good taste of water. Compact and looks good."},
            {"author":"Raizada vageesh","rating":4,"date":"30 May 2026","text":"Water does not taste too bitter. Quality seems nice. Great installation service — even attached a custom faucet I provided for no charge."},
            {"author":"Amit Katoch","rating":5,"date":"17 May 2026","text":"Hassle-free scheduling via UC app. No hidden extra charges — external pre-filter included. Professional setup takes less than 45 minutes."},
        ],
    },
    {
        "id":"m1pro","name":"Native M1 Pro RO","category":"purifier",
        "rating":4.4,"review_count":6495,"reviews_note":"(shared listing with M1)",
        "monthly_buys":"600+","price":17499,"price_display":"₹17,499",
        "status":"in-stock","status_label":"In Stock",
        "url":"https://www.amazon.in/Native-Purifier-Real-Time-Mineraliser-Unconditional/dp/B0GWQFXMTY",
        "stars":{5:76,4:13,3:2,2:0,1:9},
        "ai_summary":"Customers find this water purifier to be the best in the market, with excellent installation and professional service. The smart real-time tracking and 12-parameter health check are highlighted features. Good value for money, well-designed appearance, and consistent TDS reduction. (Shares Amazon review pool with the M1.)",
        "sentiment_tags":[("Quality","1.5K"),("Installation",389),("Value for money",273),("Reliability",246),("Appearance",203),("Water taste",184)],
        "reviews":[
            {"author":"Sweta","rating":5,"date":"5 Jun 2026","text":"Has 100% RO and water tasting good. App shows filter and water health. 2 year warranty without T&C. Very good design, looks good in my kitchen."},
            {"author":"Nandan Kumar","rating":5,"date":"15 Jun 2026","text":"Build quality feels sturdy and well-designed. Purification performance is impressive. System works smoothly, user-friendly even for first-time users."},
            {"author":"Raizada vageesh","rating":4,"date":"30 May 2026","text":"Water does not taste too bitter. Quality seems nice. Great installation service — attached a custom faucet for no charge."},
            {"author":"Amit Katoch","rating":5,"date":"17 May 2026","text":"Hassle-free scheduling via UC app. No hidden extra charges — pre-filter included. Installation takes less than 45 minutes."},
        ],
    },
    {
        "id":"m2pro","name":"Native M2 Pro RO","category":"purifier",
        "rating":4.4,"review_count":1529,"reviews_note":None,
        "monthly_buys":"2K+","price":19499,"price_display":"₹19,499",
        "status":"in-stock","status_label":"In Stock",
        "url":"https://www.amazon.in/Native-M2-Pro-Dispensing-Mineraliser/dp/B0G4CHKBGP",
        "stars":{5:79,4:10,3:1,2:0,1:10},
        "ai_summary":"Customers find this water purifier to be of good quality and appreciate its appearance, with one noting its modern touch panel with LED indicators. The product is easy to use — highlighted for its convenience for elderly people. Customers appreciate the smart features, preset dispensing modes, and good water taste. Some report it stops working when there is no power.",
        "sentiment_tags":[("Quality",409),("Installation",105),("Reliability",95),("Value for money",82),("Water taste",54),("Ease of use",43)],
        "reviews":[
            {"author":"Sushil Sakhuja","rating":5,"date":"10 Jun 2026","text":"Best economic water purifier I have owned so far. I was so satisfied I purchased it twice for two different flats. Its reliability, quality, and overall user experience have exceeded my expectations."},
            {"author":"Manoj Joshi","rating":5,"date":"9 Jun 2026","text":"Extremely satisfied. Water quality is excellent, touch dispensing feature is very convenient, and the purifier looks premium in my kitchen."},
            {"author":"bondili mahender singh","rating":5,"date":"4 Jun 2026","text":"Product quality is excellent and water tastes clean and fresh. Smart app lets me track consumption, monitor filter health and check performance in real time."},
            {"author":"Gen reviews","rating":4,"date":"30 May 2026","text":"Good water purifier with useful features. Includes a pre-filter. Only downside: food-grade plastic tank instead of stainless steel at this price point."},
        ],
    },
    {
        "id":"lockpro","name":"Native Lock Pro","category":"lock",
        "rating":4.6,"review_count":562,"reviews_note":None,
        "monthly_buys":"50+","price":16999,"price_display":"₹16,999",
        "status":"in-stock","status_label":"In Stock",
        "url":"https://www.amazon.in/Urban-Company-Native-Smart-Lock/dp/B0DJH6Q2XQ",
        "stars":{5:84,4:7,3:1,2:2,1:6},
        "ai_summary":"Customers find this smart lock to be of excellent quality, with professional installation and reliable performance. They appreciate its sleek appearance, ease of use with a good app interface, and consider it a great value. Multiple access options for self and family, and the password masking functionality are highlighted.",
        "sentiment_tags":[("Quality",108),("Installation",63),("Reliability",37),("Appearance",22),("Service",17),("Ease of use",15)],
        "reviews":[
            {"author":"chandran","rating":5,"date":"7 Jun 2026","text":"The Lock Pro is a perfect solution for the front door. Very competent installation. Very easy to use, yet quite safe. Met our requirement to the full."},
            {"author":"Amazon Customer","rating":5,"date":"8 Jun 2026","text":"Very good lock."},
            {"author":"Vishal Pandey","rating":5,"date":"3 Jun 2026","text":"Awesome lock, good features. Good connectivity and durable. Neatly setup by the technician."},
            {"author":"Raizada vageesh","rating":4,"date":"30 May 2026","text":"Good product, value for money. Fingerprint reader working well. Installation was great and the colour looks good too."},
        ],
    },
    {
        "id":"lockultra","name":"Native Lock Ultra","category":"lock",
        "rating":5.0,"review_count":7,"reviews_note":None,
        "monthly_buys":None,"price":None,"price_display":"Currently Unavailable",
        "status":"out-of-stock","status_label":"Unavailable",
        "url":"https://www.amazon.in/Native-Lock-Ultra-Urban-Company/dp/B0H2MVF2L2",
        "stars":{5:100,4:0,3:0,2:0,1:0},
        "ai_summary":None,"sentiment_tags":[],
        "reviews":[
            {"author":"Ayesha Tabassum","rating":5,"date":"14 Jun 2026","text":"As sturdy as it gets with 5 bolts. Looks good, very sleek and futuristic. App integration is smooth and UI is good. Bonus point for the face unlock."},
            {"author":"Hamaad malik","rating":5,"date":"12 Jun 2026","text":"A little skeptical on buying as it is slightly pricey, but after installation it is really worth it. Panels, material and overall build quality is very premium."},
            {"author":"Sita Ram","rating":5,"date":"11 Jun 2026","text":"Good product. Looks very nice and sleek. Go for it if you like design and reliability."},
            {"author":"MAYANK","rating":5,"date":"13 May 2026","text":"Top of the line product. Face ID is seamless, works even in complete darkness. Live video feature is very useful. Installation done within 2 hours."},
        ],
    },
]

STAR_COLORS = {5:"#ff9500", 4:"#ffcc02", 3:"#a8c5f0", 2:"#ffb3b3", 1:"#ff3b30"}
TREND_COLORS = {
    "m0":"#9333ea","m1":"#ff6900","m1pro":"#f97316","m2pro":"#2563eb",
    "lockpro":"#16a34a","lockultra":"#dc2626",
}
SKU_TO_CAT = {
    "m0":"purifier","m1":"purifier","m1pro":"purifier","m2pro":"purifier",
    "lockpro":"lock","lockultra":"lock",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def star_str(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    return "★" * full + ("½" if half else "") + "☆" * (5 - full - half)

def fmt_num(n):
    if isinstance(n, str):
        return n
    if n >= 1000:
        v = n / 1000
        return f"{v:.1f}K".replace(".0K","K")
    return str(n)

def days_ago(days):
    return (datetime.date.today() - datetime.timedelta(days=days)).isoformat()

def filter_hist(rows, days):
    if days == 0:
        return rows
    cutoff = days_ago(days)
    return [r for r in rows if r[0] >= cutoff]

def filter_trend(rows, days):
    if days == 0:
        return rows
    cutoff = days_ago(days)
    return [r for r in rows if r["d"] >= cutoff]


# ── Page header ───────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown(
        '<div style="background:linear-gradient(135deg,#ff6900,#ff9a00);width:42px;height:42px;'
        'border-radius:10px;display:flex;align-items:center;justify-content:center;'
        'font-size:20px;font-weight:800;color:white;margin-top:4px;">N</div>',
        unsafe_allow_html=True,
    )
with col_title:
    st.markdown("## Native Products — Amazon Dashboard")
    st.caption("Urban Company · amazon.in · Last updated: 19 Jun 2026")

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_live, tab_hist, tab_trends = st.tabs(["📊 Live Ratings", "📅 History", "📈 Trends"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE RATINGS
# ═══════════════════════════════════════════════════════════════════════════════
def render_star_bars(stars):
    fig = go.Figure()
    for star in [5, 4, 3, 2, 1]:
        pct = stars.get(star, 0)
        color = "#ff3b30" if star <= 2 else "#ff9500"
        fig.add_trace(go.Bar(
            x=[pct], y=[f"{star}★"], orientation="h",
            marker_color=color,
            text=[f"{pct}%"], textposition="outside",
            hovertemplate=f"{star}★: {pct}%<extra></extra>",
        ))
    fig.update_layout(
        showlegend=False, margin=dict(l=0,r=40,t=0,b=0), height=130,
        xaxis=dict(range=[0,115], visible=False),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white", paper_bgcolor="white", bargap=0.25,
    )
    return fig

def render_product_card(p):
    cat_emoji = "💧" if p["category"] == "purifier" else "🔒"
    cat_label = "Water Purifier" if p["category"] == "purifier" else "Smart Lock"
    cat_cls   = "badge-purifier" if p["category"] == "purifier" else "badge-lock"
    stk_cls   = "badge-instock" if p["status"] == "in-stock" else "badge-unavail"

    with st.container(border=True):
        c1, c2 = st.columns([4,1])
        with c1:
            st.markdown(f"**{p['name']}**")
            st.markdown(f'<span class="badge {cat_cls}">{cat_emoji} {cat_label}</span>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="text-align:right"><span class="badge {stk_cls}">{p["status_label"]}</span></div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,3,2])
        with c1:
            st.markdown(f'<div class="big-rating">{p["rating"]:.1f}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stars">{star_str(p["rating"])}</div>', unsafe_allow_html=True)
            note = f" {p['reviews_note']}" if p["reviews_note"] else ""
            st.caption(f'{fmt_num(p["review_count"])} reviews{note}')
        with c3:
            if p["monthly_buys"]:
                st.metric("This month", p["monthly_buys"])

        c1, c2 = st.columns([2,2])
        with c1:
            st.markdown(f"### {p['price_display']}")
            st.caption("incl. GST")
        with c2:
            st.markdown(f'<div style="padding-top:14px"><a href="{p["url"]}" target="_blank" style="color:#ff6900;font-weight:600;text-decoration:none;">View on Amazon ↗</a></div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Rating Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(render_star_bars(p["stars"]), use_container_width=True, config={"displayModeBar":False}, key=f"stars_{p['id']}")

        st.markdown('<div class="section-label">🤖 AI Amazon Customer Summary</div>', unsafe_allow_html=True)
        if p["ai_summary"]:
            st.markdown(f'<div class="ai-box">{p["ai_summary"]}</div>', unsafe_allow_html=True)
            if p["sentiment_tags"]:
                tags_html = " ".join(f'<span class="tag"><b>{l}</b> {c}</span>' for l,c in p["sentiment_tags"])
                st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.caption("Not enough reviews yet for an AI summary.")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recent Reviews</div>', unsafe_allow_html=True)
        show_all = st.toggle("Show all reviews", key=f"tog_{p['id']}")
        for r in (p["reviews"] if show_all else p["reviews"][:2]):
            stars_disp = "★" * r["rating"] + "☆" * (5 - r["rating"])
            st.markdown(
                f'<div class="review-box">'
                f'<span class="review-author">{r["author"]}</span> '
                f'<span class="review-date">{r["date"]}</span>'
                f'<div style="color:#ff9500;font-size:.8rem">{stars_disp}</div>'
                f'<div class="review-text">{r["text"]}</div></div>',
                unsafe_allow_html=True,
            )

with tab_live:
    col_filter, col_sort = st.columns([3,1])
    with col_filter:
        category = st.radio("Category", ["All Products","💧 Water Purifiers","🔒 Smart Locks"],
                            horizontal=True, label_visibility="collapsed")
    with col_sort:
        sort_by = st.selectbox("Sort", ["Default","Rating: High → Low","Most Reviews",
                                        "Price: Low → High","Price: High → Low"],
                               label_visibility="collapsed")

    cat_map  = {"All Products":None,"💧 Water Purifiers":"purifier","🔒 Smart Locks":"lock"}
    products = [p for p in PRODUCTS if cat_map[category] is None or p["category"]==cat_map[category]]

    if sort_by == "Rating: High → Low":   products = sorted(products, key=lambda p: p["rating"], reverse=True)
    elif sort_by == "Most Reviews":        products = sorted(products, key=lambda p: p["review_count"], reverse=True)
    elif sort_by == "Price: Low → High":  products = sorted(products, key=lambda p: p["price"] or float("inf"))
    elif sort_by == "Price: High → Low":  products = sorted(products, key=lambda p: p["price"] or 0, reverse=True)

    avg_rating   = sum(p["rating"] for p in products)/len(products) if products else 0
    total_rev    = sum(p["review_count"] for p in products if not p["reviews_note"])
    in_stock_cnt = sum(1 for p in products if p["status"]!="out-of-stock")
    top_p        = max(products, key=lambda p: p["rating"]) if products else None

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Products Shown",  len(products))
    m2.metric("Avg Rating",      f"{avg_rating:.2f} ★")
    m3.metric("Total Reviews",   fmt_num(total_rev))
    m4.metric("In Stock",        f"{in_stock_cnt}/{len(products)}")
    m5.metric("Highest Rated",   top_p["name"] if top_p else "—")

    st.divider()

    if not products:
        st.info("No products match this filter.")
    else:
        cols = st.columns(2, gap="medium")
        for i, product in enumerate(products):
            with cols[i % 2]:
                render_product_card(product)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
HIST_LABELS = {
    "m1pro":"M1 / M1 Pro","m2pro":"M2 Pro","lockpro":"Lock Pro","m0":"M0","lockultra":"Lock Ultra"
}

with tab_hist:
    st.markdown(
        '<div class="hist-note">Day-on-day view built from the sample of written reviews (12,418 with text). '
        'These counts track review growth and the star mix over time and are smaller than the live listing\'s '
        'total rating counts. M1 and M1 Pro share a single Amazon review pool. Lock Ultra isn\'t in the bulk '
        'text-review sample, so only its handful of individually-dated reviews (all 5★) are shown — its series is sparse.</div>',
        unsafe_allow_html=True,
    )

    hc1, hc2 = st.columns([3,2])
    with hc1:
        sel_sku = st.radio("Product", list(HIST_LABELS.keys()),
                           format_func=lambda k: HIST_LABELS[k],
                           horizontal=True, key="hist_sku")
    with hc2:
        period_map = {"30D":30,"90D":90,"1Y":365,"All":0}
        period_lbl = st.radio("Period", list(period_map.keys()), index=3, horizontal=True, key="hist_period")

    days    = period_map[period_lbl]
    raw     = HISTORY.get(sel_sku, {})
    rows    = filter_hist(raw.get("daily",[]), days)

    if not rows:
        st.info("No data for this selection.")
    else:
        dates     = [r[0] for r in rows]
        # each row: [date, 1★count, 2★count, 3★count, 4★count, 5★count]
        star_daily = {s: [r[s] for r in rows] for s in range(1,6)}

        # cumulative per star
        star_cum = {}
        for s in range(1,6):
            running, cum = 0, []
            for v in star_daily[s]:
                running += v; cum.append(running)
            star_cum[s] = cum

        total_cum = []
        running = 0
        for i in range(len(dates)):
            running += sum(star_daily[s][i] for s in range(1,6))
            total_cum.append(running)

        s1,s2,s3 = st.columns(3)
        s1.metric("Reviews in sample", fmt_num(raw.get("total", total_cum[-1])))
        s2.metric("Date range", f"{dates[0]}  →  {dates[-1]}")
        s3.metric("Days shown", len(dates))

        # ── Ratings over time ─────────────────────────────────────────────────
        mode_vol = st.radio("Chart mode", ["Cumulative","New per day"],
                            horizontal=True, key="hist_vol")
        fig_vol = go.Figure()
        for s in [5,4,3,2,1]:
            y = star_cum[s] if mode_vol=="Cumulative" else star_daily[s]
            fig_vol.add_trace(go.Bar(
                x=dates, y=y, name=f"{s}★",
                marker_color=STAR_COLORS[s],
                hovertemplate=f"{s}★: %{{y}}<extra></extra>",
            ))
        fig_vol.update_layout(
            title="Ratings over time", barmode="stack", height=320,
            margin=dict(l=0,r=0,t=40,b=0),
            legend=dict(orientation="h",yanchor="bottom",y=1.02),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#f0f0f0"),
        )
        st.plotly_chart(fig_vol, use_container_width=True, key="hist_vol_chart")

        # ── Star skew over time ───────────────────────────────────────────────
        mode_skew = st.radio("Chart mode", ["Cumulative mix %","New per day"],
                             horizontal=True, key="hist_skew")
        fig_skew = go.Figure()
        for s in [5,4,3,2,1]:
            if mode_skew == "Cumulative mix %":
                y = [round(star_cum[s][i]/total_cum[i]*100,1) if total_cum[i] else 0
                     for i in range(len(dates))]
            else:
                y = star_daily[s]
            fig_skew.add_trace(go.Scatter(
                x=dates, y=y, name=f"{s}★", mode="lines",
                line=dict(color=STAR_COLORS[s], width=2),
                hovertemplate=f"{s}★: %{{y}}<extra></extra>",
            ))
        fig_skew.update_layout(
            title="Star skew over time", height=300,
            margin=dict(l=0,r=0,t=40,b=0),
            legend=dict(orientation="h",yanchor="bottom",y=1.02),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#f0f0f0"),
        )
        st.plotly_chart(fig_skew, use_container_width=True, key="hist_skew_chart")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_trends:
    st.markdown(
        '<div class="hist-note">Trends use the DOD Ratings Tracker sheet (M2 Pro, M0, Lock Pro) from 14 Apr 2026 onward. '
        'M1 and M1 Pro aren\'t tracked in that sheet — they\'re seeded with today\'s Amazon values and build up daily '
        'going forward. Per-star counts are derived from each day\'s star-% and total review count.</div>',
        unsafe_allow_html=True,
    )

    tc1, tc2, tc3 = st.columns([2,2,3])
    with tc1:
        tr_cat = st.radio("Type", ["All","Purifiers","Locks"], horizontal=True, key="tr_cat")
    with tc2:
        tr_period_map = {"7D":7,"30D":30,"90D":90,"All":0}
        tr_period = st.radio("Period", list(tr_period_map.keys()), index=3, horizontal=True, key="tr_period")
        tr_days = tr_period_map[tr_period]
    with tc3:
        cat_filter = {"All":None,"Purifiers":"purifier","Locks":"lock"}[tr_cat]
        avail_skus = [k for k in TRENDS if cat_filter is None or SKU_TO_CAT.get(k)==cat_filter]
        sel_skus   = st.multiselect(
            "Products", avail_skus, default=avail_skus,
            format_func=lambda k: TRENDS[k].get("label", k),
            key="tr_skus",
        )

    if not sel_skus:
        st.info("Select at least one product above.")
    else:
        sku_rows = {sku: filter_trend(TRENDS[sku].get("daily",[]), tr_days)
                   for sku in sel_skus if filter_trend(TRENDS[sku].get("daily",[]), tr_days)}

        if not sku_rows:
            st.info("No data for this period.")
        else:
            # Summary metrics
            stat_cols = st.columns(len(sku_rows))
            for i,(sku,rows) in enumerate(sku_rows.items()):
                last = rows[-1]
                stat_cols[i].metric(
                    TRENDS[sku].get("label",sku),
                    f"{last['r']} ★",
                    f"{fmt_num(last['t'])} reviews",
                )

            st.divider()

            # ── Chart 1: Rating line + stacked star counts ────────────────────
            fig_main = make_subplots(specs=[[{"secondary_y":True}]])
            first_sku = True
            for sku, rows in sku_rows.items():
                dates = [r["d"] for r in rows]
                for s in [1,2,3,4,5]:
                    fig_main.add_trace(go.Bar(
                        x=dates, y=[r.get(f"c{s}",0) for r in rows],
                        name=f"{s}★", marker_color=STAR_COLORS[s], opacity=0.65,
                        showlegend=first_sku,
                        hovertemplate=f"{s}★ count: %{{y}}<extra></extra>",
                    ), secondary_y=False)
                fig_main.add_trace(go.Scatter(
                    x=dates, y=[r["r"] for r in rows],
                    name=TRENDS[sku].get("label",sku),
                    line=dict(color=TREND_COLORS.get(sku,"#333"), width=2.5),
                    mode="lines+markers", marker=dict(size=4),
                    hovertemplate="Rating: %{y:.2f}<extra></extra>",
                ), secondary_y=True)
                first_sku = False
            fig_main.update_layout(
                title="Daily rating & total ratings (stacked by star)",
                barmode="stack", height=360,
                margin=dict(l=0,r=0,t=40,b=0),
                legend=dict(orientation="h",yanchor="bottom",y=1.02),
                plot_bgcolor="white", paper_bgcolor="white",
            )
            fig_main.update_yaxes(title_text="Review count", secondary_y=False)
            fig_main.update_yaxes(title_text="Rating", range=[3.5,5.2], secondary_y=True)
            st.plotly_chart(fig_main, use_container_width=True, key="tr_main_chart")

            # ── Charts per star (5★ down to 1★) ──────────────────────────────
            for s in [5,4,3,2,1]:
                fig_s = make_subplots(specs=[[{"secondary_y":True}]])
                for sku, rows in sku_rows.items():
                    dates = [r["d"] for r in rows]
                    fig_s.add_trace(go.Bar(
                        x=dates, y=[r.get(f"c{s}",0) for r in rows],
                        name=f"{TRENDS[sku].get('label',sku)} count",
                        marker_color=STAR_COLORS[s], opacity=0.7,
                        hovertemplate="Count: %{y}<extra></extra>",
                    ), secondary_y=False)
                    fig_s.add_trace(go.Scatter(
                        x=dates, y=[r.get(f"p{s}",0) for r in rows],
                        name=f"{TRENDS[sku].get('label',sku)} %",
                        line=dict(color=TREND_COLORS.get(sku,"#333"), width=2),
                        mode="lines",
                        hovertemplate="%%: %{y:.1f}%%<extra></extra>",
                    ), secondary_y=True)
                fig_s.update_layout(
                    title=f"{s}★ ratings — count (bar) & % of total (line)",
                    height=260, margin=dict(l=0,r=0,t=40,b=0),
                    legend=dict(orientation="h",yanchor="bottom",y=1.02),
                    plot_bgcolor="white", paper_bgcolor="white",
                )
                fig_s.update_yaxes(title_text="Count",   secondary_y=False)
                fig_s.update_yaxes(title_text="% share", secondary_y=True)
                st.plotly_chart(fig_s, use_container_width=True, key=f"tr_star{s}_chart")

            st.divider()

            # ── Competitor comparison ─────────────────────────────────────────
            st.subheader("Competitors — rating trend vs Native")
            st.markdown(
                '<div class="hist-note">Competitor ratings are seeded with the Jun 2026 Amazon snapshot. '
                'Native lines come from the live tracker. The Period control above applies.</div>',
                unsafe_allow_html=True,
            )

            comp_cat  = "lock" if tr_cat == "Locks" else "purifier"
            comp_keys = [k for k,v in COMPETITORS.items() if v.get("category","purifier")==comp_cat]

            fig_comp = go.Figure()
            for sku, rows in sku_rows.items():
                if SKU_TO_CAT.get(sku) == comp_cat:
                    fig_comp.add_trace(go.Scatter(
                        x=[r["d"] for r in rows],
                        y=[r["r"] for r in rows],
                        name=f"Native {TRENDS[sku].get('label',sku)}",
                        line=dict(color=TREND_COLORS.get(sku,"#ff6900"), width=3),
                        mode="lines+markers", marker=dict(size=5),
                    ))
            for ck in comp_keys:
                cv   = COMPETITORS[ck]
                rows = filter_trend(cv.get("daily",[]), tr_days)
                if rows:
                    fig_comp.add_trace(go.Scatter(
                        x=[r["d"] for r in rows],
                        y=[r["r"] for r in rows],
                        name=cv.get("label",ck),
                        line=dict(color=cv.get("color","#999"), width=1.5, dash="dot"),
                        mode="lines",
                    ))
            fig_comp.update_layout(
                height=360, margin=dict(l=0,r=0,t=20,b=0),
                legend=dict(orientation="h",yanchor="bottom",y=1.02),
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(range=[3.5,5.2], gridcolor="#f0f0f0", title="Rating"),
                xaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_comp, use_container_width=True, key="tr_comp_chart")

            # Competitor snapshot cards
            st.markdown("**Competitor snapshot — Jun 2026**")
            if comp_keys:
                comp_cols = st.columns(min(len(comp_keys), 4))
                for i, ck in enumerate(comp_keys):
                    cv = COMPETITORS[ck]
                    d  = cv.get("daily",[])[0] if cv.get("daily") else {}
                    with comp_cols[i % 4]:
                        with st.container(border=True):
                            st.markdown(f"**{cv.get('label',ck)}**")
                            st.caption(cv.get("brand",""))
                            if d:
                                st.metric("Rating", f"{d.get('r','—')} ★",
                                          f"{fmt_num(d.get('t',0))} reviews")
                            st.markdown(
                                f'<a href="{cv.get("url","#")}" target="_blank" '
                                f'style="color:#ff6900;font-size:.8rem;">View on Amazon ↗</a>',
                                unsafe_allow_html=True,
                            )
