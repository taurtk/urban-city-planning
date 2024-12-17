import os
import streamlit as st
import sys
import time
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from textwrap import dedent
from tenacity import retry, stop_after_attempt, wait_exponential

os.environ["GROQ_API_KEY"]='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'
# Disable verbose warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

def print_error_details():
    """Print detailed error information for debugging."""
    import traceback
    st.error("An error occurred. Check console for details.")
    st.text("\n--- Detailed Error Information ---")
    st.text(traceback.format_exc())
    st.text("\n--- System Details ---")
    st.text(f"Python Version: {sys.version}")
    st.text(f"GROQ_API_KEY set: {'Yes' if 'GROQ_API_KEY' in os.environ else 'No'}")

class UrbanAINexusAgents:
    def __init__(self, llm):
        self.llm = llm

    def infrastructure_planning_agent(self):
        return Agent(
            llm=self.llm,
            role="Urban Infrastructure Planner",
            goal="Develop sustainable infrastructure models",
            backstory="Expert in urban development focusing on efficient and sustainable infrastructure strategies.",
            verbose=False,
            allow_delegation=False
        )

    def economic_development_agent(self):
        return Agent(
            llm=self.llm,
            role="Urban Economic Strategist",
            goal="Analyze and optimize local economic trends",
            backstory="Specialist in urban economic development with a focus on sustainable growth strategies.",
            verbose=False,
            allow_delegation=False
        )

class UrbanAINexusTasks:
    def __init__(self, agents):
        self.agents = agents

    def infrastructure_planning_task(self):
        return Task(
            description=dedent("""\
                Develop a concise infrastructure development plan for a sustainable urban environment.
                - Outline key infrastructure needs
                - Propose strategic placement strategies
                - Provide high-level cost considerations
                - Align with sustainability principles"""),
            expected_output=dedent("""\
                Compact infrastructure development plan including:
                1. Priority infrastructure recommendations
                2. Strategic placement overview
                3. Sustainability alignment
                4. Preliminary cost insights"""),
            agent=self.agents.infrastructure_planning_agent(),
            async_execution=False
        )

    def economic_development_task(self):
        return Task(
            description=dedent("""\
                Analyze economic potential and development opportunities.
                - Identify key economic growth areas
                - Propose investment strategies
                - Highlight job market potential
                - Recommend economic resilience approaches"""),
            expected_output=dedent("""\
                Focused economic development strategy including:
                1. Economic growth opportunities
                2. Investment recommendation summary
                3. Job market potential assessment
                4. Economic resilience framework"""),
            agent=self.agents.economic_development_agent(),
            async_execution=False
        )

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def urban_ai_nexus_simulation(city_context):
    try:
        # Ensure API key is set
        if "GROQ_API_KEY" not in os.environ or not os.environ["GROQ_API_KEY"]:
            raise ValueError("GROQ API Key is not set. Please set the GROQ_API_KEY environment variable.")

        # Use a more token-efficient model
        llm = ChatGroq(
            temperature=0,
            model_name="groq/llama-3.2-3b-preview",
            # api_key='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'
        )

        # Initialize agents and tasks with reduced complexity
        agents = UrbanAINexusAgents(llm)
        tasks = UrbanAINexusTasks(agents)

        # Create crew with reduced agents and tasks
        crew = Crew(
            agents=[
                agents.infrastructure_planning_agent(),
                agents.economic_development_agent()
            ],
            tasks=[
                tasks.infrastructure_planning_task(),
                tasks.economic_development_task()
            ],
            verbose=False  # Reduce overall verbosity
        )

        # Kickoff the simulation with city-specific context
        result = crew.kickoff(inputs={'city_context': city_context})
        return result

    except Exception as e:
        print_error_details()
        time.sleep(20)  # Wait between retries for debugging purposes.
        raise

def main():
    st.title("🏙️ Urban AI Nexus: City Development Simulator")
    
    # Sidebar for input
    st.sidebar.header("City Configuration")
    
    # City Name
    city_name = st.sidebar.text_input("City Name", "SmartCity Beta")
    
    # Population
    population = st.sidebar.number_input(
        "Population", 
        min_value=1000, 
        max_value=10000000, 
        value=500000
    )
    
    # Current Challenges
    st.sidebar.subheader("Current Challenges")
    challenges = [
        st.sidebar.text_input(f"Challenge {i+1}", default_challenges[i] if i < len(default_challenges) else "")
        for i in range(3)
    ]
    challenges = [c for c in challenges if c]  # Remove empty challenges
    
    # Sustainability Goals
    st.sidebar.subheader("Sustainability Goals")
    goals = [
        st.sidebar.text_input(f"Goal {i+1}", default_goals[i] if i < len(default_goals) else "")
        for i in range(3)
    ]
    goals = [g for g in goals if g]  # Remove empty goals
    
    # Simulation Button
    if st.sidebar.button("Generate Urban Development Plan"):
        # Prepare city context
        city_context = {
            "name": city_name,
            "population": population,
            "current_challenges": challenges,
            "sustainability_goals": goals
        }
        
        # Run simulation with progress bar
        with st.spinner('Generating Urban Development Plan...'):
            try:
                result = urban_ai_nexus_simulation(city_context)
                
                if result:
                    st.success("Urban Development Plan Generated!")
                    
                    # Expand result sections
                    with st.expander("🏗️ Urban Development Plan", expanded=True):
                        st.write(result)
                else:
                    st.error("Failed to generate development plan.")
            
            except Exception as e:
                print_error_details()

# Default values for challenges and goals
default_challenges = [
    "High carbon emissions",
    "Uneven resource distribution",
    "Limited public transportation"
]

default_goals = [
    "50% carbon emission reduction by 2030",
    "Increase public transit usage by 40%",
    "Develop more green spaces"
]

if __name__ == "__main__":
    main()
