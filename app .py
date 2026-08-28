import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import plotly.express as px
import plotly.graph_objects as go

# ----------------------
# APP CONFIG & PAGE SETUP
# ----------------------
st.set_page_config(
    page_title="Student Career Path Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Developer Profile
DEV_GITHUB = "https://github.com/coderravi0101"
DEV_NAME = "Ravi Kumar Singh"

# ----------------------
# ADVANCED CUSTOM CSS FOR PREMIUM UI/UX
# ----------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Modern Glassmorphic Container */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #311042 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 30px -10px rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.12);
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.15rem;
        font-weight: 400;
        max-width: 800px;
        margin-bottom: 1.2rem;
    }
    
    .github-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 6px 14px;
        border-radius: 999px;
        color: #F8FAFC !important;
        text-decoration: none !important;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.25s ease;
    }
    
    .github-pill:hover {
        background: rgba(255, 255, 255, 0.22);
        border-color: #818CF8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(129, 140, 248, 0.3);
    }
    
    /* Interactive Track Cards */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.25rem;
        margin-top: 1rem;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: #6366F1;
        box-shadow: 0 15px 30px -10px rgba(99, 102, 241, 0.3);
        background: rgba(30, 41, 59, 0.85);
    }
    
    .card-icon {
        font-size: 2.2rem;
        margin-bottom: 0.75rem;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }
    
    .card-desc {
        color: #94A3B8;
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.2);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }

    /* Score Indicator Metrics */
    .stat-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #38BDF8;
    }
    
    .stat-label {
        color: #94A3B8;
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    
    /* Custom Streamlit Sliders & Inputs */
    .stSlider > div > div > div {
        background-color: #6366F1 !important;
    }
    
    /* Footer Styling */
    .dev-footer {
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        color: #94A3B8;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------
# GLOBALS / CAREER TRACK DEFINITIONS
# ----------------------

TRACKS = {
    "Data Science / ML": [
        "You enjoy math and statistics.",
        "You like working with data, patterns, and predictions.",
        "You are comfortable with Python and libraries like Pandas, NumPy."
    ],
    "Web Development": [
        "You enjoy building websites and user interfaces.",
        "You like HTML/CSS/JavaScript and frameworks like React or Django.",
        "You care about design and user experience."
    ],
    "App Development": [
        "You like building Android/iOS apps.",
        "You enjoy working with mobile tools like Flutter / React Native / Android Studio.",
        "You care about performance and mobile UX."
    ],
    "AI / Computer Vision": [
        "You are interested in images, videos, and visual data.",
        "You like working with models for detection, classification, etc.",
        "You are comfortable experimenting with deep learning libraries."
    ]
}

# Maximum potential scores for normalized match percentage computation
MAX_TRACK_SCORES = {
    "Data Science / ML": 35,      # Q1*2(10) + Q4*2(10) + Q6*2(10) + Q8*1(5) = 35
    "Web Development": 30,        # Q2*2(10) + Q6*1(5) + Q7*2(10) + Q8*1(5) = 30
    "App Development": 15,        # Q3*2(10) + Q8*1(5) = 15
    "AI / Computer Vision": 25    # Q1*1(5) + Q5*2(10) + Q6*1(5) + Q8*1(5) = 25
}

TRACK_METADATA = {
    "Data Science / ML": {
        "icon": "📊",
        "tagline": "Discover patterns in data and build predictive machine learning models.",
        "description": "Data Scientists analyze complex datasets using mathematical models, statistical inference, and machine learning techniques to automate decision making.",
        "key_skills": ["Python", "Pandas & NumPy", "Scikit-Learn", "SQL & Relational DBs", "Statistics & Probability", "Matplotlib / Seaborn"],
        "top_roles": ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "Analytics Engineer"],
        "demand_index": "Wow Very High (94%)",
        "avg_salary": "$115,000 - $160,000 / yr",
        "sample_projects": [
            "Customer Churn Prediction Model",
            "Real-time E-commerce Sales Analytics Dashboard",
            "Automated Stock Price Forecasting"
        ],
        "color": "#3B82F6"
    },
    "Web Development": {
        "icon": "🌐",
        "tagline": "Architect modern interactive web applications and scalable backends.",
        "description": "Web Developers construct responsive frontend interfaces, RESTful APIs, and scalable back-end server infrastructure for modern web apps.",
        "key_skills": ["HTML5 / CSS3", "JavaScript & TypeScript", "React / Next.js", "Node.js / Express or Django", "REST & GraphQL APIs", "Git & CI/CD"],
        "top_roles": ["Frontend Developer", "Full Stack Engineer", "Backend Developer", "UI/UX Web Engineer"],
        "demand_index": "⚡ High (90%)",
        "avg_salary": "$95,000 - $145,000 / yr",
        "sample_projects": [
            "Full-Stack E-commerce Marketplace",
            "Real-time Collaborative Whiteboard",
            "Personal Portfolio & Blog CMS"
        ],
        "color": "#10B981"
    },
    "App Development": {
        "icon": "📱",
        "tagline": "Create sleek, high-performance mobile apps for iOS and Android.",
        "description": "Mobile App Developers craft native or cross-platform mobile experiences with fluid touch interactions, device API integrations, and offline capabilities.",
        "key_skills": ["Flutter & Dart", "React Native", "Kotlin (Android) / Swift (iOS)", "Mobile UI/UX Design", "Firebase / Supabase", "State Management (Bloc/Redux)"],
        "top_roles": ["Mobile App Developer", "iOS Engineer", "Android Engineer", "Cross-Platform Architect"],
        "demand_index": "📱 Strong (86%)",
        "avg_salary": "$100,000 - $150,000 / yr",
        "sample_projects": [
            "Cross-Platform Habit & Fitness Tracker",
            "Local Offline Recipe & Grocery List App",
            "Audio Streaming & Podcast Player"
        ],
        "color": "#8B5CF6"
    },
    "AI / Computer Vision": {
        "icon": "👁️",
        "tagline": "Enable machines to perceive, analyze, and interpret visual data.",
        "description": "Computer Vision Engineers train deep neural networks to process visual media like video streams and images for recognition, tracking, and spatial understanding.",
        "key_skills": ["PyTorch / TensorFlow", "OpenCV", "Convolutional Neural Networks (CNNs)", "YOLO & Object Detection", "Image Segmentation", "CUDA GPU Computing"],
        "top_roles": ["Computer Vision Engineer", "AI Research Scientist", "Deep Learning Engineer", "Autonomous Perception Dev"],
        "demand_index": " Exponential (96%)",
        "avg_salary": "$125,000 - $180,000 / yr",
        "sample_projects": [
            "Real-time Object Detection & Counter",
            "Facial Emotion & Gesture Recognizer",
            "Medical X-Ray Anomaly Classifier"
        ],
        "color": "#EC4899"
    }
}

# ----------------------
# HELPER FUNCTIONS
# ----------------------

def compute_scores(answers):
    """
    answers: dict of question_id -> int (1-5)
    Returns: dict of track -> score
    Rule-based scoring mechanism.
    """
    scores = {
        "Data Science / ML": 0,
        "Web Development": 0,
        "App Development": 0,
        "AI / Computer Vision": 0
    }

    # Q1: Interest in math & statistics
    scores["Data Science / ML"] += answers["q1"] * 2
    scores["AI / Computer Vision"] += answers["q1"] * 1

    # Q2: Interest in building websites
    scores["Web Development"] += answers["q2"] * 2

    # Q3: Interest in mobile apps
    scores["App Development"] += answers["q3"] * 2

    # Q4: Interest in working with data
    scores["Data Science / ML"] += answers["q4"] * 2

    # Q5: Interest in AI / Computer Vision
    scores["AI / Computer Vision"] += answers["q5"] * 2

    # Q6: Comfort with Python
    scores["Data Science / ML"] += answers["q6"] * 2
    scores["AI / Computer Vision"] += answers["q6"] * 1
    scores["Web Development"] += answers["q6"] * 1

    # Q7: Comfort with frontend (HTML/CSS/JS)
    scores["Web Development"] += answers["q7"] * 2

    # Q8: Time you can spend learning (motivation)
    scores["Data Science / ML"] += answers["q8"]
    scores["Web Development"] += answers["q8"]
    scores["App Development"] += answers["q8"]
    scores["AI / Computer Vision"] += answers["q8"]

    return scores

def get_recommended_track(scores):
    return max(scores, key=scores.get)

def compute_match_percentage(scores):
    """Computes normalized percentage match per track."""
    percentages = {}
    for track, score in scores.items():
        max_possible = MAX_TRACK_SCORES.get(track, 30)
        perc = min(100, int((score / max_possible) * 100))
        percentages[track] = perc
    return percentages

# ----------------------
# SESSION STATE INITIALIZATION
# ----------------------

if "answers" not in st.session_state:
    st.session_state.answers = None

if "user_meta" not in st.session_state:
    st.session_state.user_meta = None

# ----------------------
# SIDEBAR NAVIGATION & DEV PROFILE
# ----------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/graduation-cap.png", width=70)
    st.title("Navigation")
    
    page = st.radio(
        "Select Page",
        ("Home", "Questionnaire", "Results & Insights"),
        index=0
    )
    
    st.markdown("---")
    
    # Developer Section in Sidebar
    st.markdown("### 👨‍💻 Developer Profile")
    st.markdown(f"**{DEV_NAME}**")
    st.markdown(
        f"""
        <a href="{DEV_GITHUB}" target="_blank" class="github-pill">
            <svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            Follow on GitHub
        </a>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")
    if st.session_state.answers is not None:
        if st.button("🔄 Reset Assessment", use_container_width=True):
            st.session_state.answers = None
            st.session_state.user_meta = None
            st.rerun()

# ----------------------
# PAGE 1: HOME
# ----------------------
if page == "Home":
    # Hero Banner
    st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-title">🎓 Student Career Path Recommender</div>
            <div class="hero-subtitle">
                An intelligent rule-based career guidance platform designed to match your skills, coding preferences, and technical curiosity with high-impact engineering specializations.
            </div>
            <a href="{DEV_GITHUB}" target="_blank" class="github-pill">
                ⭐ Star on GitHub (Ravi)
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Highlights Grid
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">4</div>
            <div class="stat-label">Specialized Tracks</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">8</div>
            <div class="stat-label">Assessment Dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">100%</div>
            <div class="stat-label">Personalized Roadmap</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.markdown("### 🚀 How It Works")
        st.markdown(
            """
            1. 📝 **Take the Questionnaire**: Complete 8 quick slider questions evaluating your comfort with math, coding, web/mobile development, and AI concepts.
            2. ⚙️ **Smart Score Computation**: The app calculates weighted score metrics and normalized match percentages across all four tracks.
            3. 📊 **View Insights & Roadmaps**: Get a detailed breakdown featuring radar charts, top career roles, core skills to master, starter projects, and a step-by-step roadmap.
            4. 📥 **Export Results**: Download your personalized evaluation report as JSON or CSV to save your trajectory.
            """
        )

        st.markdown("### 🏁 Ready to discover your path?")
        st.info("Navigate to the **Questionnaire** tab from the sidebar to begin your 2-minute assessment.")

    with col_right:
        st.markdown("### 🌟 Career Tracks Overview")
        search_filter = st.text_input("🔍 Filter tracks", "", placeholder="Search skills, topics, roles...")
        
        for track_name, meta in TRACK_METADATA.items():
            if search_filter.lower() in track_name.lower() or search_filter.lower() in meta["description"].lower() or any(search_filter.lower() in s.lower() for s in meta["key_skills"]):
                with st.expander(f"{meta['icon']} **{track_name}** — *{meta['demand_index']}*", expanded=False):
                    st.write(meta["description"])
                    st.markdown(f"**Est. Salary:** `{meta['avg_salary']}`")
                    st.markdown("**Key Skills:** " + ", ".join([f"`{s}`" for s in meta["key_skills"]]))

# ----------------------
# PAGE 2: QUESTIONNAIRE
# ----------------------
elif page == "Questionnaire":
    st.markdown(f"""
        <div class="hero-banner" style="padding: 1.8rem 2.2rem;">
            <div class="hero-title" style="font-size: 2rem;">📝 Student Self-Assessment Questionnaire</div>
            <div class="hero-subtitle">
                Rate your agreement with each statement honestly on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree).
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("career_form"):
        st.markdown("#### 👤 Student Information")
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            name = st.text_input("Your Name (optional)", placeholder="e.g. Alex Smith")
        with col_meta2:
            year = st.selectbox(
                "Current Academic Level",
                ["School Student", "Diploma Student", "B.Tech / B.E. 1st Year", "B.Tech / B.E. 2nd Year", "B.Tech / B.E. 3rd Year", "B.Tech / B.E. 4th Year", "Other / Professional"]
            )

        st.markdown("---")
        st.markdown("#### 🎯 Technical Interests & Coding Comfort")

        col_q1, col_q2 = st.columns(2)

        with col_q1:
            st.markdown("##### 🧮 Math & Data")
            q1 = st.slider("Q1. I enjoy math, probability, and statistics.", 1, 5, 3)
            q4 = st.slider("Q4. I like working with data (CSV files, tables, data analysis).", 1, 5, 3)
            
            st.markdown("##### 💻 Web & Frontend")
            q2 = st.slider("Q2. I am interested in building websites and web apps.", 1, 5, 3)
            q7 = st.slider("Q7. I feel comfortable with HTML/CSS/JavaScript.", 1, 5, 3)

        with col_q2:
            st.markdown("##### 📱 Mobile & Computer Vision")
            q3 = st.slider("Q3. I am interested in building mobile apps (Android / iOS).", 1, 5, 3)
            q5 = st.slider("Q5. I am interested in AI, images & videos (Computer Vision).", 1, 5, 3)
            
            st.markdown("##### 🐍 Programming & Time Commitment")
            q6 = st.slider("Q6. I feel comfortable writing basic Python code.", 1, 5, 3)
            q8 = st.slider("Q8. I can spend at least 5–7 hours per week learning tech skills.", 1, 5, 3)

        st.markdown(" ")
        submitted = st.form_submit_button("🚀 Submit & Calculate Recommendation", use_container_width=True)

    if submitted:
        answers = {
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "q4": q4,
            "q5": q5,
            "q6": q6,
            "q7": q7,
            "q8": q8
        }
        st.session_state.answers = answers
        st.session_state.user_meta = {
            "name": name,
            "year": year,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.success("🎉 Assessment submitted successfully! Redirecting to your results...")
        st.balloons()

# ----------------------
# PAGE 3: RESULTS & INSIGHTS
# ----------------------
elif page == "Results & Insights":
    st.markdown(f"""
        <div class="hero-banner" style="padding: 1.8rem 2.2rem;">
            <div class="hero-title" style="font-size: 2rem;">📊 Assessment Results & Career Insights</div>
            <div class="hero-subtitle">
                Explore your match breakdown, track comparisons, skills checklist, and customized learning roadmap.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.answers is None:
        st.warning("⚠️ No assessment data found. Please complete the questionnaire first.")
        st.info("Use the sidebar or click below to fill out the questionnaire.")
    else:
        answers = st.session_state.answers
        scores = compute_scores(answers)
        match_percentages = compute_match_percentage(scores)
        recommended_track = get_recommended_track(scores)
        rec_meta = TRACK_METADATA.get(recommended_track, TRACK_METADATA["Data Science / ML"])

        # Candidate Header Summary
        meta = st.session_state.user_meta or {"name": "Anonymous", "year": "Not specified", "timestamp": "N/A"}
        
        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        with c_m1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number" style="font-size: 1.3rem;">👤 {meta['name'] if meta['name'] else 'Student'}</div>
                <div class="stat-label">Candidate</div>
            </div>
            """, unsafe_allow_html=True)
        with c_m2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number" style="font-size: 1.1rem; color: #A855F7;">{meta['year']}</div>
                <div class="stat-label">Academic Level</div>
            </div>
            """, unsafe_allow_html=True)
        with c_m3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number" style="font-size: 1.3rem; color: #10B981;">{match_percentages[recommended_track]}% Match</div>
                <div class="stat-label">Top Track Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        with c_m4:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number" style="font-size: 1rem; color: #94A3B8;">{meta['timestamp']}</div>
                <div class="stat-label">Timestamp</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Top Recommended Track Banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%); padding: 1.8rem; border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.4); margin-bottom: 2rem;">
            <div style="font-size: 0.9rem; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em;">🎯 Primary Recommendation</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{rec_meta['icon']} {recommended_track}</div>
            <div style="font-size: 1.05rem; color: #CBD5E1; margin-bottom: 0.8rem;">{rec_meta['tagline']}</div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border-color: rgba(16, 185, 129, 0.4);">Demand: {rec_meta['demand_index']}</span>
                <span class="badge" style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; border-color: rgba(59, 130, 246, 0.4);">Est. Salary: {rec_meta['avg_salary']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Visual Score Analysis Section
        st.markdown("### 📈 Track Scores & Match Percentages")
        
        col_vis1, col_vis2 = st.columns([1.1, 0.9])

        score_df = pd.DataFrame({
            "Track": list(scores.keys()),
            "Score": list(scores.values()),
            "Match Percentage (%)": [match_percentages[t] for t in scores.keys()]
        }).sort_values("Score", ascending=True)

        with col_vis1:
            st.markdown("#### Horizontal Match Comparison")
            fig_bar = px.bar(
                score_df,
                x="Match Percentage (%)",
                y="Track",
                orientation="h",
                text="Match Percentage (%)",
                color="Match Percentage (%)",
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1"),
                xaxis=dict(range=[0, 105], showgrid=False),
                yaxis=dict(showgrid=False),
                margin=dict(l=10, r=20, t=10, b=10),
                coloraxis_showscale=False
            )
            fig_bar.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_vis2:
            st.markdown("#### Skills & Interests Radar Profile")
            categories = list(scores.keys())
            values = list(scores.values())
            categories.append(categories[0])
            values.append(values[0])

            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                fillcolor='rgba(99, 102, 241, 0.35)',
                line=dict(color='#818CF8', width=3)
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(scores.values()) + 6], gridcolor="rgba(255,255,255,0.1)")
                ),
                showlegend=False,
                margin=dict(l=40, r=40, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1")
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("---")

        # Deep Dive: Why this Track & Skill Requirements
        st.markdown("### 💡 Comprehensive Career Breakdown")
        
        c_dd1, c_dd2 = st.columns(2)

        with c_dd1:
            st.markdown("#### 🎯 Why This Track Fits You")
            reasons = TRACKS.get(recommended_track, [])
            for r in reasons:
                st.markdown(f"✔ **{r}**")

            st.markdown("#### 👔 Potential Job Titles")
            for role in rec_meta["top_roles"]:
                st.markdown(f"💼 `{role}`")

        with c_dd2:
            st.markdown("#### 🛠️ Essential Skills Checklist")
            for skill in rec_meta["key_skills"]:
                st.checkbox(f"Master {skill}", value=False, key=f"skill_{skill}")

            st.markdown("#### 🚀 Recommended Starter Projects")
            for proj in rec_meta["sample_projects"]:
                st.markdown(f"📌 *{proj}*")

        st.markdown("---")

        # Step-by-Step Learning Roadmap
        st.markdown("### 🗺️ Step-by-Step Action Roadmap")

        if recommended_track == "Data Science / ML":
            roadmap_steps = [
                ("Phase 1: Python Mastery", "Learn functions, OOP, data structures, and virtual environments."),
                ("Phase 2: Data Wrangling & Viz", "Master NumPy, Pandas, Matplotlib, and Seaborn for dataset manipulation."),
                ("Phase 3: Machine Learning Core", "Understand linear regression, decision trees, random forests, and scikit-learn."),
                ("Phase 4: Capstone Projects", "Build end-to-end predictive web dashboards with Streamlit and deploy model APIs."),
                ("Phase 5: Deep Learning Prep", "Explore PyTorch/TensorFlow fundamentals and neural network architectures.")
            ]
        elif recommended_track == "Web Development":
            roadmap_steps = [
                ("Phase 1: Web Foundations", "Master HTML5 semantics, modern CSS Flexbox/Grid, and ES6+ JavaScript."),
                ("Phase 2: Responsive Frontend", "Build accessible static websites and web user interfaces."),
                ("Phase 3: Frontend Framework", "Learn React or Next.js alongside state management and API integration."),
                ("Phase 4: Backend Infrastructure", "Build REST APIs using Node.js/Express or Python/Django with PostgreSQL."),
                ("Phase 5: Deployment & DevOps", "Deploy full-stack apps to Vercel, Render, or Docker with CI/CD integration.")
            ]
        elif recommended_track == "App Development":
            roadmap_steps = [
                ("Phase 1: Framework Choice", "Choose Flutter (Dart) or React Native (TypeScript/JS) for cross-platform app dev."),
                ("Phase 2: Mobile UI & State", "Build responsive mobile screen layouts, navigation stacks, and state patterns."),
                ("Phase 3: Starter Projects", "Create offline-first mobile apps (Notes App, Task Manager, Calculator)."),
                ("Phase 4: Cloud & Backend Sync", "Connect apps to Firebase/Supabase for real-time auth, DB, and push notifications."),
                ("Phase 5: Publishing & QA", "Test on iOS Simulator/Android Emulator and publish to App Store / Google Play.")
            ]
        else:
            roadmap_steps = [
                ("Phase 1: Mathematics & Python", "Strengthen linear algebra, matrix calculus, Python, and PyTorch basics."),
                ("Phase 2: OpenCV Fundamentals", "Learn image processing, filtering, edge detection, and geometric transforms."),
                ("Phase 3: Deep Neural Networks", "Understand Convolutional Neural Networks (CNNs) for image classification."),
                ("Phase 4: Object Detection & Tracking", "Master YOLO, image segmentation, and video stream object detection."),
                ("Phase 5: Deployment & Edge AI", "Optimize models using TensorRT, ONNX, and OpenCV for real-time inference.")
            ]

        for title, desc in roadmap_steps:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.5); padding: 1rem 1.25rem; border-radius: 12px; border-left: 4px solid #6366F1; margin-bottom: 0.75rem;">
                <div style="font-weight: 700; color: #F8FAFC; font-size: 1.05rem;">{title}</div>
                <div style="color: #94A3B8; font-size: 0.92rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Developer Credit Card & Export Actions
        c_exp1, c_exp2 = st.columns([1.2, 0.8])

        with c_exp1:
            st.markdown("### 📥 Download & Save Report")
            st.write("Save your assessment results locally as JSON or CSV.")
            
            report_dict = {
                "candidate": meta['name'],
                "academic_level": meta['year'],
                "timestamp": meta['timestamp'],
                "recommended_track": recommended_track,
                "scores": scores,
                "match_percentages": match_percentages,
                "answers": answers
            }
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                st.download_button(
                    label="📄 Export JSON Report",
                    data=json.dumps(report_dict, indent=4),
                    file_name=f"career_report_{meta['name'] or 'student'}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with c_btn2:
                df_export = pd.DataFrame([report_dict])
                st.download_button(
                    label="📊 Export CSV Report",
                    data=df_export.to_csv(index=False),
                    file_name=f"career_report_{meta['name'] or 'student'}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        with c_exp2:
            st.markdown("### 👨‍💻 Connect with Developer")
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.9); padding: 1.25rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #F8FAFC;">{DEV_NAME}</div>
                <p style="color: #94A3B8; font-size: 0.88rem; margin: 6px 0 12px 0;">Open Source Developer & AI Explorer</p>
                <a href="{DEV_GITHUB}" target="_blank" class="github-pill" style="justify-content: center; width: 100%;">
                    <svg height="16" width="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                    Ravi
                </a>
            </div>
            """, unsafe_allow_html=True)

# ----------------------

