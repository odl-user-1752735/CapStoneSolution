# 挑战实验

# 毕业项目

### 总预计时长：4小时

## 概述

在本次挑战中，你将使用基于 Chainlit 的对话应用程序，该应用程序利用 Dapr 的发布-订阅（pub/sub）消息模型，通过智能 AI 代理协调客户服务升级。该解决方案无缝集成了多个 Azure 服务——包括用于自然语言处理的 Azure OpenAI、用于数据持久化的 Cosmos DB，以及用于可靠消息传递的 Azure Service Bus。当 AI 代理达到解决上限时，系统会智能地将案例升级到人工支持代理，通过触发一个 Logic Apps 工作流，发送电子邮件审批请求。本动手实验将为你提供宝贵的见解，了解如何将 AI 驱动的对话界面、事件驱动架构和工作流自动化相结合，构建响应迅速、可扩展且具备人性化感知的客户支持系统。


## 目标

在本实验结束时，你将能够：

- **多代理业务角色工作流**：体验涉及三种不同角色的协作工作流——Software Engineer、Product Owner 和 User。Software Engineer 编写并提交代码，Product Owner 审核并批准更改，批准后，解决方案将自动推送到 GitHub 进行部署和版本控制。

## 前提条件

参与者应具备：

- 对 Azure 服务（如 Azure OpenAI 和模型）的基本了解。
- 使用 Azure Developer CLI (AZD) 部署应用程序的经验。
- 接触过对话式 AI 工具，如 Streamlit 或类似框架。


## Explanation of Components

- **Azure OpenAI**: A cloud-based service that provides access to advanced language models, enabling natural language processing, content generation, and conversational AI capabilities. It allows you to integrate powerful AI-driven features into your applications securely and at scale.
- **Azure Container Apps**: A serverless container hosting service that allows you to deploy and scale microservices and containerized applications without managing infrastructure.

## Getting Started with the lab

Welcome to your Azure Agentic AI Workshop, Let's begin by making the most of this experience:

## Accessing Your Lab Environment

Once you're ready to dive in, your virtual machine and **lab guide** will be right at your fingertips within your web browser.

![Access Your VM and Lab Guide](./media/agg1.png)

## Lab Guide Zoom In/Zoom Out

To adjust the zoom level for the environment page, click the **A↕ : 100%** icon located next to the timer in the lab environment.

![](./media/agg2.png)

## Virtual Machine & Lab Guide

Your virtual machine is your workhorse throughout the workshop. The lab guide is your roadmap to success.

## Exploring Your Lab Resources

To get a better understanding of your lab resources and credentials, navigate to the **Environment** tab.

![Explore Lab Resources](./media/agg3.png)

## Utilizing the Split Window Feature

For convenience, you can open the lab guide in a separate window by selecting the **Split Window** button from the Top right corner.

![Use the Split Window Feature](./media/agg4.png)

## Managing Your Virtual Machine

Feel free to **start, stop, or restart (2)** your virtual machine as needed from the **Resources (1)** tab. Your experience is in your hands!

![Manage Your Virtual Machine](./media/agg5.png)

<!-- ## Lab Duration Extension

1. To extend the duration of the lab, kindly click the **Hourglass** icon in the top right corner of the lab environment.

    ![Manage Your Virtual Machine](./media/media/gext.png)

    >**Note:** You will get the **Hourglass** icon when 10 minutes are remaining in the lab.

2. Click **OK** to extend your lab duration.

   ![Manage Your Virtual Machine](./media/media/gext2.png)

3. If you have not extended the duration prior to when the lab is about to end, a pop-up will appear, giving you the option to extend. Click **OK** to proceed. -->

> **Note:** Please ensure the script continues to run and is not terminated after accessing the environment.

## Let's Get Started with Azure Portal

1. On your virtual machine, click on the Azure Portal icon.
2. You'll see the **Sign into Microsoft Azure** tab. Here, enter your credentials:

   - **Email/Username:** <inject key="AzureAdUserEmail"></inject>

     ![Enter Your Username](./media/gt-5.png)

3. Next, provide your password:

   - **Password:** <inject key="AzureAdUserPassword"></inject>

     ![Enter Your Password](./media/gt-4.png)

4. If **Action required** pop-up window appears, click on **Ask later**.
5. If prompted to **stay signed in**, you can click **No**.
6. If a **Welcome to Microsoft Azure** pop-up window appears, simply click **"Cancel"** to skip the tour.

## Steps to Proceed with MFA Setup if "Ask Later" Option is Not Visible

1. At the **"More information required"** prompt, select **Next**.

1. On the **"Keep your account secure"** page, select **Next** twice.

1. **Note:** If you don’t have the Microsoft Authenticator app installed on your mobile device:

   - Open **Google Play Store** (Android) or **App Store** (iOS).
   - Search for **Microsoft Authenticator** and tap **Install**.
   - Open the **Microsoft Authenticator** app, select **Add account**, then choose **Work or school account**.

1. A **QR code** will be displayed on your computer screen.

1. In the Authenticator app, select **Scan a QR code** and scan the code displayed on your screen.

1. After scanning, click **Next** to proceed.

1. On your phone, enter the number shown on your computer screen in the Authenticator app and select **Next**.
1. If prompted to stay signed in, you can click "No."

1. If a **Welcome to Microsoft Azure** pop-up window appears, simply click "Maybe Later" to skip the tour.

## Support Contact

The CloudLabs support team is available 24/7, 365 days a year, via email and live chat to ensure seamless assistance at any time. We offer dedicated support channels tailored specifically for both learners and instructors, ensuring that all your needs are promptly and efficiently addressed.

Learner Support Contacts:

- Email Support: [cloudlabs-support@spektrasystems.com](mailto:cloudlabs-support@spektrasystems.com)
- Live Chat Support: https://cloudlabs.ai/labs-support

Click **Next** from the bottom right corner to embark on your Lab journey!

![Start Your Azure Journey](./media/agg6.png)

Now you're all set to explore the powerful world of technology. Feel free to reach out if you have any questions along the way. Enjoy your workshop!
