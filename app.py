 import streamlit as st
import time
from datetime import datetime
from utils.player import init_db, get_player, add_xp
from utils.quests import add_quest, get_quests, complete_quest

st.set_page_config(page_title="ShadowForge", page_icon="⚔️", layout="wide")

init_db()
player = get_player()
name, level, xp, streak = player[1], player[2], player[3], player[4]

# Rank System
ranks = {
    1: "Novice Shadow", 5: "Awakened Hunter", 10: "Elite Shadow",
    15: "Monarch Candidate", 20: "Shadow Monarch", 30: "Supreme Ruler"
}

# ====================== STRONG ANIME GAMING CSS ======================
st.markdown("""
<style>
    .main {background-color: #0a0a12; color: #e0e7ff;}
    h1 {color: #c4b5fd; text-shadow: 0 0 30px #7c3aed; font-size: 3.2rem;}
    
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #a855f7);
        color: white;
        border-radius: 12px;
        border: 2px solid #818cf8;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.08);
        box-shadow: 0 0 25px #a855f7;
    }
    
    .avatar {
        border-radius: 50%;
        border: 6px solid #6366f1;
        box-shadow: 0 0 40px #a855f7;
        transition: all 0.4s ease;
    }
    .avatar:hover {box-shadow: 0 0 50px #c026d3;}
    
    .quest-card {
        background: linear-gradient(145deg, #1e1b4b, #312e81);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #6366f1;
        transition: all 0.3s ease;
    }
    .quest-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 20px #818cf8;
    }
    
    .timer {
        font-size: 4.5rem;
        font-weight: bold;
        text-shadow: 0 0 30px #a855f7;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR - CHARACTER CUSTOMIZATION ======================
with st.sidebar:
    st.header("⚔️ Character")
    uploaded_file = st.file_uploader("Upload Avatar", type=["png", "jpg", "jpeg"])
    
    if not uploaded_file:
        default_avatars = {
            "Shadow Monarch": "https://i.imgur.com/5z9vL8R.png",
            "Dark Hunter": "https://i.imgur.com/8Y5zK2m.png",
            "Void Assassin": "https://i.imgur.com/JfPqL2x.png",
        }
        selected = st.selectbox("Choose Style", options=list(default_avatars.keys()))
        avatar_url = default_avatars[selected]
    else:
        avatar_url = None

# ====================== MAIN LAYOUT ======================
col_left, col_center, col_right = st.columns([2.2, 3.5, 2.2])

# ================= LEFT PANEL - CHARACTER =================
with col_left:
    st.markdown("### Your Character")
    if uploaded_file:
        st.image(uploaded_file, width=220)
    else:
        st.markdown(f'<img src="{avatar_url}" width="220" class="avatar">', unsafe_allow_html=True)
    
    st.markdown(f"### **{name}**")
    st.markdown(f"**{ranks.get(level, 'Shadow Sovereign')}**")
    
    st.progress(xp % 100 / 100)
    st.caption(f"Level {level} • XP: {xp} / {(level*100)}")
    
    st.metric("🔥 Current Streak", f"{streak} days")

# ================= CENTER PANEL - MAIN HUB =================
with col_center:
    st.title("SHADOWFORGE")
    st.caption("You are the protagonist. Keep ascending.")
    
    # Focus Mode
    st.subheader("⚡ Focus Mode")
    duration = st.select_slider("Session Duration", options=[25, 30, 45, 60, 90], value=45)
    
    if st.button("🚀 START FOCUS SESSION", type="primary", use_container_width=True):
        st.session_state.timer_running = True
        st.session_state.timer_end = time.time() + (duration * 60)
        st.rerun()

    # Active Timer
    if st.session_state.get("timer_running"):
        remaining = int(st.session_state.timer_end - time.time())
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            st.markdown(f"<div class='timer'>{mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
            time.sleep(0.5)
            st.rerun()
        else:
            st.success("🎉 Training Complete! You have become stronger.")
            add_xp(35)
            st.balloons()
            st.session_state.timer_running = False
            st.rerun()

    # Quests
    st.subheader("Active Quests")
    with st.form("new_quest"):
        title = st.text_input("Quest Title", placeholder="Defeat Calculus Chapter 7")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        if st.form_submit_button("Accept Quest"):
            add_quest(title, difficulty)
            st.success("Quest Accepted!")
            st.rerun()

    quests = get_quests()
    for q in quests:
        if q[4] == 0:
            with st.container():
                st.markdown('<div class="quest-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([4,1])
                with col1:
                    st.write(f"**{q[1]}**")
                    st.caption(f"{q[2]} • +{q[3]} XP")
                with col2:
                    if st.button("Complete", key=f"q_{q[0]}"):
                        xp_gained = complete_quest(q[0])
                        add_xp(xp_gained)
                        st.success(f"+{xp_gained} XP Gained!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT PANEL - ACHIEVEMENTS =================
with col_right:
    st.markdown("### 🏆 Achievements")
    achievements = [
        ("First Awakening", "Reached Level 2", "🔥"),
        ("Consistent Hunter", "7 Day Streak", "🏆"),
        ("Shadow Grinder", "10 Quests Completed", "⚔️"),
        ("Deep Focus", "Completed Focus Session", "🌑")
    ]
    for title, desc, emoji in achievements:
        st.markdown(f"""
        <div style="background:#1e1b4b; padding:12px; border-radius:12px; margin-bottom:10px; border:1px solid #6366f1;">
            <strong>{emoji} {title}</strong><br>
            <small>{desc}</small>
        </div>
        """, unsafe_allow_html=True)

st.caption("ShadowForge — You are the main character.")
