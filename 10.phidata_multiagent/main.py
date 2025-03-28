from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
load_dotenv()

import os

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
api_key = os.getenv('GOOGLE_API_KEY')
os.environ["PHI_DEFAULT_MODEL"] = "gemini-2.0-flash"

web_agent=Agent(
    name='web-search-agent',
    description="Search the web for user query",
    model=Gemini(id="gemini-2.0-flash",api_key=api_key),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    description="Get financial data",
    model=Gemini(id="gemini-2.0-flash",api_key=api_key),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Summarize analyst recommendations and share the latest news for NVDA", stream=True)