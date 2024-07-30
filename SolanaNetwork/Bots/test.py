from telethon import TelegramClient
import asyncio

# Replace these with your own values
api_id = '24890651'
api_hash = '7662a65de55b21a4349bf0ceb078bd67'
phone = '+61402329029'  # Your phone number with country code

async def search_in_group():
    # Create the client and connect
    client = TelegramClient('search_txt_in_group_chat', api_id, api_hash)
    await client.start(phone)
    
    # Replace 'group_name_or_id' with the actual group name or ID
    group = await client.get_input_entity(-1002229815206) # -1002229815206

    # Replace 'search_text' with the text you're searching for
    search_text = 'A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump'

    # Iterate through messages in the group
    async for message in client.iter_messages(group):
        if search_text in message.text:
            print("------------------------------")
            print(f"Found message: {message.text}")

    await client.disconnect()

# Run the function
asyncio.run(search_in_group())
