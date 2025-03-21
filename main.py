import os
from crewai import Crew, Process,LLM
from agents import retrieve_suppliers, domain_researcher_agent, ai_suppliers_writer
from tasks import retrieve_suppliers_task, domain_and_trustpilot_researcher_task, ai_suppliers_write_task
from textwrap import dedent
planningllm = LLM(
    model="gemini/gemini-2.0-flash"
)
class AiSuppliersCrew:
    def __init__(self, inputs):
        self.inputs = inputs

    def run(self):
        # Initialize tasks with respective agents
        research_task = retrieve_suppliers_task
        domain_trustpilot_task = domain_and_trustpilot_researcher_task
        writing_task = ai_suppliers_write_task

        # Form the crew with defined agents and tasks
        crew = Crew(
            agents=[retrieve_suppliers, domain_researcher_agent, ai_suppliers_writer],
            tasks=[research_task, domain_trustpilot_task, writing_task],
            process=Process.sequential,
            # planning=True,
            # planning_llm=planningllm,
        )

        # Execute the crew to carry out the research project
        return crew.kickoff(inputs=self.inputs)

if __name__ == "__main__":
    print("Welcome to the AI Suppliers Research Crew")
    print("---------------------------------------")
    topic = input("Enter the supplier category or company name to research: ")
    country = input("Enter the target country (optional, leave blank for global search): ")

    inputs = {
        "topic": topic,
        "country": country
    }

    research_crew = AiSuppliersCrew(inputs)
    result = research_crew.run()

    print("\n\n##############################")
    print("## AI Suppliers Research Report:")
    print("##############################\n")
    print(result)
