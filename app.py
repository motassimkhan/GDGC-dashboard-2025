import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="GDGC Study Jam Leaderboard",
    page_icon="🏆",
    layout="wide"
)

# Custom CSS for Google colors and styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #4285F4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .podium-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 20px;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .podium-block {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-width: 200px;
    }
    .podium-first {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        height: 250px;
    }
    .podium-second {
        background: linear-gradient(135deg, #C0C0C0, #A8A8A8);
        height: 200px;
    }
    .podium-third {
        background: linear-gradient(135deg, #CD7F32, #B8860B);
        height: 150px;
    }
    .podium-medal {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    .podium-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: white;
        margin: 10px 0;
    }
    .podium-badges {
        font-size: 1.5rem;
        color: white;
        font-weight: bold;
    }
    .stProgress > div > div > div {
        background-color: #4285F4;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('progress.csv')
    return df

try:
    df = load_data()
    
    # Main header
    st.markdown('<h1 class="main-header">🏆 GDGC Study Jam Leaderboard 🏆</h1>', unsafe_allow_html=True)
    
    # Statistics section at the top
    st.markdown("## 📈 Study Jam Statistics")
    
    total_participants = len(df)
    completed_all = len(df[df['# of Skill Badges Completed'] == 20])
    avg_badges = df['# of Skill Badges Completed'].mean()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Participants", total_participants)
    
    with col2:
        st.metric("Completed All Badges", completed_all)
    
    with col3:
        st.metric("Average Badges Completed", f"{avg_badges:.1f}")
    
    # Progress toward 100-person goal
    st.markdown("### 🎁 Progress Toward Swag Goal")
    st.markdown(f"**{completed_all}/100 people** have completed all 20 skill badges!")
    
    progress_to_goal = min((completed_all / 100) * 100, 100)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = completed_all,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "People Completed (Goal: 100)"},
        delta = {'reference': 100},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#4285F4"},
            'steps': [
                {'range': [0, 50], 'color': "#FBBC04"},
                {'range': [50, 75], 'color': "#34A853"},
                {'range': [75, 100], 'color': "#0F9D58"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    if completed_all >= 100:
        st.balloons()
        st.success("🎉 Goal achieved! Everyone gets swags! 🎁")
    else:
        st.info(f"💪 Keep going! We need {100 - completed_all} more people to complete all badges!")
    
    st.markdown("---")
    
    # Top 3 Podium using Streamlit components
    st.markdown("### 🎖️ Top 3 Champions")
    
    # Get top 3 from full dataset
    top3_df = df.sort_values(
        by=['# of Skill Badges Completed', '# of Arcade Games Completed'],
        ascending=False
    ).head(3)
    
    if len(top3_df) >= 3:
        # Create columns for podium (2nd, 1st, 3rd order)
        pod_col1, pod_col2, pod_col3 = st.columns(3)
        
        # 2nd Place (Left)
        with pod_col1:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            st.markdown("### 🥈 2nd Place")
            second = top3_df.iloc[1]
            st.metric("Name", second['User Name'])
            st.metric("Badges", f"{second['# of Skill Badges Completed']}/20")
            st.metric("Games", f"{second['# of Arcade Games Completed']}/2")
        
        # 1st Place (Center)
        with pod_col2:
            st.markdown("### 🥇 1st Place")
            first = top3_df.iloc[0]
            st.metric("Name", first['User Name'])
            st.metric("Badges", f"{first['# of Skill Badges Completed']}/20")
            st.metric("Games", f"{first['# of Arcade Games Completed']}/2")
        
        # 3rd Place (Right)
        with pod_col3:
            st.markdown("<br><br>", unsafe_allow_html=True)  # Add more spacing
            st.markdown("### 🥉 3rd Place")
            third = top3_df.iloc[2]
            st.metric("Name", third['User Name'])
            st.metric("Badges", f"{third['# of Skill Badges Completed']}/20")
            st.metric("Games", f"{third['# of Arcade Games Completed']}/2")
    
    st.markdown("---")
    
    # Filters above the table (horizontal)
    st.markdown("### 🔍 Filters")
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        search_name = st.text_input("Search by Name", "")
    
    with filter_col2:
        completion_filter = st.selectbox(
            "Filter by Completion Status",
            ["All", "Completed All Badges", "In Progress"]
        )
    
    with filter_col3:
        top_n = st.slider("Show Top N Participants", 5, len(df), 10)
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['User Name'].str.contains(search_name, case=False, na=False)]
    
    if completion_filter == "Completed All Badges":
        filtered_df = filtered_df[filtered_df['# of Skill Badges Completed'] == 20]
    elif completion_filter == "In Progress":
        filtered_df = filtered_df[filtered_df['# of Skill Badges Completed'] < 20]
    
    # Sort by badges completed and arcade games
    filtered_df = filtered_df.sort_values(
        by=['# of Skill Badges Completed', '# of Arcade Games Completed'],
        ascending=False
    ).reset_index(drop=True)
    
    # Display top N
    display_df = filtered_df.head(top_n).copy()
    display_df.index = range(1, len(display_df) + 1)
    
    st.markdown(f"### 📊 Leaderboard (Top {len(display_df)})")
    
    # Create display table
    for idx, row in display_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        
        with col1:
            st.markdown(f"**#{idx}**")
        
        with col2:
            st.markdown(f"**{row['User Name']}**")
        
        with col3:
            badges_completed = row['# of Skill Badges Completed']
            progress_pct = (badges_completed / 20) * 100
            
            # Color coding
            if progress_pct < 25:
                color = "#EA4335"  # Red
            elif progress_pct < 75:
                color = "#FBBC04"  # Yellow
            else:
                color = "#34A853"  # Green
            
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{badges_completed}/20 Badges</span>", unsafe_allow_html=True)
            st.progress(progress_pct / 100)
        
        with col4:
            st.markdown(f"{row['# of Arcade Games Completed']}/2 Games")
        
        with col5:
            profile_url = row['Google Cloud Skills Boost Profile URL']
            st.markdown(f"[Profile]({profile_url})")
            
            # Modal button for badge details
            if st.button(f"View Details", key=f"details_{idx}"):
                st.session_state[f'show_modal_{idx}'] = True
        
        # Show modal if button clicked
        if st.session_state.get(f'show_modal_{idx}', False):
            with st.expander(f"📋 Details for {row['User Name']}", expanded=True):
                st.markdown("**Completed Skill Badges:**")
                badges = row['Names of Completed Skill Badges']
                if pd.notna(badges) and badges:
                    badge_list = badges.split('|')
                    for badge in badge_list:
                        st.markdown(f"- {badge.strip()}")
                else:
                    st.markdown("*No badges completed yet*")
                
                st.markdown("**Completed Arcade Games:**")
                games = row['Names of Completed Arcade Games']
                if pd.notna(games) and games:
                    game_list = games.split('|')
                    for game in game_list:
                        st.markdown(f"- {game.strip()}")
                else:
                    st.markdown("*No games completed yet*")
                
                if st.button("Close", key=f"close_{idx}"):
                    st.session_state[f'show_modal_{idx}'] = False
                    st.rerun()
        
        st.markdown("---")

except FileNotFoundError:
    st.error("❌ Error: progress.csv file not found! Please make sure the file is in the same directory as app.py")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #5F6368;'>Made with ❤️ by GDGC | Powered by Google Cloud Study Jams</p>", unsafe_allow_html=True)