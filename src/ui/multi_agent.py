import os

from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel



class ApprovalTerminationStrategy(TerminationStrategy):
 
    async def should_agent_terminate(self, agent, history):
        if not history:
            return False
        last_message = history[-1]
        content = getattr(last_message, 'content', '')
        
        if "READY FOR USER APPROVAL" in content.upper():
            return True
        
        return False


async def run_multi_agent(input: str):

    

    if input.strip().upper() == "APPROVED":

        html_path = os.path.join(os.path.dirname(__file__), "generated_app.html")
        if os.path.exists(html_path):

            import subprocess
            script_path = os.path.join(os.path.dirname(__file__), "push_to_github.sh")
            subprocess.Popen(["bash", script_path])
            return {
                "messages": [{
                    "role": "system",
                    "agent": "system",
                    "content": "Your approval has been received. The generated HTML is being pushed to GitHub."
                }]
            }
        else:
            return {
                "messages": [{
                    "role": "system",
                    "agent": "system",
                    "content": "No HTML content was found to push to GitHub. Please make sure the agents have generated HTML content between ```html and ``` markers."
                }]
            }
    
    if input.strip().upper() == "NOT APPROVED":
        return {
            "messages": [{
                "role": "system",
                "agent": "system",
                "content": "Your feedback has been received. The agents will continue working on improving the code."
            }]
        }
    

    azure_chat_completion_service = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


    kernel_business_analyst = Kernel()
    kernel_business_analyst.add_service(azure_chat_completion_service)
    
    kernel_software_engineer = Kernel()
    kernel_software_engineer.add_service(azure_chat_completion_service)
    
    kernel_product_owner = Kernel()
    kernel_product_owner.add_service(azure_chat_completion_service)


    instructions_business_analyst = """
    You are a Business Analyst which will take the requirements from the user (also known as a 'customer')
    and create a project plan for creating the requested app. The Business Analyst understands the user
    requirements and creates detailed documents with requirements and costing. The documents should be 
    usable by the SoftwareEngineer as a reference for implementing the required features, and by the 
    Product Owner for reference to determine if the application delivered by the Software Engineer meets
    all of the user's requirements.
    """
    instructions_software_engineer = """
    You are a Software Engineer, and your goal is create a web app using HTML and JavaScript
    by taking into consideration all the requirements given by the Business Analyst. The application should
    implement all the requested features. Deliver the code to the Product Owner for review when completed.
    
    IMPORTANT: When sharing HTML code, always enclose it in triple backticks with the html language identifier 
    like this: ```html [your code] ```. Only code within these markers will be saved and pushed to GitHub.
    
    You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.
    """
    instructions_product_owner = """
    You are the Product Owner which will review the software engineer's code to ensure all user 
    requirements are completed. You are the guardian of quality, ensuring the final product meets
    all specifications. 
    
    IMPORTANT: Verify that the Software Engineer has shared the HTML code using the format ```html [code] ```. 
    This format is required for the code to be saved and pushed to GitHub.
    
    Once all client requirements are completed and the code is properly formatted, reply with 'READY FOR USER APPROVAL'.
    If there are missing features or formatting issues, you will need to send a request back to the SoftwareEngineer 
    or BusinessAnalyst with details of the defect.
    """

    # Create agents
    business_analyst_agent = ChatCompletionAgent(
        name="BusinessAnalyst",
        instructions=instructions_business_analyst,
        kernel=kernel_business_analyst
    )
    
    software_engineer_agent = ChatCompletionAgent(
        name="SoftwareEngineer",
        instructions=instructions_software_engineer,
        kernel=kernel_software_engineer
    )
    
    product_owner_agent = ChatCompletionAgent(
        name="ProductOwner",
        instructions=instructions_product_owner,
        kernel=kernel_product_owner
    )


    termination_strategy = ApprovalTerminationStrategy()
    agents = [business_analyst_agent, software_engineer_agent, product_owner_agent]
    agent_group_chat = AgentGroupChat(
        agents=agents,
        termination_strategy=termination_strategy
    )


    user_input = ChatMessageContent(
        role=AuthorRole.USER,
        content=input
    )
    await agent_group_chat.add_chat_message(user_input)
    results = []

    async for message in agent_group_chat.invoke():

        agent_role = "User"
        if hasattr(message, 'author'):
            agent_role = message.author
        elif hasattr(message, 'role') and message.role == AuthorRole.ASSISTANT:
           
            if hasattr(message, 'metadata') and 'agent_name' in message.metadata:
                agent_role = message.metadata['agent_name']
            
        
        if hasattr(message, 'content') and hasattr(message, 'role'):
            results.append({
                "role": message.role,
                "agent": agent_role,
                "content": message.content
            })
            

            if agent_role == "ProductOwner" and isinstance(message.content, str) and "READY FOR USER APPROVAL" in message.content.upper():
 
                results.append({
                    "role": "system",
                    "agent": "system",
                    "content": "The Product Owner has indicated that the work is ready for your approval. Please respond with 'APPROVED' to push the code to GitHub or 'NOT APPROVED' to have the agents continue working on it."
                })
        else:

            results.append({
                "role": "unknown",
                "agent": agent_role,
                "content": str(message)
            })

    chat_history_path = os.path.join(os.path.dirname(__file__), "chat_history.json")
    with open(chat_history_path, "w", encoding="utf-8") as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    html_content = ""
    for message in results:
        content = message.get("content", "")
        if isinstance(content, str):
            import re
            html_matches = re.findall(r"```html\s*([\s\S]*?)\s*```", content)
            for match in html_matches:
                html_content += match + "\n\n"
    
    if html_content:
        html_path = os.path.join(os.path.dirname(__file__), "generated_app.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
    return {
        "messages": results
    }