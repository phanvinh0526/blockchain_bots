import asyncio
import logging, time
import re, base58
import requests, json
from datetime import datetime, timedelta

# from aiogram import types, Dispatcher, Router, Bot
# from aiogram.filters import CommandStart, Command
# from aiogram.methods import SendMessage
# from aiogram.client.default import DefaultBotProperties

from solana.rpc.api import Client
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey
from solana.rpc.types import MemcmpOpts


# ###### DESCRIPTION ###### #
# This bot is to search any new pool created in Solana network
# Process:
#   1.  search for initialize transaction
#   2.  https://solana-mainnet.g.alchemy.com/v2/8lkJ9fP65TFrEXHYY_M6eoc_cxjGZ1IX
#-------------------------#

# CREDENTIALS
TELE_BOT_TOKEN     = "7406444343:AAFLwMumktwFhhfFSB3uzJXGNTQlLudDGJ8"
# BIRDEYE_API_TOKEN  = "6af62e0ddb424d288693b68e3c72805e"
ALCHEMY_API_TOKEN  = "8lkJ9fP65TFrEXHYY_M6eoc_cxjGZ1IX"
# QUICKNODE_TOKEN    = "0127af86093591fd3e6926f99a9c4e6a762dce8a"

# Constants
TAR_FORUM_ID = -1002229815206
TAR_TOPIC_ID = 5795
# RPC_ENDPOINT = "https://blissful-greatest-liquid.solana-devnet.quiknode.pro"
RPC_ENDPOINT = "https://solana-mainnet.g.alchemy.com/v2"

# Raydium program ID (example ID, please replace with actual Raydium program ID if different)
RAYDIUM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8" #  4Rr4XHjxj46Yt7fGhgyQTBqNsT3VcihB5UStSsxJxnCy

# b58 encoded: JdQ2wqbZTST6Pz5a3ibFwtynYm8XrXVntoMSHtbUTeZNKYMHGCuMgq2iJFgK


# Setup logging
logging.basicConfig(level=logging.INFO)

# Setup connection to RPC
client = Client(endpoint = f"{RPC_ENDPOINT}/{ALCHEMY_API_TOKEN}")
# if(client.is_connected() == False):
#    print("Cannot connect to RPC server!!!")
#    exit()

# headers = {
#     "x-chain": "solana",
#     "X-API-KEY": BIRDEYE_API_TOKEN
# }
# birdeye_endpoint = "https://public-api.birdeye.so/"

# Dispatcher
# dp = Dispatcher()
# bot = Bot(
#     token= TELE_BOT_TOKEN,
#     default=DefaultBotProperties(parse_mode='HTML')
# )

# ############## #
# Command handlers
# @dp.message(CommandStart())
# async def cmd_start(msg: types.Message) -> None:
#     await msg.answer(
#         text='This bot is about to search for new pool created in Raydium.'
#     )

# @dp.message(Command('send_msg_to_topic'))
# async def cmd_send_to_topic(msg: types.Message) -> None:
#     await bot.send_message(chat_id=TAR_FORUM_ID, message_thread_id=TAR_TOPIC_ID, text=msg.text)
#     await msg.reply("Msg sent to the a forum topic!")
    

# ############## #
# Message handlers
# ############## #
# Message handlers
# @dp.message()
# async def message_handler(msg: types.Message) -> None:


# ######## #
# Functions
def get_latest_block():
    response = client.get_epoch_info()
    return response.value.block_height

def get_block_transactions(block_height):
    response = client.get_block(slot=block_height, max_supported_transaction_version=0) # TODO: 256755020 block was skipped
    if(response.value is not None):
        return response.value.transactions
    return []

def is_new_pool_creation(tx):
    # check if the transaction contains instructions for Raydium program
    for instruction in tx.transaction.message.instructions:
        # print(base58.b58encode(instruction.data))
        if((instruction.program_id_index is not None) and (base58.b58encode(instruction.data) == RAYDIUM_PROGRAM_ID)):
            # add logic to identify pool creation instruction here
            print(instruction)
            return True
    return False

def track_new_pools():
    latest_block = get_latest_block()
    while True:
        print(f"***Block number: {latest_block}")
        transactions = get_block_transactions(latest_block)
        for tx in transactions:
            if is_new_pool_creation(tx):
                print("New pool creation detected.", tx)
        latest_block += 1


# async def forward_message_to_a_forum(msg: types.Message) -> None:
#     await bot.forward_message(chat_id=TAR_FORUM_ID, message_thread_id=TAR_TOPIC_ID, from_chat_id=msg.chat.id, message_id=msg.message_id)
#     await msg.reply("Message forwarded!")

# ######## #
# Main Funcs
# async def main() -> None:
#     """The main function which will execute our event loop and start polling"""
#     # Start polling
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())

if __name__ == "__main__":
    track_new_pools()

# ### Test Case ### #
