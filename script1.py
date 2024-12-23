import asyncio
import nest_asyncio
import httpx  # Use httpx instead of requests for async HTTP requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# Apply nest_asyncio to allow async in Jupyter environments or environments requiring it
nest_asyncio.apply()

# Your ChatGPT API endpoint and key
CHATGPT_API_URL = "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQm5IZkJDMlNyYUVUTjIyZVN3UWFNX3BFTU85SWpCM2NUMUk3T2dxejhLSzBhNWNMMXNzZlp3c09BSTR6YW1Sc1BmdGNTVk1GY0liT1RoWDZZX1lNZlZ0Z1dqd3c9PQ=="

# Function to send a request to ChatGPT API using httpx (async)
async def fetch_chatgpt_response(user_message: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            # Send request to the API asynchronously
            response = await client.post(
                CHATGPT_API_URL,
                json={"prompt": user_message},
                headers={"Content-Type": "application/json"}
            )

        if response.status_code != 200:
            return "Error: Something went wrong with the API."

        response_data = response.json()
        if response_data.get("status") == "success":
            return response_data.get("text", "No response text found.")
        else:
            return "Error: Could not fetch a valid response."

    except Exception as e:
        return f"Error: {str(e)}"

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am a bot powered by ChatGPT. How can I help you today?')

# Function to handle messages from the user
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    
    # Show typing indication immediately after user input
    typing_message = await update.message.reply_text("Typing...", reply_to_message_id=update.message.message_id)

    # Fetch the response from ChatGPT API asynchronously
    bot_response = await fetch_chatgpt_response(user_message)

    # Edit the "typing..." message with the actual response
    await typing_message.edit_text(bot_response)
