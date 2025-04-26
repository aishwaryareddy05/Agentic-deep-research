import streamlit as st
from agents import research_agent, answer_drafter_agent
from tasks import research_task, draft_task
from crewai import Crew, Process
import json
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource
def load_animation(animation_path):
    try:
        with open(animation_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Animation load failed: {e}")
        return None

def inject_css():
    st.markdown("""
        <style>
            .nebula-header {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                margin-bottom: 2rem;
            }
            .nebula-header h1 {
                color: #c084fc;
                font-size: 2.5rem;
            }
            .query-box input {
                border: 2px solid #7dd3fc !important;
                border-radius: 12px !important;
            }
            .metric-label {
                color: #38bdf8;
                font-size: 0.9rem;
            }
            .metric-value {
                font-size: 1.4rem;
                color: #ffffff;
            }
            .summary-container {
                background-color: #0f172a;
                padding: 1.2rem;
                border-radius: 14px;
                color: #e2e8f0;
            }
        </style>
    """, unsafe_allow_html=True)

def progress_gauge(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#38bdf8"},
            'steps': [
                {'range': [0, 50], 'color': "#1e3a8a"},
                {'range': [50, 100], 'color': "#0ea5e9"},
            ],
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(paper_bgcolor="#0f172a", font_color="#f8fafc", height=250)
    return fig

def initialize_state():
    for key in ['research_results', 'progress']: 
        if key not in st.session_state:
            st.session_state[key] = {} if key == 'research_results' else 0
def main():
    st.set_page_config("Fairycon Research Core", page_icon="🪐", layout="wide")
    inject_css()
    initialize_state()

    animation_data = load_animation("orbit-ai.json")

  
    st.markdown("""
        <div class='nebula-header'>
            <h1>🪐 Fairycon Research Core</h1>
            <p>AI-Powered Deep Research Companion</p>
        </div>
    """, unsafe_allow_html=True)

 
    with st.sidebar:
        st.header("AI-Powered-Researcher tool ⚙️")
        if animation_data:
            st_lottie(animation_data, height=180, speed=1)

    # MAIN INTERACTION
    query = st.text_input("Enter research query", 
                         placeholder="Type something interesting...", 
                         help="The AI will search and synthesize data based on this.",
                         key="research_query")

    if st.button("🚀 Launch Research"):
        if not query:
            st.warning("Please input a query first.")
            return

        with st.spinner("Collecting knowledge across galaxies..."):
            st.session_state.progress = 30
            
            try:
               
                research_task.description = f"Research information about: {query}"
                draft_task.description = f"Draft a response about: {query}"
                
        
                crew = Crew(
                    agents=[research_agent, answer_drafter_agent],
                    tasks=[research_task, draft_task],
                    process=Process.sequential,
                    verbose=True
                )

                
                results = crew.kickoff(inputs={'query': query})

                st.session_state.progress = 100
                st.session_state.research_results = {
                    "query": query,
                    "results": results
                }
                
            except Exception as e:
                logger.error(f"Research failed: {e}")
                st.error(f"Research failed: {str(e)}")
                st.session_state.progress = 0


   
    if st.session_state.progress:
        st.plotly_chart(progress_gauge(st.session_state.progress), use_container_width=True)

    
    if st.session_state.research_results:
        tab1, tab2 = st.tabs(["✨ Summary", "📄 Raw"])

        with tab1:
            st.markdown("""
                <div class='summary-container'>
                    <h3>✨ Final Summary</h3>
                    <p>{}</p>
                </div>
            """.format(st.session_state.research_results["results"]), unsafe_allow_html=True)

        with tab2:
            st.json(st.session_state.research_results)

if __name__ == "__main__":
    main()
