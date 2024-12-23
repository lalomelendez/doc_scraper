from agent_helper import create_tailwind_agent
import autogen

# Create agents
tailwind_agent = create_tailwind_agent()

config_list = [{
    "model": "meta-llama/Llama-3.3-70B-Instruct",
    "base_url": "https://api.hyperbolic.xyz/v1",
    "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldXJ5dGhtaWEuaW50ZXJhY3RpdmVAZ21haWwuY29tIiwiaWF0IjoxNzMzNTA1NzcxfQ.NXnZfydBvo1K6SeB-N7x47CngdjfzcvjpuldaR_3tWY"
}]

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": config_list}
)

# Start chat
user_proxy.initiate_chat(
    tailwind_agent,
    message="How do I create a responsive card component?"
)