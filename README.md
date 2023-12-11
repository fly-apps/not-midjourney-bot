

<div align="center">
  <h1>(Not) Midjourney Bot on Fly GPUs</h1>
</div>

<div align="center">
  <img width="639" alt="cover" src="https://github.com/fly-apps/not-midjourney-bot/assets/3727384/4afa530a-06e6-45d3-ae22-5a910435c98c">
</div>

________

This template repository accompanies the "Deploy your own (Not) Midjourney Bot on Fly GPUs" blog post. This README will guide you through setting up the bot and server on Fly.io.

## Deploy the [Fooocus](https://github.com/lllyasviel/Fooocus) API Server App
> [!IMPORTANT]  
> You'll need Fly GPU access to perform this action.

Before you begin, ensure you have access to [Fly GPUs](https://fly.io/docs/gpus/). If you do not, join the waitlist [here](https://fly.io/gpu).

To deploy the Fooocus API server, follow these steps:

1. From the base directory, use the Fly CLI to deploy the server:

   ```
   fly deploy -c ./server/fly.toml
   ```

## Create Discord Application and Setup Bot Permissions
To invite your bot to your server and grant it the necessary permissions, you'll need to generate an OAuth2 URL using the [Discord Developer Portal](https://discord.com/developers/applications).

<details>
<summary>Follow these steps to create the URL and define the bot's capabilities:</summary>
<br>
  
1. In the Discord Developer Portal, select your application if you have one, or create one if you don't.
2. Create a new ["bot user"](https://discord.com/developers/docs/topics/oauth2#bots).
3. Navigate to the "OAuth2" page in the sidebar.
4. Under the "OAuth2 URL Generator" section, you'll find the scopes and permissions settings.
5. In the "SCOPES" section, select the checkboxes for:

    - `bot` – This allows your application to use bot-related features.
    - `applications.commands` – This permits your bot to create and handle application commands (slash commands).

6. Once you've selected the scopes, the "BOT PERMISSIONS" section will become active.
7. In the "BOT PERMISSIONS" section, you'll need to specify what actions your bot can perform on the server. Under "TEXT PERMISSIONS", select the following permissions:

    - `Send Messages` – Allows your bot to send messages in the chat.
    - `Create Public Threads` – Enables your bot to create new public threads.
    - `Send Messages in Threads` – Permits your bot to send messages in threads that it has access to.
    - `Attach Files` – Your bot can attach files to the messages it sends.
    - `Add Reactions` – Allows your bot to add reactions to messages.
    - `Use Slash Commands` – Enables your bot to interact with users through slash commands.

Your permissions should now look like this in the Developer Portal:

<img width="925" alt="Screenshot 2023-12-11 at 16 20 48" src="https://github.com/fly-apps/not-midjourney-bot/assets/3727384/3d551bbe-e1f3-458c-a43f-b19058942ee0">

8. After selecting the permissions, the page will automatically generate an OAuth2 URL at the bottom of the section.
9. Copy this URL, and use it to invite your bot to your server. Simply paste the URL into your web browser, choose a server to invite your bot to, and confirm the permissions.

It's important to only grant the permissions that your bot needs to function as intended. Excessive permissions can pose a security risk.

By following these steps, your bot will be set up with the appropriate permissions to interact with users on your server.
</details>

## Deploy the Discord Bot App

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

## The `/imagine` slash command

The bot exposes an `/imagine` slash command in your Discord server.

> [!NOTE]  
> The `/imagine` command is asynchronous, so it may take some time for the bot to generate and send the image.

 To use it:

1. Open Discord and navigate to the server where your bot is invited.
2. Type `/imagine` in the chat input box to trigger the slash command.
3. Write your text-to-image prompt for the image you want to generate. The more creative you are the better results you will get! 
4. Optionally, you can specify the styles to use in the image generation. You can provide up to three styles by using the style1, style2, and style3 options.
5. You can also choose to run the image generation at quality instead of speed by setting the quality option to `True`.
6. If you want to specify the aspect ratio for the image, you can use the ar option. The default is 1152×896px.
7. If you want to provide a *negative* prompt for the image, you can use the negative option.
8. Once you have provided all the necessary options, press Enter to execute the command.
9. The bot will generate the image based on the provided prompt and options. The generated image will be sent as an image response in the chat.
