

<div align="center">
  <h1>(Not) Midjourney Bot on Fly GPUs</h1>
</div>

<div align="center">
  <img width="639" alt="cover" src="https://github.com/fly-apps/not-midjourney-bot/assets/3727384/4afa530a-06e6-45d3-ae22-5a910435c98c">
</div>

________

This template repository accompanies the "Deploy your own (Not) Midjourney Bot on Fly GPUs" blog post. This README will guide you through setting up the bot and server on Fly.io.

## Part 1 - Deploy the [Fooocus](https://github.com/lllyasviel/Fooocus) API Server

Before you begin, ensure you have access to [Fly GPUs](https://fly.io/docs/gpus/). If you do not, join the waitlist [here](https://fly.io/gpu).

To deploy the Fooocus API server, follow these steps:

1. From the base directory, use the Fly CLI to deploy the server:

   ```
   fly deploy -c ./server/fly.toml
   ```

## Part 2 - Discord Bot OAuth2 URL and Permissions Setup
To invite your bot to your server and grant it the necessary permissions, you'll need to generate an OAuth2 URL using the [Discord Developer Portal](https://discord.com/developers/applications).

<details>
<summary>Follow these steps to create the URL and define the bot's capabilities:</summary>
<br>

1. Go to the Discord Developer Portal and select your application.
2. Navigate to the "OAuth2" page in the sidebar.
3. Under the "OAuth2 URL Generator" section, you'll find the scopes and permissions settings.
4. In the "SCOPES" section, select the checkboxes for:

    - `bot` – This allows your application to use bot-related features.
    - `applications.commands` – This permits your bot to create and handle application commands (slash commands).

5. Once you've selected the scopes, the "BOT PERMISSIONS" section will become active.
6. In the "BOT PERMISSIONS" section, you'll need to specify what actions your bot can perform on the server. Under "TEXT PERMISSIONS", select the following permissions:

    - `Send Messages` – Allows your bot to send messages in the chat.
    - `Create Public Threads` – Enables your bot to create new public threads.
    - `Send Messages in Threads` – Permits your bot to send messages in threads that it has access to.
    - `Attach Files` – Your bot can attach files to the messages it sends.
    - `Add Reactions` – Allows your bot to add reactions to messages.
    - `Use Slash Commands` – Enables your bot to interact with users through slash commands.

7. After selecting the permissions, the page will automatically generate an OAuth2 URL at the bottom of the section.
8. Copy this URL, and use it to invite your bot to your server. Simply paste the URL into your web browser, choose a server to invite your bot to, and confirm the permissions.

It's important to only grant the permissions that your bot needs to function as intended. Excessive permissions can pose a security risk.

By following these steps, your bot will be set up with the appropriate permissions to interact with users on your server.
</details>

## Part 2 - Deploy the Discord Bot

> [!NOTE]  
> The Discord bot app will be deployed on non-GPU hardware.

To deploy your Discord bot, you'll need to perform the following steps:

1. Set the `DISCORD_TOKEN` secret using the Fly CLI:

   ```
   fly secrets set DISCORD_TOKEN=your_discord_bot_token --stage
   ```

   Replace `your_discord_bot_token` with the actual token of your Discord bot.

6. Set the `URL` secret. This will be the URL where your bot can communicate with the deployed Fooocus API server:

   ```
   fly secrets set URL="http://$(fly config show -c ./server/fly.toml | jq -r '.app').flycast" --stage
   ```

7. Deploy your bot to Fly.io using the Fly CLI:

   ```
   fly deploy -c ./bot/fly.toml
   ```