## Guia de Solução
# Sistemas Multi-Agente - Guia de Solução

## Introdução

Os Sistemas Multiagentes (MAS) consistem em vários agentes autônomos, cada um com objetivos, comportamentos e áreas de responsabilidade distintos. Estes agentes operam de forma independente, tomando decisões com base no seu conhecimento local e ambiente. No entanto, também podem comunicar e partilhar informações entre si, cooperando ou competindo em função dos seus objetivos. O MAS é normalmente usado em cenários em que as tarefas são distribuídas por várias entidades e o sistema se beneficia da descentralização. As aplicações comuns incluem gestão de tráfego, equipas robóticas, IA distribuída e sistemas em rede onde a coordenação é necessária sem depender de um controlador central.

Neste desafio, você criará um Sistema Multiagente que aceita a solicitação de um usuário e a processa por meio de uma coleção de agentes, cada um projetado com uma persona específica e área de especialização. Os agentes analisarão individualmente o pedido e contribuirão com as suas respostas com base nas suas responsabilidades definidas. O resultado final será uma coleção consolidada de respostas de todos os agentes, abordando colaborativamente a consulta do usuário de uma forma que reflita a perspetiva única de cada persona.

## Tarefa 1 - Implantação do Modelo Azure AI Foundry e Configuração do Ambiente

1. Navegue para `https://portal.azure.com` e faça login com suas credenciais Azure.

    - **Email/Utilizador**: <inject key="AzureAdUserEmail"></inject>
    - **Palavra-passe**: <inject key="AzureAdUserPassword"></inject>

1. Pesquise e selecione Open AI.

   ![](./Images/Image1.png)

1. Na página de conteúdo **Azure Open AI (1)**, clique em **+ criar (2)**.

   ![](./Images/Image2.png)

1. Forneça os seguintes detalhes e clique em **Seguinte**:

    - Subscrição: Mantenha a subscrição predefinida **(1)**.

    - Grupo de Recursos: Clique em **Criar novo (2)**, forneça o nome **openaiagents** e clique em OK.

    - Região: **East US 2 (3)**

    - Nome: **OpenAI-<inject key="Deployment ID" enableCopy="false"/>** **(4)**

    - Nível de Preço: **Standard SO (5)**

   ![](./Images/Image3.png)

1. Clique em Seguinte duas vezes e depois em **Rever + Enviar**.

1. Reveja todos os valores e clique em **Criar**.

1. Quando a implantação estiver concluída, clique em **Ir para o recurso**.

1. No painel do recurso Azure OpenAI, clique em **Ir para o portal Azure AI Foundry**, que irá navegar para o portal Azure AI Foundry.

   ![](./Images/Image4.png)

1. No painel esquerdo selecione **Implantações (1)**. Clique em **+ Implantar Modelo (2)** e selecione **Implantar Modelo Base (3)**.

   ![](./Images/Image5.png)

1. Pesquise por **gpt-4o (1)**, **selecione-o (2)** e clique em **Confirmar (3)**.

   ![](./Images/Image6.png)

1. Clique em **Personalizar** e forneça os seguintes detalhes para implantar um modelo gpt-4o:

    - Nome da implantação: **gpt4-o (1)**
    - Tipo de implantação: **Global Standard (2)**
    - Versão do Modelo: **2024-11-20 (3)**
    - Defina o **Limite de Tokens por Minuto** para **200k (4)**.
    - Deixe os outros valores como padrão e clique em **Implantar (5)**.

   ![](./Images/Image7a.png)

1. Quando a implantação do gpt-4o for concluída, copie o **URI de Destino (1)** e a **Chave (2)**. **Cole** estes valores num bloco de notas para uso posterior.

   ![](./Images/Image8.png)

1. Abra o VS Code na sua VM de laboratório. Clique em **Ficheiro (1)** e selecione **Abrir Pasta (2)**.

   ![](./Images/Image9.png)

1. Navegue até ao caminho `C:\LabFiles\` **(1)**, selecione **CAPSTONE-PROJECT (2)** e clique em **Selecionar Pasta (3)**.

   ![](./Images/Image10a.png)

1. Selecione a **caixa de verificação (1)** e clique em **Sim, confio nos autores (2)** para prosseguir.

   ![](./Images/Image11a.png)

1. Expanda a pasta **src/ui**, renomeie o ficheiro de **Sample.env** para **.env**.

   ![](./Images/Image12a.png)

1. Atualize o ficheiro `.env` com os detalhes da implantação do Azure AI Foundry e guarde o ficheiro:

    ```
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=Substitua pelo nome da sua implantação
    AZURE_OPENAI_ENDPOINT=Substitua pela URL do seu endpoint
    AZURE_OPENAI_API_KEY=Substitua pela sua chave API
    ```
   ![](./Images/Image13a.png)


## Tarefa 2 - Criar um Repositório GitHub e Gerar um Token PAT

1. Inicie sessão no GitHub em [https://github.com](https://github.com).

1. Crie um novo repositório com o nome **Capstone-Project-<inject key="Deployment ID" enableCopy="false"/>** **(1)**. Defina a visibilidade do repositório para **Público (2)** e clique em **Criar Repositório (3)**.

   ![](./Images/Image16.png)

1. Após a criação do novo repositório, **copie o URL** do seu repositório e cole num bloco de notas para uso futuro.

   ![](./Images/Image25.png)

1. Clique na sua **foto de perfil (1)** no canto superior direito e selecione **Configurações (2)** no menu dropdown.

   ![](./Images/Image17.png)

1. No menu lateral esquerdo, clique em **<> Definições de Programador**.

   ![](./Images/Image18.png)

1. Expanda **Tokens de acesso pessoal** no painel esquerdo. Selecione **Tokens de acesso personalizado (Fine-grained tokens) (1)** e clique em **Gerar novo token (2)**.

   ![](./Images/Image19.png)

1. Insira **<inject key="Deployment ID" enableCopy="false"/>-PAT-RepoAccess** **(1)** como nome do seu token. Defina a data de expiração para **30 dias (2)**.

   ![](./Images/Image20.png)

1. Desça até **Acesso ao repositório** e clique em **Apenas repositórios selecionados (1)**. Procure o repositório **Capstone-Project-<inject key="Deployment ID" enableCopy="false"/>** **(2)** e **selecione-o (3)**.

   ![](./Images/Image21.png)

1. Em **Permissões**, expanda **Permissões do Repositório (1)**. Dê acesso de **Leitura e Escrita (3)** para **Conteúdos (2)** nas permissões do repositório.

   ![](./Images/Image22.png)

1. Desça até ao final da página, clique em **Gerar token (1)** e, na janela popup, reveja as permissões e clique novamente em **Gerar token (2)**.

   ![](./Images/Image23.png)

1. **Copie (1)** o token gerado e **cole** num bloco de notas para uso futuro.

   ![](./Images/Image24.png)

## Tarefa 3 - Definir Personas dos Agentes e Configurar o Chat Multi-Agente

1. Abra o ficheiro `multi_agent.py`. É aqui que irá implementar todo o código necessário para este desafio.

1. Substitua o código no ficheiro **multi_agent.py** pelo código do link abaixo e guarde o ficheiro.

    ```
    https://docs-api.cloudlabs.ai/repos/raw.githubusercontent.com/CloudLabsAI-Azure/Capstone-Project/refs/heads/soln-guide/src/ui/multi_agent.py
    ```

    ![](./Images/Image14a.png)

1. Crie um ficheiro chamado `push_to_github.sh` dentro do diretório `src/ui`. Cole o código do link abaixo e guarde o ficheiro.

    ```
    https://docs-api.cloudlabs.ai/repos/raw.githubusercontent.com/CloudLabsAI-Azure/Capstone-Project/refs/heads/soln-guide/src/ui/push_to_github.sh
    ```

    ![](./Images/Image15.png)

1. Atualize as seguintes variáveis de ambiente no ficheiro `.env` com os valores que copiou na Tarefa 2 e guarde o ficheiro.

    ```
    GITHUB_REPO_URL=Substitua pelo URL do seu repositório Github
    GITHUB_PAT=Substitua pelo seu token PAT do Github
    GIT_USER_EMAIL=Substitua pelo seu email do Github
    GITHUB_USERNAME=Substitua pelo seu nome de utilizador do Github
    ```

    ![](./Images/Image27.png)


1. No ficheiro `.env`, clique em **CRLF (1)** na barra de estado inferior e altere para **LF (2)** selecionando essa opção. Guarde o ficheiro após fazer esta alteração.

    ![](./Images/Image35.png)

1. Verifique que também está selecionado **LF** no ficheiro `push_to_github.sh`.

    ![](./Images/Image36.png)

1. Clique nas **reticências (1)**. Selecione **Terminal (2)** e escolha **Novo Terminal (3)**.

    ![](./Images/Image26.png)

1. Execute o seguinte comando:

    ```
    azd auth login
    ```

    ![](./Images/Image28.png)

1. Inicie sessão usando as seguintes credenciais:  
    - **Email/Utilizador**: <inject key="AzureAdUserEmail"></inject>  
    - **Password**: <inject key="AzureAdUserPassword"></inject>

1. Execute o seguinte comando para provisionar a aplicação web e os recursos necessários no Azure:

    ```
    azd up
    ```

1. Ao executar o comando **azd up**, será solicitado que forneça detalhes de configuração de forma interativa. Forneça os seguintes valores quando solicitado:

   - **Nome Único do Ambiente**: Introduza **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(1)**.
   - **Assinatura Azure a utilizar**: Escolha a assinatura padrão **(2)** que aparecer e pressione **Enter**.
   - **Parâmetro de Localização da Infraestrutura**: Selecione **East US 2** **(3)** entre as opções e pressione **Enter**.
   - **Parâmetro ResourceGroupName da Infraestrutura**: Digite **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(4)** e pressione **Enter**.
   - **Grupo de Recursos a utilizar**: Selecione **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(5)** entre as opções e pressione **Enter**.

   ![](./Images/Image38.png)

   - **Nota:** Aguarde cerca de 5 minutos até que o comando termine completamente.

## Tarefa 4 - Geração de Código Multi-Agente e Integração com Repositório

1. Aceda ao portal Azure e selecione o Grupo de Recursos recém-criado com o nome **rg-CapstoneEnv<inject key="Deployment ID" enableCopy="false"/>**.

1. Abra a aplicação de contentor com o prefixo **dev-ui-**.

    ![](./Images/Image30.png)

1. Clique na **URL da Aplicação** presente na página de visão geral da aplicação de contentor.

    ![](./Images/Image31.png)

1. A aplicação de chat Streamlit será aberta. Tente fornecer o **seguinte prompt (1)** no chat e clique em **send**.

    ```
    Create code for simple calculator
    ```
   - **Nota:** Aguarde até que os agentes colaborem e forneçam uma resposta.

    ![](./Images/Image32.png)

1. Assim que a aplicação executar e apresentar o código e outros detalhes, digite **approved (1)** e selecione **send (2)** para aprovar o código. No final do chat, poderá observar que o código está a ser enviado para o repositório após a aprovação.

    ![](./Images/Image33.png)

    ![](./Images/Image34.png)

1. Navegue até ao repositório **Capstone-Project-<inject key="Deployment ID" enableCopy="false"/>** e verifique que o ficheiro `generated_app.html` foi criado, contendo o código da sua calculadora simples.

    ![](./Images/Image37.png)

## Critérios de Sucesso

- Você implementou o sistema de Chat Multi-Agente que produz:
    - Geração de código-fonte completo em HTML e JavaScript para a aplicação solicitada
    - Processo completo de revisão de código e aprovação pelo Usuário
    - Implantação automatizada da aplicação no Azure
    - Envio automatizado do código para um repositório Git após a aprovação do usuário

## Bônus

- Copie o código do histórico do chat em arquivos correspondentes no seu sistema de arquivos.
- Salve o conteúdo HTML como `index.html` e abra-o no seu navegador.
- Teste se a aplicação funciona conforme descrito pela IA.
- Melhore o aplicativo pedindo para a IA torná-lo responsivo ou adicionar novos recursos.
- Experimente modificar as personas para melhorar os resultados ou funcionalidades.

## Recursos de Aprendizado

- [Agent Group Chat com Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-chat?pivots=programming-language-python)
- [MetaGPT](https://github.com/geekan/MetaGPT)
- [AutoGen Multi-Agent Conversational Framework](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/)
- [AutoGen com Semantic Kernel](https://devblogs.microsoft.com/semantic-kernel/autogen-agents-meet-semantic-kernel/)

## Conclusão

Este desafio demonstrou como construir e coordenar um Sistema Multi-Agente usando Azure AI Foundry e Semantic Kernel. Ao projetar personas distintas para Analista de Negócios, Engenheiro de Software e Product Owner, e configurar um ambiente de chat em grupo com uma estratégia de encerramento, você criou um fluxo de trabalho colaborativo de IA capaz de coletar requisitos, desenvolver código e realizar revisões de código. A estrutura da tarefa permite o gerenciamento escalável e descentralizado de problemas complexos usando agentes autônomos e interativos.

# Você concluiu com sucesso o Laboratório !!
