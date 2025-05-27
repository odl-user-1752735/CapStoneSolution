# 課題 - マルチエージェントシステム

## 紹介

マルチエージェントシステム(MAS)は、それぞれが異なる目標、動作、および責任範囲を持つ複数の自律エージェントで構成されています。これらのエージェントは独立して動作し、地域の知識と環境に基づいて意思決定を行います。しかし、彼らはまた、彼らの目的に応じて協力したり競争したりして、互いにコミュニケーションを取り、情報を共有することもできます。MAS は通常、タスクが複数のエンティティに分散され、システムが分散化の恩恵を受けるシナリオで使用されます。一般的なアプリケーションには、トラフィック管理、ロボットチーム、分散型AI、中央コントローラーに依存しない調整が必要なネットワークシステムなどがあります。

この課題では、ユーザーのリクエストを受け入れ、それぞれが特定のペルソナと専門分野で設計されたエージェントのコレクションを通じて処理するマルチエージェントシステムを作成します。エージェントは個別にリクエストを分析し、定義された責任に基づいて応答を提供します。最終的な出力は、すべてのエージェントからの回答の統合コレクションであり、各ペルソナの独自の視点を反映する方法でユーザーのクエリに協力して対処します。


## チャレンジ目標:

1. **Azure OpenAI Service のデプロイ:**

    - SKU サイズ Standard S0 の Azure OpenAI Service インスタンスを設定します。

        > **手記:** リージョンが [米国東部] に設定されていることを確認します。

    - `openaiagents` というプレフィックスが付いたリソース グループにデプロイします。

    - Azure OpenAI キーとエンドポイントを取得します。

1. **Azure OpenAI モデルをデプロイします。**
   
    - Azure OpenAI には、モデルのデプロイ、管理、探索に使用できる Azure AI Foundry Portal という名前の Web ベースのポータルが用意されています。Azure OpenAI の調査を開始するには、Azure AI Foundry を使用してモデルをデプロイします。
    
    - 概要ウィンドウから Azure AI Foundry ポータルを起動し、Azure OpenAI モデル (gpt-4o) をデプロイします。

        >- **手記:** デプロイの名前が gpt-4o であることを確認します。
        >- **手記:** [デプロイの種類] が [グローバル標準] に設定されていることを確認し、モデル バージョンに 2024-11-20 を使用します。

    - モデルのデプロイ名と API バージョンをフェッチします。

        >- **ヒント:** API バージョンは、ターゲット URI から取得できます。


## タスク 1 - Azure AI Foundry モデルのデプロイと環境の構成

1. Azure AI Foundry デプロイの詳細で .env ファイルを更新します。

    ```
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=Replace with your deployment name
    AZURE_OPENAI_ENDPOINT=Replace with your endpoint URL
    AZURE_OPENAI_API_KEY=Replace with your API key
    AZURE_OPENAI_API_VERSION=Replace with your API version
    ```

---

## タスク 2 - エージェントのペルソナの定義とマルチエージェント チャットの構成

1. `multi_agent.py` ファイルを開きます。ここで、このチャレンジに必要なすべてのコードを実装します。

1. 次の手順で、3 人のエージェントのペルソナを作成します。

    - **ビジネスアナリストのペルソナ**

        ```
        You are a Business Analyst which will take the requirements from the user (also known as a 'customer') and create a project plan for creating the requested app. The Business Analyst understands the user requirements and creates detailed documents with requirements and costing. The documents should be usable by the SoftwareEngineer as a reference for implementing the required features, and by the Product Owner for reference to determine if the application delivered by the Software Engineer meets all of the user's requirements.
        ```

    - **ソフトウェアエンジニアのペルソナ**

        ```
        You are a Software Engineer, and your goal is create a web app using HTML and JavaScript by taking into consideration all the requirements given by the Business Analyst. The application should implement all the requested features. Deliver the code to the Product Owner for review when completed. You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.
        ```

    - **プロダクトオーナーペルソナ**

        ```
        You are the Product Owner which will review the software engineer's code to ensure all user  requirements are completed. You are the guardian of quality, ensuring the final product meets all specifications. IMPORTANT: Verify that the Software Engineer has shared the HTML code using the format ```html [code] ```. This format is required for the code to be saved and pushed to GitHub. Once all client requirements are completed and the code is properly formatted, reply with 'READY FOR USER APPROVAL'. If there are missing features or formatting issues, you will need to send a request back to the SoftwareEngineer or BusinessAnalyst with details of the defect.
        ```

1. 上記の各ペルソナに対して `ChatCompletionAgent` を作成します。各エージェントには、次のものが必要です。
    - 指示 (ペルソナ プロンプト)
    - 意の名前 (文字のみ、スペースや特殊文字は使用不可)
    - `Kernel` オブジェクトへの参照

1. `AgentGroupChat` オブジェクトを作成して、3 人のエージェントを結び付けます。通る：
    - 3 つのエージェントの配列
    - `ExecutionSettings` と `TerminationStrategy` のインスタンスに設定された `TerminationStrategy`
1. `should_agent_terminate` メソッドを `ApprovalTerminationStrategy` クラスに実装します。エージェントは、ユーザーがチャット履歴で `APPROVED` を返したときに終了する必要があります。

## タスク 3 - ユーザー承認時の Git プッシュのトリガー

ユーザーがチャットで「APPROVED」を送信すると、Bashスクリプトがトリガーされ、ソフトウェアエンジニアエージェントが記述したコードをGitリポジトリにプッシュするロジックを追加します。

1. `APPROVED` を検出する `should_agent_terminate` メソッドを実装した後、この条件が満たされたときに実行されるコールバックまたは後処理ステップを追加します。
2. ソフトウェアエンジニアエージェントから提供されたHTMLコードをチャット履歴から抽出します。
3. 抽出したコードをファイル(index.htmlなど)に保存します。
4. Bashスクリプト(push_to_git.shなど)を作成し、ファイルをステージング、コミット、目的のGitリポジトリにプッシュします。
5. Python コードで、subprocess モジュールを使用して、"APPROVED" が検出されたときにこのスクリプトを呼び出します。
6. お使いの環境で、非対話型プッシュに必要な Git 資格情報が構成されていることを確認します。

This automation ensures that once the Product Owner (or user) sends "APPROVED", the latest code is automatically pushed to your Git repository.

## Task 4 - Run the Multi-Agent Conversation and Validate Workflow

1. Implement the code to send a user message to the agent group using `add_chat_message` on the `AgentGroupChat` object. The message should include:
    - `AuthorRole.User` as the author
    - The chat message contents from the user's input

1. Iterate through the responses from the `AgentGroupChat` using an asynchronous loop, and print each message as it arrives:

    ```python
    async for content in chat.invoke():
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
    ```

1. Run your application and provide a request to build a calculator app. Observe how the Business Analyst, Software Engineer, and Product Owner collaborate to plan, build, and approve the solution.

## Task 5 - Deploy the app to Azure
### Deploying the App to Azure Using Container Registry and Azure App Service

To host your app online using Azure, follow these steps to containerize your application, push it to Azure Container Registry (ACR), and deploy it using Azure App Service:

1. Open a terminal and sign in to the Azure Developer CLI using the following command:

    ```bash
    azd auth login
    ```

1. Deploy the required resources to Azure by running:

    ```bash
    azd up
    ```

1. When running the **azd up** command, you'll be asked to provide configuration details interactively. Provide the following values when prompted:

   - **Unique Environment Name**: Enter **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(1)**.
   - **Azure Subscription to use**: Choose the default subscription **(2)** that appears and press **Enter**.
   - **Location Infrastructure Parameter**: Select **East US 2** **(3)** from the options and press **Enter**.
   - **ResourceGroupName Infrastructure Parameter**: Type **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(4)** and press **Enter**.
   - **Resource Group to use**: Select **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(5)** from the options and press **Enter**.

1. Open the Azure portal and navigate to the resource group **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>**.
2. Locate the deployed container app resource.
3. Copy the endpoint URL of the container app.
4. Access the web app by visiting this endpoint in your browser and verify that the application functions as expected.
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
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

---

## Conclusion

This challenge demonstrated how to build and coordinate a Multi-Agent System using Azure AI Foundry and Semantic Kernel. By designing distinct personas for Business Analyst, Software Engineer, and Product Owner, and configuring a group chat environment with a termination strategy, you created a collaborative AI workflow capable of gathering requirements, developing code, and performing code reviews. The task structure allows for scalable, decentralized handling of complex problems using autonomous, interactive agents.
