import os
from dotenv import load_dotenv
import openai

load_dotenv()
os.environ['OPENAI_API_KEY'] =os.getenv('OPENAI_API_KEY')

os.environ["GROQ_API_KEY"] = "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"


#Web search agent
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

web_search_agent = Agent(
    name="Web Search Agent",
    model=Groq(id="llama-3.2-90b-vision-preview"),
    tools=[DuckDuckGo()],
    role="search web for latest information",
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

#Finance Agent
from phi.tools.yfinance import YFinanceTools


finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,stock_fundamentals=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_search_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Summarize analyst recommendations and share the latest news for NVDA",stream=True)