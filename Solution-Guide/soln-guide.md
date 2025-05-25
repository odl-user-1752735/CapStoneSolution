## Solution Guide
# Multi-Agent Systems - Solution Guide

## Introduction

Multi-Agent Systems (MAS) consist of multiple autonomous agents, each with distinct goals, behaviors, and areas of responsibility. These agents can interact with each other, either cooperating or competing, depending on the objectives they are designed to achieve. In MAS, each agent operates independently, making decisions based on its local knowledge and the environment, but they can communicate and share information to solve complex problems collectively.

MAS is often used in scenarios where tasks are distributed across different entities, and the overall system benefits from decentralization. Examples include simulations of real-world systems like traffic management, robotic teams, distributed AI applications, or networked systems where agents need to coordinate actions without a central controller. MAS allows for flexibility, scalability, and adaptability in solving dynamic and complex problems where a single agent or centralized system might be less efficient or incapable of handling the complexity on its own.

In this challenge, you will create a multi-agent system that takes the user's request and feeds it to a collection of agents. Each agent will have its own persona and responsibility. The final response will be a collection of answers from all agents that together will satisfy the user's request based on each persona's area of expertise.

## Task 1 - Azure AI Foundry Model Deployment & Environment Configuration

1. Navigate to `https://portal.azure.com` and log in with your Azure credentials.

    - **Email/Username**: <inject key="AzureAdUserEmail"></inject>
    - **Password**: <inject key="AzureAdUserPassword"></inject>

1. Search and Select Open AI. 

   ![](./Images/Image1.png)

1. On the Open AI content page, click on + create. 

   ![](./Images/Image2.png)

1. Provide the following details and click on Next (7):

    - Subscription: Keep the default subscription

    - Resource Group: Click on Create new (1), provide the name as **openaiagents** and click on OK.

    - Region: East US 2 (3)

    - Name: **OpenAI-<inject key="Deployment ID" enableCopy="false"/>** (4)

    - Pricing Tier: Standard (5)

   ![](./Images/Image3.png)

1. Click on Next twice and click on **Review + Submit**.

1. Review all the values and click on **Create**.

1. Once the deployment is complete, click on **Go to resource**

1. In the Azure OpenAI resource pane, click on Go to Azure AI Foundry portal, it will navaigate to Azure AI Foundry portal.

   ![](./Images/Image4.png)

1. On the left panel select , select **Deployments**. Click on **+Deploy Model** and select **Deploy Base Model**.

   ![](./Images/Image5.png)

1. Search for **gpt-4o**, select it and click on **Confirm**.

   ![](./Images/Image6.png)

1. Click on **Customize** and provide the following details to deploy a gpt-4o model:

    - Deployment name: gpt4-o
    - Deployment type: Global Standard
    - Model Version: 2024-11-20
    - Set the **Tokens per Minute Rate Limit** to 200k.
    - Leave the other values to default and click on **Deploy**.

   ![](./Images/Image7.png)

1. Once the gpt-4o deployment gets completed, copy the Target URI and Key. Paste these values in a notepad for further use. 

   ![](./Images/Image8.png)

1. Open VS Code from the desktop. Click on **File** and select **Open Folder**.

   ![](./Images/Image9.png)

1. Navigate to the path `C:\LabFiles\`, select **Capstone-Project** and click on **Select Folder**.

   ![](./Images/Image10.png)

1. Expand the src folder, rename the file from **Sample.env** to **.env**.

   ![](./Images/Image11.png)

1. Update the `.env` file with the Azure AI Foundry deployment details and save the file:

    ```
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=Replace with your deployment name
    AZURE_OPENAI_ENDPOINT=Repl ace with your endpoint URL
    AZURE_OPENAI_API_KEY=Replace with your API key
    ```
   ![](./Images/Image12.png)

## Task 2 - Define Agent Personas and Configure Multi-Agent Chat

1. Open the `multi_agent.py` file. This is where you will implement all necessary code for this challenge.
1. Replace the code in the **multi_agent.py** file with the below mentioned code and save.
 
    ```python
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
    ```

    ![](./Images/Image13.png)


1. Click on the ellipses. Select Terminal and choose New Terminal. 

1. // required commands to be added.//

1. Interact with the Multi Agent by giving the below prompt :

   ```
    Build a Calculator App

   ```

1. Wait until the agents interact with themselves and provide a detailed output. Verify the output and differentiate the involvement of different agents in providing the result.   


## Success Criteria

- You have implemented the Multi-Agent Chat system that produces:
  - Software Development Plan and Requirements
  - Source Code in HTML and JavaScript
  - Code Review and Approval

---

## Bonus

- Copy the code from the chat history markdown into matching files on your file system.
- Save HTML content as `index.html` and launch it in your web browser.
- Test if the application functions as the AI described.
- Enhance the app by asking the AI to make it responsive or add new features.
- Experiment with modifying personas to improve results or functionality.

---

## Learning Resources

- [Agent Group Chat with Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-chat?pivots=programming-language-python)
- [MetaGPT](https://github.com/geekan/MetaGPT)
- [AutoGen Multi-Agent Conversational Framework](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/)
- [AutoGen with Semantic Kernel](https://devblogs.microsoft.com/semantic-kernel/autogen-agents-meet-semantic-kernel/)

---

## Conclusion

This challenge demonstrated how to build and coordinate a Multi-Agent System using Azure AI Foundry and Semantic Kernel. By designing distinct personas for Business Analyst, Software Engineer, and Product Owner, and configuring a group chat environment with a termination strategy, you created a collaborative AI workflow capable of gathering requirements, developing code, and performing code reviews. The task structure allows for scalable, decentralized handling of complex problems using autonomous, interactive agents.
