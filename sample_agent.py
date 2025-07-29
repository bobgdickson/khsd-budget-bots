# -------------------------------
# 🤖 SAMPLE AGENT: Getting Started
# -------------------------------
# This file shows the basic building blocks of an agent + tool combo.
# It is designed to be readable and editable by non-Python experts.

# --- Imports ---
from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel
import asyncio

# --------------------------
# 🧰 TOOL: Word Counter
# --------------------------
# Tools are functions the AI agent can call to help it perform a task.
# Tools can be API calls, database queries, parsers, calculators, etc.
# This one just counts the number of words in a string.

class WordCountResult(BaseModel):
    word_count: int
    success: bool
    message: str

@function_tool
def count_words(input: str) -> WordCountResult:
    """
    Count the number of words in the input string.
    The input will usually come from the user or from another tool.
    """
    try:
        num_words = len(input.strip().split())
        return WordCountResult(
            word_count=num_words,
            success=True,
            message="Word count successful"
        )
    except Exception as e:
        return WordCountResult(
            word_count=0,
            success=False,
            message=f"Error: {str(e)}"
        )

# --------------------------
# 🧠 AGENT: Text Summarizer
# --------------------------
# This is where we define the agent's behavior.
# Think of it like writing the AI's job description.

text_summary_agent = Agent(
    name="Summary Agent",
    instructions=(
        "You are a helpful assistant. "
        "Use the count_words tool to get the word count of the input. "
        "Then, summarize the input in one sentence. "
        "Include the word count in the final response."
    ),
    tools=[count_words],  # List of tools this agent is allowed to use
    model="gpt-4.1-mini",  # You can change this to try different OpenAI models
    output_type=str,  # The agent should return a plain string
)

# --------------------------
# 🚀 RUNNER FUNCTION
# --------------------------
# This is the code that actually runs the agent on a sample input.

async def run_sample():
    sample_input = (
        "Generative AI has the potential to transform how organizations automate work, "
        "extract insights, and interact with data. It can also boost productivity."
    )

    with trace("Running sample agent"):
        result = await Runner.run(text_summary_agent, sample_input)
        print("✅ Agent response:")
        print(result)

# --------------------------
# 🧪 ENTRY POINT (Run this file)
# --------------------------
# You can run this file directly with:
#   python sample_agent.py

if __name__ == "__main__":
    asyncio.run(run_sample())
