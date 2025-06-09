# Import packages
# Import packages
import os
import asyncio
import logging
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.agents.strategies.selection.kernel_function_selection_strategy import (
    KernelFunctionSelectionStrategy,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel

from dotenv import load_dotenv
##from otlp_tracing import configure_oltp_grpc_tracing

load_dotenv() # Loads the environment variables and credentials we need to setup the agent


logging.basicConfig(level=logging.INFO)
tracer = configure_oltp_grpc_tracing()
logger = logging.getLogger(__name__)

class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""
 
    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        # return NotImplementedError("Code to be implemented by the student")
        return "approved" in history[-1].content.lower()


# create personas
ANALYST_NAME = "BusinessAnalyst"
ANALYST_INSTRUCTIONS = """
You are a Business Analyst which will take the requirements from the user (also known as a 'customer') and create a project plan for creating the requested app. 
The Business Analyst understands the user requirements and creates detailed documents with requirements and costing. 
The documents should be usable by the SoftwareEngineer as a reference for implementing the required features, and by the Product Owner for reference to determine if the application delivered by the Software Engineer meets all of the user's requirements.
"""

ENGINEER_NAME = "SoftwareEngineer"
ENGINEER_INSTRUCTIONS = """
You are a Software Engineer, and your goal is create a web app using HTML and JavaScript by taking into consideration all the requirements given by the Business Analyst. 
The application should implement all the requested features. 
Deliver the code to the Product Owner for review when completed. 
You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.
"""

OWNER_NAME = "ProductOwner"
OWNER_INSTRUCTIONS = """
You are the Product Owner which will review the software engineer's code to ensure all user requirements are completed. 
You are the guardian of quality, ensuring the final product meets all specifications. 
IMPORTANT: Verify that the Software Engineer has shared the HTML code using the format ```html [code] ```. 
This format is required for the code to be saved and pushed to GitHub. 
Once all client requirements are completed and the code is properly formatted, reply with 'READY FOR USER APPROVAL'. 
If there are missing features or formatting issues, you will need to send a request back to the SoftwareEngineer or BusinessAnalyst with details of the defect."""


async def run_multi_agent(input: str):
    service_id ="service_id"
    # Define the Kernel
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(service_id=service_id))
    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    ####settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create agents
    BusinessAnalyst_agent = ChatCompletionAgent(
    id="Analyst", 
    kernel=kernel, 
    name=BusinessAnalyst_NAME, 
    instructions=BusinessAnalyst_INSTRUCTIONS,
    service=AzureChatCompletion()
    )

    SoftwareEngineer_agent = ChatCompletionAgent(
    id="Engineer", 
    kernel=kernel, 
    name=SoftwareEngineer_NAME, 
    instructions=SoftwareEngineer_INSTRUCTIONS,
    service=AzureChatCompletion()
    )

    ProductOwner_agent = ChatCompletionAgent(
    id="Reviewer", 
    kernel=kernel, 
    name=ProductOwner_NAME, 
    instructions=ProductOwner_INSTRUCTIONS,
    service=AzureChatCompletion()
    )

    # Chat agent group and termination strategy
    chat = AgentGroupChat(
        agents=[BusinessAnalyst_agent,
                SoftwareEngineer_agent,
                ProductOwner_agent],
        termination_strategy=ApprovalTerminationStrategy(agents=[ProductOwner_agent], maximum_iterations=10),
    )
    logger.info(f"User said  : {input}")
    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=input))

    # Collect responses
    responses = []
    async for response in chat.invoke():
        responses.append({"role": response.role.value, "message": response.content})
    
    logger.info("Agent chat finished.")
    return responses
