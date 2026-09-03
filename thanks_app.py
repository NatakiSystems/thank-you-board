from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="IF'26 Thank You Jose & Alex! 🎓", page_icon="🎉", layout="wide"
)

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)


def load_notes():
    try:
        data = conn.read(ttl=5)
        return data.dropna(how="all")
    except Exception:
        return pd.DataFrame(
            columns=[
                "Timestamp",
                "Instructor",
                "Sender",
                "Location",
                "Superpower",
                "Message",
            ]
        )


# Celebration trigger on rerun
if st.session_state.get("show_celebration", False):
    st.balloons()
    st.toast("🎉 Your celebration note is live on the wall!", icon="🎈")
    st.session_state["show_celebration"] = False

# UI Styling
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    .block-container {
        max-width: 1080px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 3rem !important;
        padding-left: clamp(1rem, 4vw, 2.5rem) !important;
        padding-right: clamp(1rem, 4vw, 2.5rem) !important;
        margin: 0 auto !important;
    }

    @media print {
        header, footer, .stButton, .stForm, [data-testid="stSidebar"], .no-print {
            display: none !important;
        }
        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
        }
        .thank-you-card {
            break-inside: avoid;
            box-shadow: none !important;
            border: 1.5px solid #cbd5e1 !important;
            margin-bottom: 16px !important;
            background: #ffffff !important;
        }
    }

    .hero-banner {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 35%, #8b5cf6 70%, #ec4899 100%);
        border-radius: clamp(18px, 3vw, 28px);
        padding: clamp(2rem, 5vw, 3.5rem) clamp(1.2rem, 4vw, 2.8rem);
        color: #ffffff;
        text-align: center;
        box-shadow: 0 16px 36px -10px rgba(99, 102, 241, 0.4);
        margin-bottom: 1.8rem;
    }

    .hero-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(10px);
        padding: 6px 18px;
        border-radius: 999px;
        font-size: clamp(0.78rem, 1.8vw, 0.92rem);
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    .hero-title {
        font-size: clamp(2.1rem, 5.5vw, 3.3rem);
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0 0 1rem 0;
        line-height: 1.15;
    }

    .hero-subtitle {
        font-size: clamp(1.05rem, 2.2vw, 1.25rem);
        font-weight: 400;
        line-height: 1.65;
        max-width: 820px;
        margin: 0 auto;
        text-align: center !important;
        color: rgba(255, 255, 255, 0.96);
    }

    .profile-card {
        border-radius: 18px;
        padding: clamp(1.2rem, 3vw, 1.6rem);
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 1rem;
    }

    .card-jose {
        border-top: 6px solid #f59e0b;
        background: linear-gradient(180deg, #fffdfa 0%, #ffffff 100%);
    }

    .card-alex {
        border-top: 6px solid #06b6d4;
        background: linear-gradient(180deg, #f7fdfe 0%, #ffffff 100%);
    }

    .role-badge {
        font-size: clamp(0.72rem, 1.6vw, 0.82rem);
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 5px 12px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 0.6rem;
        width: fit-content;
    }

    .badge-jose { background: #fef3c7; color: #92400e; }
    .badge-alex { background: #cffafe; color: #155e75; }

    .profile-name {
        font-size: clamp(1.35rem, 3vw, 1.65rem);
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 6px 0;
    }

    .profile-traits {
        font-size: clamp(0.88rem, 1.8vw, 0.98rem);
        color: #334155;
        line-height: 1.5;
        font-weight: 500;
    }

    .form-header {
        font-size: clamp(1.25rem, 2.5vw, 1.5rem);
        font-weight: 800;
        color: #0f172a;
        margin: 1.2rem 0 0.8rem 0;
    }

    .thank-you-card {
        background: #ffffff;
        border-radius: 18px;
        border: 1.5px solid #e2e8f0;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }

    .card-meta {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.9rem;
    }

    .tag-recipient {
        background: #e2e8f0;
        color: #0f172a;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 5px 12px;
        border-radius: 7px;
    }

    .tag-atl {
        background: #ffe4e6;
        color: #9f1239;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 5px 12px;
        border-radius: 7px;
    }

    .tag-la {
        background: #e0e7ff;
        color: #3730a3;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 5px 12px;
        border-radius: 7px;
    }

    .tag-superpower {
        background: #fef08a;
        color: #854d0e;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 5px 10px;
        border-radius: 7px;
    }

    .card-date {
        color: #64748b;
        font-size: 0.88rem;
        font-weight: 600;
        margin-left: auto;
    }

    .card-body-text {
        font-size: 1.12rem;
        line-height: 1.65;
        color: #0f172a;
        font-weight: 450;
        margin: 1rem 0;
        white-space: pre-wrap;
    }

    .card-author {
        text-align: right;
        font-weight: 700;
        font-size: 1.05rem;
        color: #1e293b;
    }

    .print-tip-box {
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        border-radius: 12px;
        padding: 0.85rem 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.95rem;
        color: #1e293b;
        font-weight: 500;
    }

    .key-badge {
        background: #e2e8f0;
        border: 1px solid #94a3b8;
        border-bottom-width: 2px;
        color: #0f172a;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 5px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Hero Banner
st.markdown(
    """
<div class="hero-banner">
    <div class="hero-tag">✨ IF'26 AI Business Solutions Engineering Cohort</div>
    <h1 class="hero-title">Thank You, Jose & Alex! 🎓 💻</h1>
    <p class="hero-subtitle">
        To two incredible educators who brought code, AI, and business solutions to life.<br>
        From late-night debugging breakthroughs to empowering capstone projects —<br>
        here is the love and gratitude from your Atlanta 🍑 and Los Angeles 🌴 fellows!
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Teacher Spotlight Cards
col_jose, col_alex = st.columns(2)
with col_jose:
    st.markdown(
        """
    <div class="profile-card card-jose">
        <span class="role-badge badge-jose">Lead Instructor • New York 🗽</span>
        <div class="profile-name">🗽 Jose</div>
        <div class="profile-traits">
            Architecture Guide • Code Mentor • Champion of Student Growth 🚀
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_alex:
    st.markdown(
        """
    <div class="profile-card card-alex">
        <span class="role-badge badge-alex">Teaching Assistant (TA) • Los Angeles 🌴</span>
        <div class="profile-name">🌴 Alex</div>
        <div class="profile-traits">
            Lab Support Hero • Debugging Expert • Patient Problem-Solver 💡
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Input Form
st.markdown(
    '<div class="form-header">💌 Add Your Note to the Celebration Board</div>',
    unsafe_allow_html=True,
)

with st.form("celebration_form", clear_on_submit=True):
    col_who, col_name, col_loc = st.columns([1.3, 1.4, 1.3])

    with col_who:
        instructor = st.selectbox(
            "Who are you celebrating? *",
            ["Both Jose & Alex 🌟", "Jose (Lead Instructor) 🗽", "Alex (TA) 🌴"],
        )
    with col_name:
        sender = st.text_input(
            "Your Name", placeholder="e.g., Maya Lin (or leave blank for Fellow)"
        )
    with col_loc:
        location = st.selectbox(
            "Fellow Cohort Location *",
            ["Atlanta Cohort 🍑", "Los Angeles Cohort 🌴", "Other / Remote 🌐"],
        )

    superpower = st.selectbox(
        "Superpower Highlight (pick a vibe that fits your note):",
        [
            "💡 Made complex AI and code click",
            "🐛 Late-night debugging lifesaver",
            "🌱 Endless patience and encouraging energy",
            "🎯 Practical business & career guidance",
            "☕ Inspiring, fun classroom atmosphere",
            "⭐ All of the above!",
        ],
    )

    message = st.text_area(
        "Your Message of Gratitude & Memories *",
        placeholder="Share a moment when Jose or Alex helped you overcome a blocker, an inspiring lecture, or well wishes for their future journeys...",
        height=130,
    )

    submitted = st.form_submit_button(
        "Post Celebration Note 🎉", use_container_width=True
    )

    if submitted:
        if message.strip():
            clean_instructor = (
                "Jose & Alex"
                if "Both" in instructor
                else "Jose"
                if "Jose" in instructor
                else "Alex"
            )
            existing_df = load_notes()
            new_entry = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime("%b %d, %Y"),
                        "Instructor": clean_instructor,
                        "Sender": sender.strip()
                        if sender.strip()
                        else "Grateful Fellow",
                        "Location": location,
                        "Superpower": superpower,
                        "Message": message.strip(),
                    }
                ]
            )

            updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
            conn.update(data=updated_df)

            st.session_state["show_celebration"] = True
            st.rerun()
        else:
            st.error("Please enter a note before submitting.")

st.divider()

# Reading Wall Display
df = load_notes()

col_wall_title, col_filter = st.columns([1.8, 1.2])
with col_wall_title:
    st.markdown("### 📖 The Wall of Gratitude")
with col_filter:
    filter_choice = st.selectbox(
        "Filter messages:",
        ["All Messages", "Jose & Alex", "Jose", "Alex"],
        label_visibility="collapsed",
    )

if not df.empty and len(df) > 0:
    if filter_choice != "All Messages":
        view_df = df[df["Instructor"] == filter_choice]
    else:
        view_df = df

    st.markdown(f"**Showing {len(view_df)} celebration note(s)**")

    if view_df.empty:
        st.info(f"No notes specifically for {filter_choice} yet.")
    else:
        for _, row in view_df.iloc[::-1].iterrows():
            loc_str = str(row.get("Location", ""))
            loc_badge = (
                '<span class="tag-atl">Atlanta 🍑</span>'
                if "Atlanta" in loc_str
                else '<span class="tag-la">Los Angeles 🌴</span>'
                if "Los Angeles" in loc_str
                else '<span class="tag-recipient">Remote 🌐</span>'
            )
            superpower_html = (
                f'<span class="tag-superpower">{row["Superpower"]}</span>'
                if pd.notna(row.get("Superpower")) and row.get("Superpower")
                else ""
            )

            card_html = (
                f'<div class="thank-you-card">'
                f'<div class="card-meta">'
                f'<span class="tag-recipient">To: {row["Instructor"]}</span>'
                f"{loc_badge}"
                f"{superpower_html}"
                f'<span class="card-date">{row["Timestamp"]}</span>'
                f"</div>"
                f'<div class="card-body-text">{row["Message"]}</div>'
                f'<div class="card-author">— {row["Sender"]}</div>'
                f"</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("---")
    col_down1, col_down2 = st.columns([1, 1.4])
    with col_down1:
        st.download_button(
            label="📥 Download All Messages (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="jose_and_alex_gratitude_notes.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_down2:
        st.markdown(
            """
        <div class="print-tip-box">
            <span>💡 <strong>Print Keepsake:</strong> Press <span class="key-badge">Cmd + P</span> or <span class="key-badge">Ctrl + P</span> to export as a formatted PDF book.</span>
        </div>
        """,
            unsafe_allow_html=True,
        )
else:
    st.info("No messages posted yet. Be the first to share your gratitude above!")