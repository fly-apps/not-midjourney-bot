<img width="639" alt="cover" src="https://github.com/fly-apps/not-midjourney-bot/assets/3727384/4afa530a-06e6-45d3-ae22-5a910435c98c">

________

This template repository accompanies the "Deploy your own (Not) Midjourney Bot on Fly GPUs" blog post. This README will guide you through setting up the bot and server on Fly.io.

## Part 1 - Deploy the Foocus API Server

Before you begin, ensure you have access to [Fly GPUs](https://fly.io/docs/gpus/). If you do not, join the waitlist [here](https://fly.io/gpu).

To deploy the Foocus API server, follow these steps:

1. From the base directory, use the Fly CLI to deploy the server:

   ```
   fly deploy -c ./server/fly.toml
   ```

## Part 2 - Deploy the Discord Bot

To deploy your Discord bot, you'll need to perform the following steps:

1. Create a new Discord application in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Within your application, create a bot and configure its permissions.
3. Generate an authorization URL for your bot.
4. Use the authorization URL to add your bot to your Discord server.
5. Set the `DISCORD_TOKEN` secret using the Fly CLI:

   ```
   fly secrets set DISCORD_TOKEN=your_discord_bot_token --stage
   ```

   Replace `your_discord_bot_token` with the actual token of your Discord bot.

6. Set the `URL` secret. This will be the URL where your bot can communicate with the deployed Foocus API server:

   ```
   fly secrets set URL="http://$(fly config show -c ./server/fly.toml | jq -r '.app').flycast" --stage
   ```

7. Deploy your bot to Fly.io using the Fly CLI:

   ```
   fly deploy -c ./bot/fly.toml
   ```