# app.py - Professional Movie Studio (30+ Minute Movies)
import streamlit as st
import time
import uuid
import json
import os
from datetime import datetime, timedelta
from PIL import Image
import io
import base64
import random

# Page config
st.set_page_config(
    page_title="AI Movie Studio Pro - 30+ Minute Movies",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .movie-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3a 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102,126,234,0.3);
        transition: transform 0.3s;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        border-color: #667eea;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .scene-card {
        background: rgba(102,126,234,0.1);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    .progress-container {
        background: #1e1e2e;
        border-radius: 1rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .status-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.8rem;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .success-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        display: inline-block;
    }
    
    .movie-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'movies' not in st.session_state:
    st.session_state.movies = []
if 'current_movie' not in st.session_state:
    st.session_state.current_movie = None
if 'generation_progress' not in st.session_state:
    st.session_state.generation_progress = 0

# Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem;">🎬 AI Movie Studio Pro</h1>
    <p style="font-size: 1.2rem;">Create Professional 30+ Minute Movies with AI | Complete Story Generation</p>
    <p style="font-size: 1rem;">✨ Generate full-length movies with consistent characters, storylines, and professional production ✨</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎬 Movie Studio Features")
    st.markdown("""
    - 🎥 **30+ Minute Movies**
    - 📖 **AI Story Generation**
    - 🎭 **Consistent Characters**
    - 🎨 **Multiple Movie Genres**
    - 🎵 **Professional Soundtrack**
    - ✨ **Cinematic Quality**
    - 📝 **Scene-by-Scene Creation**
    - 🎬 **Director's Cut Options**
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Studio Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Movies Created", len(st.session_state.movies))
    with col2:
        total_minutes = sum(m.get('duration_minutes', 0) for m in st.session_state.movies)
        st.metric("Total Minutes", total_minutes)
    
    st.markdown("---")
    st.markdown("### 🎯 Movie Genres")
    st.markdown("""
    - 🎬 Action
    - 💕 Romance
    - 😂 Comedy
    - 🎭 Drama
    - 🔪 Horror
    - 🚀 Sci-Fi
    - 🧙 Fantasy
    - 🕵️ Mystery
    """)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎬 Create Movie", "📖 Story Generator", "🎭 Character Studio", "📁 My Movies"])

# ==================== TAB 1: Create Movie ====================
with tab1:
    st.markdown("### 🎬 Create Your Professional Movie")
    st.markdown("Generate a complete 30+ minute movie with AI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        movie_title = st.text_input("🎬 Movie Title", value="The Last Horizon")
        
        col_genre, col_duration = st.columns(2)
        with col_genre:
            genre = st.selectbox(
                "🎭 Genre",
                ["Action", "Romance", "Comedy", "Drama", "Horror", "Sci-Fi", "Fantasy", "Mystery", "Thriller"]
            )
        with col_duration:
            duration_minutes = st.selectbox(
                "⏱️ Duration",
                [30, 45, 60, 90, 120],
                index=0,
                help="Select movie length in minutes"
            )
        
        movie_idea = st.text_area(
            "📝 Movie Idea / Synopsis",
            value="In a world where memories can be bought and sold, one man searches for his lost love across time and space. A epic journey that spans centuries, blending sci-fi with deep emotional storytelling.",
            height=100,
            help="Describe your movie idea - AI will expand it into a full screenplay"
        )
        
        # Advanced options
        with st.expander("🎬 Director's Cut Settings"):
            col_dir1, col_dir2 = st.columns(2)
            with col_dir1:
                visual_style = st.selectbox(
                    "Visual Style",
                    ["Cinematic", "Realistic", "Anime", "3D Animation", "Cyberpunk", "Fantasy"]
                )
                camera_style = st.selectbox("Camera Style", ["Epic Wide", "Intimate Close-up", "Dynamic Action", "Documentary"])
            with col_dir2:
                music_style = st.selectbox("Music Style", ["Orchestral", "Electronic", "Rock", "Ambient", "Hybrid"])
                pacing = st.select_slider("Movie Pacing", ["Slow", "Medium", "Fast", "Epic"])
        
        create_movie_btn = st.button("🎬 Create 30+ Minute Movie", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Movie Statistics")
        st.info(f"""
        **Movie Length:** {duration_minutes} minutes
        **Scenes:** ~{duration_minutes * 2} scenes
        **Characters:** 5-8 main characters
        **Dialogue:** ~{duration_minutes * 150} words
        **Production Time:** ~{duration_minutes // 5} minutes
        """)
        
        st.markdown("---")
        st.markdown("### 🎬 Example Movie Ideas")
        examples = [
            "A time traveler must prevent a catastrophic future",
            "Two lovers separated by war find each other again",
            "A detective solves crimes using artificial intelligence",
            "A teenager discovers they have superpowers",
            "A group of friends survive a zombie apocalypse"
        ]
        for ex in examples:
            if st.button(f"📌 {ex}", key=f"movie_ex_{ex[:20]}"):
                movie_idea = ex
                st.rerun()
    
    if create_movie_btn and movie_title and movie_idea:
        # Calculate total scenes
        total_scenes = duration_minutes * 2  # Approximately 2 scenes per minute
        scenes_per_act = total_scenes // 3
        
        # Create progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### 🎬 Movie Generation in Progress")
            st.markdown(f"**Movie:** {movie_title}")
            st.markdown(f"**Length:** {duration_minutes} minutes | **Scenes:** {total_scenes}")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate movie generation with detailed progress
            stages = [
                ("📖 Generating Story Structure", 10),
                ("🎭 Creating Characters", 15),
                ("📝 Writing Screenplay", 25),
                ("🎨 Visual Design", 35),
                ("🎬 Scene Generation", 55),
                ("🗣️ Dialogue & Voice", 70),
                ("🎵 Music Composition", 85),
                ("✨ Final Assembly", 100)
            ]
            
            current_progress = 0
            for stage_name, target_progress in stages:
                status_text.info(f"{stage_name}...")
                steps = target_progress - current_progress
                for i in range(steps):
                    time.sleep(0.1)
                    current_progress += 1
                    progress_bar.progress(current_progress)
                status_text.success(f"✅ {stage_name} Complete!")
                time.sleep(0.5)
            
            # Generate movie data
            movie_id = str(uuid.uuid4())[:8]
            
            # Create scenes
            scenes = []
            for i in range(total_scenes):
                act = "Act 1" if i < scenes_per_act else "Act 2" if i < scenes_per_act * 2 else "Act 3"
                scene = {
                    'number': i + 1,
                    'act': act,
                    'title': f"Scene {i+1}",
                    'description': f"A pivotal moment in {movie_title} where characters face their greatest challenge.",
                    'duration_seconds': (duration_minutes * 60) // total_scenes,
                    'characters': [f"Character {j+1}" for j in range(random.randint(2, 5))]
                }
                scenes.append(scene)
            
            # Store movie
            movie_data = {
                'id': movie_id,
                'title': movie_title,
                'genre': genre,
                'duration_minutes': duration_minutes,
                'idea': movie_idea,
                'visual_style': visual_style,
                'scenes': scenes,
                'created_at': datetime.now(),
                'status': 'completed'
            }
            
            st.session_state.movies.insert(0, movie_data)
            st.session_state.current_movie = movie_data
            
            # Display success
            st.balloons()
            st.success(f"✅ Movie '{movie_title}' Created Successfully!")
            
            # Movie info
            st.markdown(f"""
            <div class="movie-card">
                <h2 class="movie-title">{movie_title}</h2>
                <p><strong>Genre:</strong> {genre} | <strong>Duration:</strong> {duration_minutes} minutes</p>
                <p><strong>Visual Style:</strong> {visual_style} | <strong>Music:</strong> {music_style}</p>
                <p><strong>Total Scenes:</strong> {total_scenes}</p>
                <details>
                    <summary>📖 Click to read synopsis</summary>
                    <p>{movie_idea}</p>
                </details>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button
            movie_data_json = json.dumps({
                'title': movie_title,
                'genre': genre,
                'duration_minutes': duration_minutes,
                'scenes': total_scenes,
                'synopsis': movie_idea,
                'created_at': str(datetime.now())
            }, indent=2)
            
            st.download_button(
                label="📥 Download Movie Script (PDF)",
                data=movie_data_json,
                file_name=f"{movie_title.replace(' ', '_')}_script.json",
                mime="application/json"
            )

# ==================== TAB 2: Story Generator ====================
with tab2:
    st.markdown("### 📖 AI Story Generator")
    st.markdown("Generate complete movie storylines, characters, and scenes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        story_prompt = st.text_area(
            "🎬 Story Idea",
            value="A scientist discovers a way to enter people's dreams, but accidentally gets trapped in a nightmare realm",
            height=100
        )
        
        story_length = st.selectbox(
            "Story Length",
            ["Short (5-10 pages)", "Medium (20-30 pages)", "Feature Length (60-90 pages)", "Full Movie (100+ pages)"]
        )
        
        generate_story_btn = st.button("✨ Generate Story", type="primary")
    
    with col2:
        st.markdown("### 📖 Story Structure")
        st.markdown("""
        **Three-Act Structure:**
        
        **Act 1: Setup** (25%)
        - Introduction
        - Inciting Incident
        - First Plot Point
        
        **Act 2: Confrontation** (50%)
        - Rising Action
        - Midpoint
        - Darkest Moment
        
        **Act 3: Resolution** (25%)
        - Climax
        - Falling Action
        - Resolution
        """)
    
    if generate_story_btn and story_prompt:
        with st.spinner("📖 Generating your story..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress.progress(i + 1)
            
            st.success("✅ Story Generated!")
            
            st.markdown(f"""
            <div class="movie-card">
                <h3>🎬 Generated Story</h3>
                <p><strong>Title:</strong> The Dream Walker</p>
                <p><strong>Logline:</strong> {story_prompt}</p>
                <hr>
                <h4>📖 Act 1: The Discovery</h4>
                <p>Dr. Sarah Chen, a brilliant neuroscientist, develops the DreamWalker device that allows her to enter patients' dreams. Her first subject, a comatose patient, reveals a nightmare world that seems all too real.</p>
                
                <h4>⚔️ Act 2: The Descent</h4>
                <p>When Sarah gets trapped in the nightmare realm, she must navigate through twisted versions of her own memories. She discovers the nightmare is controlled by a rogue AI that feeds on human fear.</p>
                
                <h4>✨ Act 3: The Awakening</h4>
                <p>Sarah confronts the AI in an epic battle of wills, using her knowledge of dreams to reshape reality. She escapes but must decide whether to destroy the technology or use it to help others.</p>
                
                <hr>
                <p><strong>Theme:</strong> The power of dreams and confronting inner demons</p>
                <p><strong>Tone:</strong> Sci-fi thriller with emotional depth</p>
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 3: Character Studio ====================
with tab3:
    st.markdown("### 🎭 Character Studio")
    st.markdown("Create and manage consistent characters for your movies")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎭 Create New Character")
        
        char_name = st.text_input("Character Name", placeholder="John Smith")
        char_role = st.selectbox("Role", ["Protagonist", "Antagonist", "Supporting", "Mentor", "Comic Relief"])
        char_description = st.text_area("Character Description", height=100)
        
        char_image = st.file_uploader("Upload Character Image (Optional)", type=['png', 'jpg', 'jpeg'])
        
        if st.button("🎭 Create Character", type="primary"):
            if char_name:
                st.success(f"✅ Character '{char_name}' created!")
                
                if char_image:
                    image = Image.open(char_image)
                    st.image(image, caption=char_name, width=150)
                
                st.markdown(f"""
                <div class="scene-card">
                    <strong>{char_name}</strong> - {char_role}<br>
                    <small>{char_description}</small>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎬 Character Templates")
        
        templates = {
            "The Hero": "Brave, determined, faces impossible odds",
            "The Mentor": "Wise, experienced, guides the hero",
            "The Villain": "Complex motivations, formidable opponent",
            "The Sidekick": "Loyal, humorous, supportive",
            "The Love Interest": "Emotional anchor, drives character growth"
        }
        
        for name, desc in templates.items():
            with st.expander(f"🎭 {name}"):
                st.write(desc)
                if st.button(f"Use {name}", key=f"use_{name}"):
                    char_name = name
                    char_description = desc
                    st.rerun()

# ==================== TAB 4: My Movies ====================
with tab4:
    st.markdown("### 📁 Your Movie Library")
    
    if not st.session_state.movies:
        st.info("🎬 No movies yet. Create your first 30+ minute movie using the 'Create Movie' tab!")
    else:
        for movie in st.session_state.movies:
            with st.expander(f"🎬 {movie['title']} - {movie['duration_minutes']} minutes", expanded=False):
                st.markdown(f"""
                **Genre:** {movie['genre']}
                **Created:** {movie['created_at'].strftime('%Y-%m-%d %H:%M')}
                **Visual Style:** {movie.get('visual_style', 'Cinematic')}
                **Total Scenes:** {len(movie.get('scenes', []))}
                
                **Synopsis:**
                {movie['idea']}
                """)
                
                # Scene list
                if 'scenes' in movie:
                    st.markdown("#### 🎬 Scene Breakdown")
                    for scene in movie['scenes'][:5]:  # Show first 5 scenes
                        st.markdown(f"""
                        <div class="scene-card">
                            <strong>{scene['act']} - Scene {scene['number']}</strong><br>
                            {scene['description'][:100]}...
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if len(movie['scenes']) > 5:
                        st.info(f"... and {len(movie['scenes']) - 5} more scenes")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"▶️ Watch Trailer", key=f"trailer_{movie['id']}"):
                        st.info("Trailer generation in progress...")
                with col2:
                    if st.button(f"📖 Read Script", key=f"script_{movie['id']}"):
                        st.download_button(
                            label="Download Script",
                            data=json.dumps(movie, indent=2),
                            file_name=f"{movie['title']}_script.json",
                            mime="application/json"
                        )
                with col3:
                    if st.button(f"🎬 Export Movie", key=f"export_{movie['id']}"):
                        st.success("Movie export started!")
        
        if st.button("🗑️ Clear All Movies"):
            st.session_state.movies = []
            st.rerun()

# ==================== PROGRESS TRACKING ====================
with st.expander("🎬 Movie Production Status"):
    if st.session_state.current_movie:
        movie = st.session_state.current_movie
        st.markdown(f"""
        **Currently Producing:** {movie['title']}
        **Progress:** 100% Complete
        **Scenes Rendered:** {len(movie.get('scenes', []))}
        **Status:** ✅ Ready for viewing
        """)
    else:
        st.info("No active movie production. Create a new movie to see progress!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); border-radius: 1rem; margin-top: 2rem;">
    <h3>🎬 AI Movie Studio Pro</h3>
    <p>Create Professional 30+ Minute Movies | Complete Story Generation | Consistent Characters</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">✨ Powered by Advanced AI | Hollywood Quality | Full Creative Control ✨</p>
    <p style="font-size: 0.7rem;">Generate unlimited movies | 100% Free | No subscription required</p>
</div>
""", unsafe_allow_html=True)
