import subprocess
import sys
import os
import requests
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip39WordsNum,
)

# Check if we've set the environment variable indicating we're in the correct CMD
if os.environ.get("RUNNING_IN_NEW_CMD") != "TRUE":
    # Set the environment variable for the new CMD session
    os.environ["RUNNING_IN_NEW_CMD"] = "TRUE"

    # Open a new command prompt and run this script
    subprocess.run(f'start cmd.exe /K python "{__file__}"', shell=True)

    # Exit this run, as we've opened a new CMD
    sys.exit()


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


def check_ETH_balance(address, etherscan_api_key):
    # Etherscan API endpoint to check the balance of an address
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={etherscan_api_key}"

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
            print("Error getting balance:", data["message"])
            return 0
    except Exception as e:
        print("Error checking balance:", str(e))
        return 0


def check_BTC_balance(address):
    # Check the balance of the address
    try:
        response = requests.get(f"https://blockchain.info/balance?active={address}")
        data = response.json()
        balance = data[address]["final_balance"]
        return balance / 100000000  # Convert satoshi to bitcoin
    except Exception as e:
        print("Error checking balance:", str(e))
        return 0


def write_to_file(seed, BTC_address, BTC_balance, ETH_address, ETH_balance):
    # Get the absolute path of the directory where the script is located
    directory = os.path.dirname(os.path.abspath(__file__))
    # Create the absolute path for the file
    file_path = os.path.join(directory, "wallets_with_balance.txt")

    # Write the seed, address, and balance to a file in the script's directory
    with open(file_path, "a") as f:
        f.write(f"Seed: {seed}\n")
        f.write(f"Address: {BTC_address}\n")
        f.write(f"Balance: {BTC_balance} BTC\n\n")
        f.write(f"Ethereum Address: {ETH_address}\n")
        f.write(f"Balance: {ETH_balance} ETH\n\n")


def main():
    try:
        while True:
            seed = bip()
            # BTC
            BTC_address = bip44_BTC_seed_to_address(seed)
            BTC_balance = check_BTC_balance(BTC_address)

            print("Seed:")
            print("\___", seed)
            print("BTC address:")
            print("\___", BTC_address)
            print("BTC balance:")
            print("\___", BTC_balance, "BTC")
            print("\n")

            # ETH
            ETH_address = bip44_ETH_wallet_from_seed(seed)
            ###!
            etherscan_api_key = "YOUR_API_KEY"  # API key for Etherscan
            ###!
            ETH_balance = check_ETH_balance(ETH_address, etherscan_api_key)
            print("ETH address:")
            print("\___", ETH_address)
            print("ETH balance:")
            print("\___", ETH_balance, "ETH")

            # Check if the address has a balance
            if BTC_balance > 0 or ETH_balance > 0:
                print("(!) Wallet with balance found!")
                write_to_file(seed, BTC_address, BTC_balance, ETH_address, ETH_balance)

    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")


if __name__ == "__main__":
    main()
