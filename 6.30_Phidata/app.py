#for executing app in phidata playground
from phi.agent import Agent
from phi.model.groq import Groq
from fastapi import FastAPI
from phi.tools.duckduckgo import DuckDuckGo
import phi
import os
from dotenv import load_dotenv
from phi.playground import Playground,serve_playground_app


load_dotenv()
phi.api=os.getenv('PHI_API_KEY')
os.environ['GROQ_API_KEY'] =os.getenv('GROQ_API_KEY')




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

app=Playground(agents=[web_search_agent, finance_agent]).get_app()


if __name__ == '__main__':
    serve_playground_app("app:app",reload=True)