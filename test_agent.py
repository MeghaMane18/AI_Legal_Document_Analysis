from agents.legal_agent import legal_agent

response = legal_agent.run(
    "What is a legal contract?"
)

print(response.content)