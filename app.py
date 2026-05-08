import streamlit as st
from utils.player import init_db, get_player, add_xp
from utils.quests import add_quest, get_quests, complete_quest

st.set_page_config(page_title="ShadowForge", page_icon="⚔️", layout="wide")

# Dark Anime Theme
st.markdown("""
<style>
    .main {background-color: #0a0f1c; color: #e0e7ff;}
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white; 
        border-radius: 12px;
        font-weight: bold;
    }
    h1 {color: #a5b4fc; text-shadow: 0 0 20px #6366f1;}
    .avatar {border-radius: 50%; border: 5px solid #6366f1; box-shadow: 0 0 30px #4f46e5;}
</style>
""", unsafe_allow_html=True)

init_db()
player = get_player()
name, level, xp, streak = player[1], player[2], player[3], player[4]

# Rank Titles
ranks = {
    1: "Novice Shadow", 5: "Awakened Hunter", 10: "Elite Shadow",
    15: "Monarch Candidate", 20: "Shadow Monarch"
}
current_rank = ranks.get(level, "Shadow Sovereign")

# Sidebar - Character Customization
with st.sidebar:
    st.header("⚔️ Character")
    uploaded_file = st.file_uploader("Upload your avatar", type=["png", "jpg", "jpeg"])
    
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

# Main Header
col1, col2 = st.columns([1, 4])
with col1:
    if uploaded_file:
        st.image(uploaded_file, width=150)
    else:
        st.markdown(f'<img src="{avatar_url}" width="150" class="avatar">', unsafe_allow_html=True)

with col2:
    st.title("ShadowForge")
    st.markdown(f"**{name}** — *{current_rank}*")
    st.caption("Solo Leveling Inspired Study System")

# Progress Bar
st.progress(xp % 100 / 100)
st.write(f"**Level {level}** | **XP: {xp}** | 🔥 **{streak} Day Streak**")

tab1, tab2, tab3, tab4 = st.tabs(["🗡️ Dashboard", "📜 Quest Board", "⏳ Focus Mode", "🏆 Achievements"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Level", level)
    with col2: st.metric("Total XP", xp)
    with col3: st.metric("Streak", f"{streak} 🔥")

with tab2:
    st.subheader("Quest Board")
    with st.form("new_quest"):
        title = st.text_input("Quest Title", placeholder="Complete Chapter 5 - Integration")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        if st.form_submit_button("Accept Quest"):
            add_quest(title, difficulty)
            st.success("New Quest Added!")

    st.subheader("Active Quests")
    quests = get_quests()
    for q in quests:
        if q[4] == 0:  # Not completed
            col1, col2 = st.columns([4,1])
            with col1:
                st.write(f"**{q[1]}** — `{q[2]}`")
            with col2:
                if st.button("Complete", key=f"c_{q[0]}"):
                    xp_gained = complete_quest(q[0])
                    add_xp(xp_gained)
                    st.success(f"+{xp_gained} XP Gained! ⚡")
                    st.rerun()

with tab3:
    st.subheader("⚡ Focus Mode")
    minutes = st.slider("Focus Duration", 15, 90, 45)
    if st.button("Start Focus Session", type="primary"):
        st.success(f"Focus Session Started for {minutes} minutes. Become stronger!")
        st.balloons()

with tab4:
    st.subheader("Achievements")
    ach = [
        ("First Awakening", "Reach Level 2", "🔥"),
        ("Hunter's Consistency", "7 Day Streak", "🏆"),
        ("Shadow Grind", "Complete 10 Quests", "⚔️")
    ]
    for title, desc, emoji in ach:
        st.write(f"{emoji} **{title}** — {desc}")

st.caption("Keep leveling up. You are the main character.")
