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

1. On the **Azure Open AI (1)** content page, click on **+ create(2)**.

   ![](./Images/Image2.png)

1. Provide the following details and click on **Next**:

    - Subscription: Keep the default subscription **(1)**.

    - Resource Group: Click on Create new (2), provide the name as **openaiagents** and click on OK.

    - Region: East US 2 (3)

    - Name: **OpenAI-<inject key="Deployment ID" enableCopy="false"/>** (4)

    - Pricing Tier: Standard (5)

   ![](./Images/Image3.png)

1. Click on Next twice and click on **Review + Submit**.

1. Review all the values and click on **Create**.

1. Once the deployment is complete, click on **Go to resource**

1. In the Azure OpenAI resource pane, click on Go to Azure AI Foundry portal, it will navaigate to Azure AI Foundry portal.

   ![](./Images/Image4.png)

1. On the left panel select **Deployments**. Click on **+ Deploy Model** and select **Deploy Base Model**.

   ![](./Images/Image5.png)

1. Search for **gpt-4o**, select it and click on **Confirm**.

   ![](./Images/Image6.png)

1. Click on **Customize** and provide the following details to deploy a gpt-4o model:

    - Deployment name: **gpt4-o (1)**
    - Deployment type: **Global Standard (2)**
    - Model Version: **2024-11-20 (3)**
    - Set the **Tokens per Minute Rate Limit** to **200k (4)**.
    - Leave the other values to default and click on **Deploy (5)**.

   ![](./Images/Image7a.png)

1. Once the gpt-4o deployment gets completed, copy the **Target URI** and **Key**. **Paste** these values in a notepad for further use. 

   ![](./Images/Image8.png)

1. Open VS Code from the desktop. Click on **File** and select **Open Folder**.

   ![](./Images/Image9.png)

1. Navigate to the path `C:\LabFiles\`, select **Capstone-Project** and click on **Select Folder**.

   ![](./Images/Image10a.png)

1. Select the **checkbox** and click **'I trust the authors'** to proceed.

   ![](./Images/Image11a.png)

1. Expand the src folder, rename the file from **Sample.env** to **.env**.

   ![](./Images/Image12a.png)

1. Update the `.env` file with the Azure AI Foundry deployment details and save the file:

    ```
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=Replace with your deployment name
    AZURE_OPENAI_ENDPOINT=Replace with your endpoint URL
    AZURE_OPENAI_API_KEY=Replace with your API key
    ```
   ![](./Images/Image13a.png)

## Task 2 - Create a GitHub Repository and Generate a PAT Token

1. Sign in to GitHub at [https://github.com](https://github.com).  

1. Create a New Repository with the name `Capstone-Project-<inject key="Deployment ID" enableCopy="false"/>` **(1)**. Let the repo be set to **Public (2)** and click on **Create Repository (3)**.

   ![](./Images/Image16.png)

2. Click your profile picture at the top-right corner and select **Settings** from the dropdown menu.  

   ![](./Images/Image.png)

4. In the left sidebar, click **Developer settings**.  
5. Click **Personal access tokens**.  
6. Click **Tokens (classic)**.  
7. Click **Generate new token (classic)**.  
8. Enter a name for your token (e.g., `MyToken`).  
9. Set an expiration date for the token.  
10. Select the required scopes (e.g., check `repo` and `workflow`).  
11. Scroll down and click **Generate token**.  
12. Copy the generated token now. You won’t see it again.  

---

## Important

- Use this token instead of your password when authenticating GitHub.  
- Keep your token safe and do not share it.  
- Revoke the token immediately if you suspect it is compromised.


## Task 3 - Define Agent Personas and Configure Multi-Agent Chat

1. Open the `multi_agent.py` file. This is where you will implement all necessary code for this challenge.
1. Replace the code in the **multi_agent.py** file with code from the below link and save.
    ```
    https://docs-api.cloudlabs.ai/repos/raw.githubusercontent.com/CloudLabsAI-Azure/Capstone-Project/refs/heads/soln-guide/src/ui/multi_agent.py
    ```

    ![](./Images/Image14a.png)


1. Create a file named `push_to_github.sh` under the `src/ui` directory and paste the code from below link and save.

    ```
    https://docs-api.cloudlabs.ai/repos/raw.githubusercontent.com/CloudLabsAI-Azure/Capstone-Project/refs/heads/soln-guide/src/ui/push_to_github.sh
    ```

    ![](./Images/Image15.png)

1. Update the following env variables in `.env` file:
    ```
    GITHUB_REPO_URL=Replace with your Github Repo
    GITHUB_PAT=Replace with your Github pat token
    GIT_USER_EMAIL=Replace with your Github email
    GITHUB_USERNAME=Replace with your Github username
    ```

1. Click on **Terminal>New Terminal** and run the following command:-

    ```
    azd auth login
    ```

1. Sign in using the following credentials:-
    - **Email/Username**: <inject key="AzureAdUserEmail"></inject>
    - **Password**: <inject key="AzureAdUserPassword"></inject>

1. Run the following command to provision the web app and required resources to azure:-

    ```
    azd up
    ```

## Task 3 - 

1. Navigate to azure portal, and select the newly created rg.
1. open the container app with prefix **dev-ui-** and click on the application url
1. the app will start, try running the following prompt
    ```
    Create code for simple calculator
    ```
1. once it runs , type approved to approve the code and push to github.
1. the code will be pushed to github.

## Success Criteria

- You have implemented the Multi-Agent Chat system that produces:
    - Generation of complete source code in HTML and JavaScript for the requested application
    - Thorough code review and approval process by User
    - Automated deployment of the application to Azure
    - Automated code push to a Git repository upon user approval

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
