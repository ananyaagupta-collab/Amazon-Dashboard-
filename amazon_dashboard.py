import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Native Products — Amazon Dashboard",
    page_icon="💧",
    layout="wide",
)

# ── Custom styling ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  .big-rating { font-size: 2.2rem; font-weight: 800; line-height: 1; }
  .stars      { font-size: 1.1rem; color: #ff9500; letter-spacing: 2px; }
  .badge      { display:inline-block; padding:2px 10px; border-radius:12px;
                font-size:0.75rem; font-weight:600; }
  .badge-purifier { background:#e8f5e9; color:#2e7d32; }
  .badge-lock     { background:#e3f2fd; color:#1565c0; }
  .badge-instock  { background:#e8f5e9; color:#2e7d32; }
  .badge-unavail  { background:#fce4ec; color:#c62828; }
  .tag { display:inline-block; background:#f2f2f7; border-radius:12px;
         padding:2px 9px; font-size:0.75rem; margin:2px; }
  hr.divider { border:none; border-top:1px solid #f0f0f0; margin:8px 0; }
  .section-label { font-size:0.7rem; color:#8e8e93; text-transform:uppercase;
                   letter-spacing:.7px; font-weight:600; margin-bottom:4px; }
  .ai-box { background:#fafafa; border-radius:10px; padding:12px 14px;
            border:1px solid #e5e5ea; font-size:0.85rem; color:#3a3a3c;
            line-height:1.55; }
  .review-box { background:#fff; border-radius:8px; padding:10px 12px;
                border:1px solid #f0f0f0; margin-bottom:6px; }
  .review-author { font-weight:600; font-size:0.82rem; }
  .review-date   { color:#8e8e93; font-size:0.75rem; }
  .review-text   { font-size:0.82rem; color:#3a3a3c; line-height:1.45; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

# ── Product data ─────────────────────────────────────────────────────────────
PRODUCTS = [
    {
        "id": "m0", "name": "Native M0 RO", "category": "purifier",
        "rating": 4.4, "review_count": 532, "reviews_note": None,
        "monthly_buys": "500+", "price": 13499, "price_display": "₹13,499",
        "status": "in-stock", "status_label": "In Stock",
        "url": "https://www.amazon.in/Native-RO-Mineraliser-Purifier-Unconditional/dp/B0FB3L3FSH",
        "stars": {5: 75, 4: 12, 3: 3, 2: 1, 1: 9},
        "ai_summary": (
            "Customers find this water purifier to be a very good product with reliable RO "
            "filtration and professional installation. They appreciate its value for money, great "
            "taste, and premium matte finish. The purifier is easy to maintain and hassle-free. "
            "However, several customers report issues with water leakage from the unit."
        ),
        "sentiment_tags": [
            ("Quality", 166), ("Filter performance", 50), ("Installation", 43),
            ("Value for money", 36), ("Water taste", 27), ("Water leakage", 16),
        ],
        "reviews": [
            {"author": "Gaurav", "rating": 5, "date": "14 Jun 2026",
             "text": "Using this RO for about a month. Delivery by Amazon and installation by UC was fantastic — the technician was a thorough professional. Water filtration is good, TDS meter provided. Sleek and blends with any kitchen. Unconditional 2-year warranty incl. filters."},
            {"author": "Margi Buch (M1)", "rating": 5, "date": "13 Jun 2026",
             "text": "Very good filtration and good taste of water. Compact and looks good."},
            {"author": "viswanath", "rating": 4, "date": "9 Jun 2026",
             "text": "Really best product within the budget. Installation also very smooth. Overall value for the money."},
            {"author": "Ghintoxon Shamaddar", "rating": 5, "date": "14 May 2026",
             "text": "Good buy. Worth the cost. Satisfied after using for a couple of weeks. Installation was seamless and the technician was extremely competent. Water quality has improved a lot."},
        ],
    },
    {
        "id": "m1", "name": "Native M1 RO", "category": "purifier",
        "rating": 4.4, "review_count": 6495, "reviews_note": None,
        "monthly_buys": "2K+", "price": 15999, "price_display": "₹15,999",
        "status": "in-stock", "status_label": "In Stock",
        "url": "https://www.amazon.in/Native-Purifier-RO-Copper-Alkaline/dp/B0D79G62J3",
        "stars": {5: 76, 4: 13, 3: 2, 2: 0, 1: 9},
        "ai_summary": (
            "Customers find this water purifier to be the best in the market, with excellent "
            "installation and professional service. The product offers good value for money, with "
            "one customer noting the TDS value is below 100, and they appreciate its well-designed "
            "appearance. The water quality receives positive feedback — consistently reducing TDS for a crisp taste."
        ),
        "sentiment_tags": [
            ("Quality", "1.5K"), ("Installation", 389), ("Value for money", 273),
            ("Reliability", 246), ("Appearance", 203), ("Water taste", 184),
        ],
        "reviews": [
            {"author": "Nandan Kumar", "rating": 5, "date": "15 Jun 2026",
             "text": "The Native M1 has proven to be an excellent choice. Build quality feels sturdy and well-designed. Purification performance is impressive, delivering great-tasting water consistently. Installation was quick and hassle-free."},
            {"author": "Margi Buch", "rating": 5, "date": "13 Jun 2026",
             "text": "Very good filtration and good taste of water. Compact and looks good."},
            {"author": "Raizada vageesh", "rating": 4, "date": "30 May 2026",
             "text": "Water does not taste too bitter. Quality seems nice. Great installation service — even attached a custom faucet I provided for no charge. No leakage as of yet."},
            {"author": "Amit Katoch", "rating": 5, "date": "17 May 2026",
             "text": "Hassle-free scheduling via UC app. No hidden extra charges — external pre-filter included. Professional setup takes less than 45 minutes."},
        ],
    },
    {
        "id": "m1pro", "name": "Native M1 Pro RO", "category": "purifier",
        "rating": 4.4, "review_count": 6495, "reviews_note": "(shared listing with M1)",
        "monthly_buys": "600+", "price": 17499, "price_display": "₹17,499",
        "status": "in-stock", "status_label": "In Stock",
        "url": "https://www.amazon.in/Native-Purifier-Real-Time-Mineraliser-Unconditional/dp/B0GWQFXMTY",
        "stars": {5: 76, 4: 13, 3: 2, 2: 0, 1: 9},
        "ai_summary": (
            "Customers find this water purifier to be the best in the market, with excellent "
            "installation and professional service. The smart real-time tracking and 12-parameter "
            "health check are highlighted features. The product offers good value for money, with "
            "well-designed appearance and consistent TDS reduction. (Shares Amazon review pool with the M1.)"
        ),
        "sentiment_tags": [
            ("Quality", "1.5K"), ("Installation", 389), ("Value for money", 273),
            ("Reliability", 246), ("Appearance", 203), ("Water taste", 184),
        ],
        "reviews": [
            {"author": "Sweta", "rating": 5, "date": "5 Jun 2026",
             "text": "Has 100% RO and water tasting good. App shows filter and water health. 2 year warranty without T&C. Very good design, looks good in my kitchen."},
            {"author": "Nandan Kumar", "rating": 5, "date": "15 Jun 2026",
             "text": "Build quality feels sturdy and well-designed. Purification performance is impressive. System works smoothly, user-friendly even for first-time users. Great value for money."},
            {"author": "Raizada vageesh", "rating": 4, "date": "30 May 2026",
             "text": "Water does not taste too bitter. Quality seems nice. Great installation service — attached a custom faucet for no charge. No leakage as of yet."},
            {"author": "Amit Katoch", "rating": 5, "date": "17 May 2026",
             "text": "Hassle-free scheduling via UC app. No hidden extra charges — pre-filter included. Installation takes less than 45 minutes."},
        ],
    },
    {
        "id": "m2pro", "name": "Native M2 Pro RO", "category": "purifier",
        "rating": 4.4, "review_count": 1529, "reviews_note": None,
        "monthly_buys": "2K+", "price": 19499, "price_display": "₹19,499",
        "status": "in-stock", "status_label": "In Stock",
        "url": "https://www.amazon.in/Native-M2-Pro-Dispensing-Mineraliser/dp/B0G4CHKBGP",
        "stars": {5: 79, 4: 10, 3: 1, 2: 0, 1: 10},
        "ai_summary": (
            "Customers find this water purifier to be of good quality and appreciate its appearance, "
            "with one noting its modern touch panel with LED indicators. The product is easy to use — "
            "highlighted for its convenience for elderly people. Customers appreciate the smart features, "
            "preset dispensing modes, and good water taste. Some report it stops working when there is no power."
        ),
        "sentiment_tags": [
            ("Quality", 409), ("Installation", 105), ("Reliability", 95),
            ("Value for money", 82), ("Water taste", 54), ("Ease of use", 43),
        ],
        "reviews": [
            {"author": "Sushil Sakhuja", "rating": 5, "date": "10 Jun 2026",
             "text": "Best economic water purifier I have owned so far. I was so satisfied I purchased it twice for two different flats. Its reliability, quality, and overall user experience have exceeded my expectations."},
            {"author": "Manoj Joshi", "rating": 5, "date": "9 Jun 2026",
             "text": "Extremely satisfied. Water quality is excellent, touch dispensing feature is very convenient, and the purifier looks premium in my kitchen. Installation was smooth and neat."},
            {"author": "bondili mahender singh", "rating": 5, "date": "4 Jun 2026",
             "text": "Product quality is excellent and water tastes clean and fresh. Smart app lets me track consumption, monitor filter health and check performance in real time."},
            {"author": "Gen reviews", "rating": 4, "date": "30 May 2026",
             "text": "Good water purifier with useful features. Includes a pre-filter. Only downside: food-grade plastic tank instead of stainless steel at this price point."},
        ],
    },
    {
        "id": "lockpro", "name": "Native Lock Pro", "category": "lock",
        "rating": 4.6, "review_count": 562, "reviews_note": None,
        "monthly_buys": "50+", "price": 16999, "price_display": "₹16,999",
        "status": "in-stock", "status_label": "In Stock",
        "url": "https://www.amazon.in/Urban-Company-Native-Smart-Lock/dp/B0DJH6Q2XQ",
        "stars": {5: 84, 4: 7, 3: 1, 2: 2, 1: 6},
        "ai_summary": (
            "Customers find this smart lock to be of excellent quality, with professional installation "
            "and reliable performance. They appreciate its sleek appearance, ease of use with a good app "
            "interface, and consider it a great value. They like the features, highlighting the multiple "
            "access options for self and family, and the password masking functionality."
        ),
        "sentiment_tags": [
            ("Quality", 108), ("Installation", 63), ("Reliability", 37),
            ("Appearance", 22), ("Service", 17), ("Ease of use", 15),
        ],
        "reviews": [
            {"author": "chandran", "rating": 5, "date": "7 Jun 2026",
             "text": "The Lock Pro is a perfect solution for the front door. Very competent installation. Very easy to use, yet quite safe. Met our requirement to the full."},
            {"author": "Amazon Customer", "rating": 5, "date": "8 Jun 2026",
             "text": "Very good lock."},
            {"author": "Vishal Pandey", "rating": 5, "date": "3 Jun 2026",
             "text": "Awesome lock, good features. Good connectivity and durable. Neatly setup by the technician."},
            {"author": "Raizada vageesh", "rating": 4, "date": "30 May 2026",
             "text": "Good product, value for money. Fingerprint reader working well. Just wish the handles were heavier. Installation was great and the colour looks good too."},
        ],
    },
    {
        "id": "lockultra", "name": "Native Lock Ultra", "category": "lock",
        "rating": 5.0, "review_count": 7, "reviews_note": None,
        "monthly_buys": None, "price": None, "price_display": "Currently Unavailable",
        "status": "out-of-stock", "status_label": "Unavailable",
        "url": "https://www.amazon.in/Native-Lock-Ultra-Urban-Company/dp/B0H2MVF2L2",
        "stars": {5: 100, 4: 0, 3: 0, 2: 0, 1: 0},
        "ai_summary": None,
        "sentiment_tags": [],
        "reviews": [
            {"author": "Ayesha Tabassum", "rating": 5, "date": "14 Jun 2026",
             "text": "As sturdy as it gets with 5 bolts. Looks good, very sleek and futuristic. Company services are good. App integration is smooth and UI is good. Bonus point for the face unlock."},
            {"author": "Hamaad malik", "rating": 5, "date": "12 Jun 2026",
             "text": "A little skeptical on buying as it is slightly pricey, but after installation it is really worth it. Panels, material and overall build quality is very premium."},
            {"author": "Sita Ram", "rating": 5, "date": "11 Jun 2026",
             "text": "Good product. Looks very nice and sleek. Go for it if you like design and reliability."},
            {"author": "MAYANK", "rating": 5, "date": "13 May 2026",
             "text": "Top of the line product. Face ID is seamless, works even in complete darkness. Live video feature is very useful. Installation done within 2 hours."},
        ],
    },
]


# ── Helpers ──────────────────────────────────────────────────────────────────
def star_str(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def fmt_num(n):
    if n >= 1000:
        v = n / 1000
        return f"{v:.1f}K".replace(".0K", "K")
    return str(n)


def render_star_bars(stars: dict):
    fig = go.Figure()
    for star in [5, 4, 3, 2, 1]:
        pct = stars.get(star, 0)
        color = "#ff3b30" if star <= 2 else "#ff9500"
        fig.add_trace(go.Bar(
            x=[pct], y=[f"{star}★"],
            orientation="h",
            marker_color=color,
            text=[f"{pct}%"],
            textposition="outside",
            hovertemplate=f"{star}★: {pct}%<extra></extra>",
        ))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=40, t=0, b=0),
        height=130,
        xaxis=dict(range=[0, 115], visible=False),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.25,
    )
    return fig


def render_product_card(p):
    cat_emoji = "💧" if p["category"] == "purifier" else "🔒"
    cat_label = "Water Purifier" if p["category"] == "purifier" else "Smart Lock"
    cat_color = "badge-purifier" if p["category"] == "purifier" else "badge-lock"
    stock_color = "badge-instock" if p["status"] == "in-stock" else "badge-unavail"

    with st.container(border=True):
        # Header row
        col_title, col_stock = st.columns([4, 1])
        with col_title:
            st.markdown(f"**{p['name']}**")
            st.markdown(
                f'<span class="badge {cat_color}">{cat_emoji} {cat_label}</span>',
                unsafe_allow_html=True,
            )
        with col_stock:
            st.markdown(
                f'<div style="text-align:right"><span class="badge {stock_color}">{p["status_label"]}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Rating row
        col_num, col_meta, col_buys = st.columns([1, 3, 2])
        with col_num:
            st.markdown(f'<div class="big-rating">{p["rating"]:.1f}</div>', unsafe_allow_html=True)
        with col_meta:
            st.markdown(f'<div class="stars">{star_str(p["rating"])}</div>', unsafe_allow_html=True)
            note = f" {p['reviews_note']}" if p["reviews_note"] else ""
            st.caption(f'{fmt_num(p["review_count"])} reviews{note}')
        with col_buys:
            if p["monthly_buys"]:
                st.metric(label="This month", value=p["monthly_buys"])

        # Price row
        col_price, col_link = st.columns([2, 2])
        with col_price:
            st.markdown(f"### {p['price_display']}")
            st.caption("incl. GST")
        with col_link:
            st.markdown(
                f'<div style="padding-top:14px"><a href="{p["url"]}" target="_blank" '
                f'style="color:#ff6900;font-weight:600;text-decoration:none;">View on Amazon ↗</a></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Star breakdown chart
        st.markdown('<div class="section-label">Rating Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(render_star_bars(p["stars"]), use_container_width=True, config={"displayModeBar": False})

        # AI Summary
        st.markdown('<div class="section-label">🤖 AI Amazon Customer Summary</div>', unsafe_allow_html=True)
        if p["ai_summary"]:
            st.markdown(f'<div class="ai-box">{p["ai_summary"]}</div>', unsafe_allow_html=True)
            if p["sentiment_tags"]:
                tags_html = " ".join(
                    f'<span class="tag"><b>{label}</b> {count}</span>'
                    for label, count in p["sentiment_tags"]
                )
                st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.caption("Not enough reviews yet for an AI summary.")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Recent reviews
        st.markdown('<div class="section-label">Recent Reviews</div>', unsafe_allow_html=True)
        show_all = st.toggle("Show all reviews", key=f"toggle_{p['id']}")
        reviews_to_show = p["reviews"] if show_all else p["reviews"][:2]
        for r in reviews_to_show:
            stars_display = "★" * r["rating"] + "☆" * (5 - r["rating"])
            st.markdown(
                f'<div class="review-box">'
                f'<div><span class="review-author">{r["author"]}</span>'
                f' &nbsp;<span class="review-date">{r["date"]}</span></div>'
                f'<div style="color:#ff9500;font-size:0.8rem">{stars_display}</div>'
                f'<div class="review-text">{r["text"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Page layout ──────────────────────────────────────────────────────────────

# Header
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

# ── Filters + Sort ───────────────────────────────────────────────────────────
col_filter, col_sort = st.columns([3, 1])
with col_filter:
    category = st.radio(
        "Category",
        options=["All Products", "💧 Water Purifiers", "🔒 Smart Locks"],
        horizontal=True,
        label_visibility="collapsed",
    )
with col_sort:
    sort_by = st.selectbox(
        "Sort by",
        options=["Default", "Rating: High → Low", "Most Reviews", "Price: Low → High", "Price: High → Low"],
        label_visibility="collapsed",
    )

# Apply filter
cat_map = {"All Products": None, "💧 Water Purifiers": "purifier", "🔒 Smart Locks": "lock"}
selected_cat = cat_map[category]
products = [p for p in PRODUCTS if selected_cat is None or p["category"] == selected_cat]

# Apply sort
if sort_by == "Rating: High → Low":
    products = sorted(products, key=lambda p: p["rating"], reverse=True)
elif sort_by == "Most Reviews":
    products = sorted(products, key=lambda p: p["review_count"], reverse=True)
elif sort_by == "Price: Low → High":
    products = sorted(products, key=lambda p: p["price"] or float("inf"))
elif sort_by == "Price: High → Low":
    products = sorted(products, key=lambda p: p["price"] or 0, reverse=True)

# ── Summary bar ──────────────────────────────────────────────────────────────
avg_rating = sum(p["rating"] for p in products) / len(products) if products else 0
# Don't double-count M1 + M1 Pro shared listing
unique_review_counts = sum(
    p["review_count"] for p in products if not p["reviews_note"]
)
in_stock_count = sum(1 for p in products if p["status"] != "out-of-stock")
top_product = max(products, key=lambda p: p["rating"]) if products else None

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Products Shown", len(products))
m2.metric("Avg Rating", f"{avg_rating:.2f} ★")
m3.metric("Total Reviews", fmt_num(unique_review_counts))
m4.metric("In Stock", f"{in_stock_count}/{len(products)}")
m5.metric("Highest Rated", top_product["name"] if top_product else "—")

st.divider()

# ── Product grid (2 columns) ─────────────────────────────────────────────────
if not products:
    st.info("No products match this filter.")
else:
    cols = st.columns(2, gap="medium")
    for i, product in enumerate(products):
        with cols[i % 2]:
            render_product_card(product)
