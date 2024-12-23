# agents.py
from agent_helper import TailwindDocsHelper
import autogen

# Init vector DB helper
docs_helper = TailwindDocsHelper()

config_list = [{
   "model": "meta-llama/Llama-3.3-70B-Instruct", 
   "base_url": "https://api.hyperbolic.xyz/v1",
   "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldXJ5dGhtaWEuaW50ZXJhY3RpdmVAZ21haWwuY29tIiwiaWF0IjoxNzMzNTA1NzcxfQ.NXnZfydBvo1K6SeB-N7x47CngdjfzcvjpuldaR_3tWY"
}]

analyzer = autogen.AssistantAgent(
   name="analyzer",
   system_message="""Analyze UI/UX requirements:
   - Identify key components
   - List technical constraints 
   - Break down into sub-tasks
   - Ask for a modern and stylish design""",
   llm_config={"config_list": config_list}
)

solution_finder = autogen.AssistantAgent(
   name="solution_finder", 
   system_message="""Find Tailwind solutions:
   - Search docs for patterns
   - Propose optimal classes
   - Consider responsiveness""",
   function_map={"search_docs": docs_helper.search_docs},
   llm_config={"config_list": config_list}
)

code_presenter = autogen.AssistantAgent(
   name="code_presenter",
   system_message="""Present clean code solutions:
   - HTML/JSX only
   - Essential Tailwind classes
   - Minimal comments""",
   llm_config={"config_list": config_list}
)

group_chat = autogen.GroupChat(
   agents=[analyzer, solution_finder, code_presenter],
   messages=[],
   max_round=5
)

manager = autogen.GroupChatManager(
   groupchat=group_chat,
   llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
   name="user",
   human_input_mode="TERMINATE",
   max_consecutive_auto_reply=10,
   llm_config={"config_list": config_list}
)

# Start chat
user_proxy.initiate_chat(
   manager,
   message="Create a responsive frontpage for an online store"
)