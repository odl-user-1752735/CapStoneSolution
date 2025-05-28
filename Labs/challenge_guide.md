# Desafío - Sistemas Multi-Agente

## Introducción

Los Sistemas Multi-Agente (MAS) consisten en múltiples agentes autónomos, cada uno con objetivos, comportamientos y áreas de responsabilidad distintas. Estos agentes operan de forma independiente, tomando decisiones basadas en su conocimiento local y entorno. Sin embargo, también pueden comunicarse y compartir información entre sí, ya sea cooperando o compitiendo dependiendo de sus objetivos. Los MAS se utilizan típicamente en escenarios donde las tareas están distribuidas entre múltiples entidades y el sistema se beneficia de la descentralización. Las aplicaciones comunes incluyen la gestión del tráfico, equipos robóticos, IA distribuida y sistemas en red donde se requiere coordinación sin depender de un controlador central.

En este desafío, crearás un `Multi-Agent System` que acepta la solicitud de un usuario y la procesa a través de una colección de agentes, cada uno diseñado con una persona específica y área de especialización. Los agentes analizarán individualmente la solicitud y contribuirán con sus respuestas basándose en sus responsabilidades definidas. La salida final será una colección consolidada de respuestas de todos los agentes, abordando colaborativamente la consulta del usuario de una manera que refleje la perspectiva única de cada persona.


## Objetivos del Desafío:

1. **Despliegue del Servicio Azure OpenAI:**

    - Configurar una instancia del Servicio Azure OpenAI con tamaño de SKU Standard `S0`.

        > **Nota:** Asegúrate de que la región esté configurada en **East US**.

    - Desplegarlo en un grupo de recursos con prefijo `openaiagents`.

    - Obtener la clave y el endpoint de Azure OpenAI.
 

1. **Desplegar Modelos de Azure OpenAI:**

    - Azure OpenAI proporciona un portal web llamado **Azure AI Foundry Portal** que puedes usar para desplegar, administrar y explorar modelos. Comenzarás tu exploración de Azure OpenAI utilizando Azure AI Foundry para desplegar un modelo.

    - Inicia el portal Azure AI Foundry desde el panel de resumen y despliega un modelo de Azure OpenAI, es decir, `gpt-4o`.

        >- **Nota:** Asegúrate de que los despliegues se nombren **gpt-4o**.  
        >- **Nota:** Verifica que el Tipo de Despliegue esté configurado como **Global Standard** y utiliza **2024-11-20** para la versión del modelo.

    - Obtén el **nombre del despliegue** y la **versión API** del modelo.

        >- **Pista:** La versión API puede obtenerse desde el URI de destino.


## Tarea 1 - Despliegue del Modelo Azure AI Foundry y Configuración del Entorno

1. Actualiza el archivo `.env` con los detalles del despliegue de Azure AI Foundry:

    ```
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=Reemplaza con el nombre de tu despliegue
    AZURE_OPENAI_ENDPOINT=Reemplaza con la URL de tu endpoint
    AZURE_OPENAI_API_KEY=Reemplaza con tu clave API
    AZURE_OPENAI_API_VERSION=Reemplaza con la versión de tu API
    ```


## Tarea 2 - Definir las Personalidades de los Agentes y Configurar el Chat Multi-Agente

1. Abre el archivo `multi_agent.py`. Aquí es donde implementarás todo el código necesario para este desafío.

2. Crea las personalidades para los tres agentes con las siguientes instrucciones:

    - **Persona de Analista de Negocios**

        ```
        You are a Business Analyst which will take the requirements from the user (also known as a 'customer') and create a project plan for creating the requested app. The Business Analyst understands the user requirements and creates detailed documents with requirements and costing. The documents should be usable by the SoftwareEngineer as a reference for implementing the required features, and by the Product Owner for reference to determine if the application delivered by the Software Engineer meets all of the user's requirements.
        ```

    - **Persona de ingeniero de software**

        ```
        You are a Software Engineer, and your goal is create a web app using HTML and JavaScript by taking into consideration all the requirements given by the Business Analyst. The application should implement all the requested features. Deliver the code to the Product Owner for review when completed. You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.
        ```

    - **Persona del propietario del producto**

        ```
        You are the Product Owner which will review the software engineer's code to ensure all user  requirements are completed. You are the guardian of quality, ensuring the final product meets all specifications. IMPORTANT: Verify that the Software Engineer has shared the HTML code using the format ```html [code] ```. This format is required for the code to be saved and pushed to GitHub. Once all client requirements are completed and the code is properly formatted, reply with 'READY FOR USER APPROVAL'. If there are missing features or formatting issues, you will need to send a request back to the SoftwareEngineer or BusinessAnalyst with details of the defect.
        ```

1. Crea un `ChatCompletionAgent` para cada una de las personas mencionadas anteriormente. Cada agente debe tener:
    - Instrucciones (el prompt de la persona)
    - Un Nombre único (solo letras, sin espacios ni caracteres especiales)
    - Una referencia a un objeto `Kernel`

1. Crea un objeto `AgentGroupChat` para enlazar los tres agentes. Pasa:
    - Un arreglo con los tres agentes
    - `ExecutionSettings` con una `TerminationStrategy` configurada como una instancia de `ApprovalTerminationStrategy`

1. Implementa el método `should_agent_terminate` en la clase `ApprovalTerminationStrategy`. Los agentes deben terminar cuando el Usuario devuelva "APPROVED" en el historial del chat.


## Tarea 3 - Activar Git Push tras la Aprobación del Usuario

Agrega lógica para que cuando el usuario envíe "APPROVED" en el chat, se active un script Bash que haga push del código escrito por el agente Software Engineer a un repositorio Git.

1. Después de implementar el método `should_agent_terminate` para detectar "APPROVED", añade un callback o paso de post-procesamiento que se ejecute cuando se cumpla esta condición.
2. Extrae el código HTML proporcionado por el agente Software Engineer del historial del chat.
3. Guarda el código extraído en un archivo (por ejemplo, `index.html`).
4. Crea un script Bash (por ejemplo, `push_to_git.sh`) que haga staging, commit y push del archivo al repositorio Git deseado:
5. En tu código Python, usa el módulo `subprocess` para llamar a este script cuando se detecte "APPROVED":
6. Asegúrate de que tu entorno tenga las credenciales Git necesarias configuradas para realizar push sin interacción.

Esta automatización asegura que una vez que el Product Owner (o usuario) envíe "APPROVED", el código más reciente se suba automáticamente a tu repositorio Git.

## Tarea 4 - Ejecutar la Conversación Multi-Agente y Validar el Flujo de Trabajo

1. Implementa el código para enviar un mensaje del usuario al grupo de agentes usando `add_chat_message` sobre el objeto `AgentGroupChat`. El mensaje debe incluir:
    - `AuthorRole.User` como autor
    - El contenido del mensaje del chat basado en la entrada del usuario

2. Itera sobre las respuestas del `AgentGroupChat` usando un bucle asíncrono, e imprime cada mensaje a medida que llega:

    ```python
    async for content in chat.invoke():
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
    ```

3. Ejecuta tu aplicación y proporciona una solicitud para construir una aplicación calculadora. Observa cómo el Business Analyst, Software Engineer y Product Owner colaboran para planear, construir y aprobar la solución.


## Tarea 5 - Desplegar la aplicación en Azure

### Desplegando la aplicación en Azure usando Container Registry y Azure App Service

Para alojar tu aplicación en línea usando Azure, sigue estos pasos para contenerizar tu aplicación, enviarla a Azure Container Registry (ACR) y desplegarla usando Azure App Service:

1. Abre una terminal e inicia sesión en Azure Developer CLI usando el siguiente comando:

    ```bash
    azd auth login
    ```

1. Despliega los recursos requeridos en Azure ejecutando:

    ```bash
    azd up
    ```

1. Al ejecutar el comando **azd up**, se te pedirá que proporciones detalles de configuración de forma interactiva. Proporciona los siguientes valores cuando se te solicite:

   - **Nombre Único del Entorno**: Ingresa **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(1)**.
   - **Suscripción de Azure a usar**: Elige la suscripción predeterminada **(2)** que aparece y presiona **Enter**.
   - **Parámetro de Infraestructura Location**: Selecciona **East US 2** **(3)** de las opciones y presiona **Enter**.
   - **Parámetro de Infraestructura ResourceGroupName**: Escribe **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(4)** y presiona **Enter**.
   - **Grupo de Recursos a usar**: Selecciona **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>** **(5)** de las opciones y presiona **Enter**.

1. Abre el portal de Azure y navega al grupo de recursos **CapstoneEnv-<inject key="Deployment ID" enableCopy="false"/>**.  
2. Localiza el recurso de la aplicación de contenedor desplegada.  
3. Copia la URL del endpoint de la aplicación de contenedor.  
4. Accede a la aplicación web visitando este endpoint en tu navegador y verifica que la aplicación funcione según lo esperado.  


## Criterios de Éxito

- Has implementado el sistema de Chat Multi-Agente que produce:
    - Generación de código fuente completo en HTML y JavaScript para la aplicación solicitada.
    - Revisión y proceso de aprobación exhaustivos del código por parte del Usuario.
    - Despliegue automatizado de la aplicación en Azure.
    - Push automatizado del código a un repositorio Git tras la aprobación del usuario.


---

## Bonus

- Copia el código del historial del chat en archivos correspondientes en tu sistema de archivos.
- Guarda el contenido HTML como `index.html` y ábrelo en tu navegador web.
- Prueba si la aplicación funciona según lo descrito por la IA.
- Mejora la aplicación pidiéndole a la IA que la haga responsiva o que añada nuevas funcionalidades.
- Experimenta modificando las personalidades de los agentes para mejorar resultados o funcionalidades.


---

## Recursos de aprendizaje

- [Agent Group Chat with Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-chat?pivots=programming-language-python)
- [MetaGPT](https://github.com/geekan/MetaGPT)
- [AutoGen Multi-Agent Conversational Framework](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/)
- [AutoGen with Semantic Kernel](https://devblogs.microsoft.com/semantic-kernel/autogen-agents-meet-semantic-kernel/)
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

---

## Conclusión

Este desafío demostró cómo construir y coordinar un Sistema Multi-Agente utilizando Azure AI Foundry y Semantic Kernel. Al diseñar personalidades distintas para el Analista de Negocios, el Ingeniero de Software y el Propietario del Producto, y configurar un entorno de chat grupal con una estrategia de terminación, creaste un flujo de trabajo colaborativo de IA capaz de recopilar requisitos, desarrollar código y realizar revisiones de código. La estructura de la tarea permite un manejo escalable y descentralizado de problemas complejos usando agentes autónomos e interactivos.
