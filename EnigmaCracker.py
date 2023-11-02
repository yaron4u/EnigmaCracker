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


def bip():
    # Generate a 12-word BIP39 mnemonic
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)


def seed_to_address(seed):
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


def check_balance(address):
    # Check the balance of the address
    try:
        response = requests.get(f"https://blockchain.info/balance?active={address}")
        data = response.json()
        balance = data[address]["final_balance"]
        return balance / 100000000  # Convert satoshi to bitcoin
    except Exception as e:
        print("Error checking balance:", str(e))
        return 0


def write_to_file(seed, address, balance):
    # Get the absolute path of the directory where the script is located
    directory = os.path.dirname(os.path.abspath(__file__))
    # Create the absolute path for the file
    file_path = os.path.join(directory, "wallets_with_balance.txt")

    # Write the seed, address, and balance to a file in the script's directory
    with open(file_path, "a") as f:
        f.write(f"Seed: {seed}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Balance: {balance} BTC\n\n")


def main():
    try:
        while True:
            seed = bip()
            address = seed_to_address(seed)
            balance = check_balance(address)

            print("Seed:")
            print("\___", seed)
            print("Address:")
            print("\___", address)
            print("Balance:")
            print("\___", balance, "BTC")
            print("\n")

            if balance > 0:
                print("(!) Wallet with balance found!")
                write_to_file(seed, address, balance)

    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")


if __name__ == "__main__":
    main()
