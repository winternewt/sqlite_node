
import os, dotenv
from just_agents.llm_session import LLMSession
import just_agents.llm_options
from ai_tools import get_headers, execute_query


dotenv.load_dotenv(override=True)
#api_key = os.getenv("OPENAI_API_KEY", None)

opt = just_agents.llm_options.OPENAI_GPT4oMINI.copy()

session: LLMSession = LLMSession(
        llm_options=just_agents.llm_options.OPENAI_GPT4oMINI.copy(),
        tools=[get_headers, execute_query]
    )

result = session.query("You have access to a DrugAge database stored as 'csv_data'. What columns does it list? What are the model animals?")
print("Results: ", result)
result = session.query("You have access to a DrugAge database. What is the database internal name? Formulate and execute an SQLite query to find out in which animal model metformin lifespan effect was maximal.")
print("Results: ", result)


