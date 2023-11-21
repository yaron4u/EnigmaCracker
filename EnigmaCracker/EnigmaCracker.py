# EnigmaCracker
import subprocess
import sys
import os
import platform
import requests
import logging
import time
from dotenv import load_dotenv
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip39WordsNum,
)

# Constants
LOG_FILE_NAME = "enigmacracker.log"
ENV_FILE_NAME = "EnigmaCracker.env"
WALLETS_FILE_NAME = "wallets_with_balance.txt"

# Global counter for the number of wallets scanned
wallets_scanned = 0

# Get the absolute path of the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))
# Initialize directory paths
log_file_path = os.path.join(directory, LOG_FILE_NAME)
env_file_path = os.path.join(directory, ENV_FILE_NAME)
wallets_file_path = os.path.join(directory, WALLETS_FILE_NAME)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),  # Log to a file
        logging.StreamHandler(sys.stdout),  # Log to standard output
    ],
)

# Load environment variables from .env file
load_dotenv(env_file_path)

# Environment variable validation
required_env_vars = ["ETHERSCAN_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

# Check if we've set the environment variable indicating we're in the correct CMD
if os.environ.get("RUNNING_IN_NEW_CMD") != "TRUE":
    # Set the environment variable for the new CMD session
    os.environ["RUNNING_IN_NEW_CMD"] = "TRUE"

    # Determine the operating system
    os_type = platform.system()

    # For Windows
    if os_type == "Windows":
        subprocess.run(f'start cmd.exe /K python "{__file__}"', shell=True)

    # For Linux
    elif os_type == "Linux":
        subprocess.run(f"gnome-terminal -- python3 {__file__}", shell=True)

    # Exit this run, as we've opened a new CMD
    sys.exit()


def update_cmd_title():
    # Update the CMD title with the current number of wallets scanned
    if platform.system() == "Windows":
        os.system(f"title EnigmaCracker.py - Wallets Scanned: {wallets_scanned}")


def bip():
    # Generate a 12-word BIP39 mnemonic
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)


def bip44_ETH_wallet_from_seed(seed):
    # Generate an Ethereum wallet from a BIP39 seed.

    # Generate the seed from the mnemonic
    seed_bytes = Bip39SeedGenerator(seed).Generate()

    # Create a Bip44 object for Ethereum derivation
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)

    # Derive the account 0, change 0, address_index 0 path (m/44'/60'/0'/0/0)
    bip44_acc_ctx = (
        bip44_mst_ctx.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )

    # Get the Ethereum address
    eth_address = bip44_acc_ctx.PublicKey().ToAddress()

    return eth_address


def bip44_BTC_seed_to_address(seed):
    # Generate the seed from the mnemonic
    seed_bytes = Bip39SeedGenerator(seed).Generate()

    # Generate the Bip44 object
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

    # Generate the Bip44 address (account 0, change 0, address 0)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)

    # Print the address
    return bip44_addr_ctx.PublicKey().ToAddress()


def check_ETH_balance(address, etherscan_api_key, retries=3, delay=5):
    # Etherscan API endpoint to check the balance of an address
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={etherscan_api_key}"

    for attempt in range(retries):
        try:
            # Make a request to the Etherscan API
            response = requests.get(api_url)
            data = response.json()

            # Check if the request was successful
            if data["status"] == "1":
                # Convert Wei to Ether (1 Ether = 10^18 Wei)
                balance = int(data["result"]) / 1e18
                return balance
            else:
                logging.error("Error getting balance: %s", data["message"])
                return 0
        except Exception as e:
            if attempt < retries - 1:
                logging.error(
                    f"Error checking balance, retrying in {delay} seconds: {str(e)}"
                )
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
                return 0


def check_BTC_balance(address, retries=3, delay=5):
    # Check the balance of the address
    for attempt in range(retries):
        try:
            response = requests.get(f"https://blockchain.info/balance?active={address}")
            data = response.json()
            balance = data[address]["final_balance"]
            return balance / 100000000  # Convert satoshi to bitcoin
        except Exception as e:
            if attempt < retries - 1:
                logging.error(
                    f"Error checking balance, retrying in {delay} seconds: {str(e)}"
                )
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
                return 0


def write_to_file(seed, BTC_address, BTC_balance, ETH_address, ETH_balance):
    # Write the seed, address, and balance to a file in the script's directory
    with open(wallets_file_path, "a") as f:
        log_message = f"Seed: {seed}\nAddress: {BTC_address}\nBalance: {BTC_balance} BTC\n\nEthereum Address: {ETH_address}\nBalance: {ETH_balance} ETH\n\n"
        f.write(log_message)
        logging.info(f"Written to file: {log_message}")


def main():
    global wallets_scanned
    try:
        while True:
            seed = bip()
            # BTC
            BTC_address = bip44_BTC_seed_to_address(seed)
            BTC_balance = check_BTC_balance(BTC_address)

            logging.info(f"Seed: {seed}")
            logging.info(f"BTC address: {BTC_address}")
            logging.info(f"BTC balance: {BTC_balance} BTC")
            logging.info("")

            # ETH
            ETH_address = bip44_ETH_wallet_from_seed(seed)
            ###!
            etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
            if not etherscan_api_key:
                raise ValueError(
                    "The Etherscan API key must be set in the environment variables."
                )
            ###!
            ETH_balance = check_ETH_balance(ETH_address, etherscan_api_key)
            logging.info(f"ETH address: {ETH_address}")
            logging.info(f"ETH balance: {ETH_balance} ETH")

            # Increment the counter and update the CMD title
            wallets_scanned += 1
            update_cmd_title()

            # Check if the address has a balance
            if BTC_balance > 0 or ETH_balance > 0:
                logging.info("(!) Wallet with balance found!")
                write_to_file(seed, BTC_address, BTC_balance, ETH_address, ETH_balance)

    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")


if __name__ == "__main__":
    main()
