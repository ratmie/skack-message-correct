import asyncio
import config
import chatgpt
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler

# 環境変数からAPIトークンを取得
SLACK_APP_TOKEN = config.SLACK_APP_TOKEN
SLACK_BOT_TOKEN = config.SLACK_BOT_TOKEN
app = AsyncApp(token=SLACK_BOT_TOKEN)
client = AsyncWebClient(token=SLACK_BOT_TOKEN)

@app.shortcut("correct-message")
async def process_message_shortcut(ack, body, logger):
    await ack()
    logger.debug("Message shortcut invoked")
    # Extract message link from command text
    channel_id = body['channel']['id']
    message_ts = body['message']['ts']
    user_id = body['user']['id']

    if channel_id and message_ts:
        try:
            # Retrieve message content
            result = await client.conversations_history(channel=channel_id, latest=message_ts, inclusive=True, limit=1)
            message = result['messages'][0]['text']
# Unhandled request ({'type': 'message_action', 'callback_id': 'correct-message'})
            # Process the message with ChatGPT API (replace with your actual API call)
            chatgpt_response = await chatgpt.correct_message(message)

            # Send the response as an ephemeral message to the user who triggered the shortcut
            response = await client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"ChatGPT response: {chatgpt_response}")
        except SlackApiError as e:
            logger.error(f"Error: {e}")

async def main():
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())

