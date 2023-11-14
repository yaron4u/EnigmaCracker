# EnigmaCracker
EnigmaCracker is a tool for brute forcing Crypto Wallets

![EnigmaCrackerV2](https://github.com/yaron4u/EnigmaCracker/assets/67191566/de72ea8a-2ec4-4b32-9580-bd80c9715f87)

## **Disclaimer**

This script is developed for educational and research purposes only.

**By using this code, you agree to the following:**

1. You will not use this code, in whole or in part, for malicious intent, including but not limited to unauthorized mining on third-party systems.
2. You will seek explicit permission from any and all system owners before running or deploying this code.
3. You understand the implications of running mining software on hardware, including the potential for increased wear and power consumption.
4. The creator of this script cannot and will not be held responsible for any damages, repercussions, or any negative outcomes that result from using this script.

If you do not agree to these terms, please do not use or distribute this code.

## **How it works?**

We'll begin by delving into the foundational concepts. Upon establishing a wallet through platforms like **Exodus/TrustWallet** or similar services, users receive a **mnemonic phrase (_seed-phrase_)** comprised of **12 unique words**. The selection of words for this passphrase isn't arbitrary; they are derived from a specific lexicon containing **2048 potential words**. From this collection, the passphrase words are selected at random (**_the entire list of these words is accessible_** [**_HERE_**](https://www.blockplate.com/pages/bip-39-wordlist)). Utilizing this passphrase, an individual has the capability to access their wallet on any device and manage their assets. My application operates by employing brute force techniques to decipher these passphrases.

If EnigmaCracker finds a wallet with a balance, it will create `wallets_with_balance.txt` file that will contain the info of the discovered wallet.

Upon execution, EnigmaCracker generates a comprehensive log file named `enigmacracker.log`, which neatly records the entire session history for review and analysis.

# Technical Details

## Master Seed and Wallet Generation

![derivation](https://github.com/yaron4u/EnigmaCracker/assets/67191566/bbdcaab5-030f-4e03-b1cb-c816253d27df)

EnigmaCracker is engineered around the key principle of the **Master Seed** in cryptocurrency wallet generation, as per the standards described in BIP 32 for Hierarchical Deterministic (HD) Wallets. The Python script provided within this repository is designed to create a mnemonic phrase (also known as a seed phrase), which essentially acts as the **Master Seed** from which all cryptographic keys can be derived.

For a more in-depth understanding of this topic, feel free to explore the detailed documentation available here: [BIP 32 wiki](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki).

### The Role of Master Seed in EnigmaCracker

The script leverages the `bip_utils` library to generate a 12-word BIP39 mnemonic. This mnemonic is a human-readable representation of the wallet's **Master Seed**. This seed is then used to generate seeds for various cryptocurrency wallets, specifically for Bitcoin (BTC) and Ethereum (ETH), by following the BIP44 protocol that defines a logical hierarchy for deterministic wallets.

### Code Workflow:

1. **Seed Generation**: The `bip()` function in the script calls upon the BIP39 protocol to generate a new 12-word mnemonic. This is the first and most crucial step in the HD wallet creation process.
    
2. **Seed to Wallet Transformation**: The functions `bip44_ETH_wallet_from_seed` and `bip44_BTC_seed_to_address` take the generated mnemonic and produce the corresponding wallet addresses for Ethereum and Bitcoin, respectively. These addresses are derived from the master seed and follow a deterministic path outlined by BIP44, ensuring that each mnemonic generates a unique and recoverable set of addresses.
    
3. **Balance Checking**: With the generated addresses, the script uses online blockchain explorers through their APIs (Etherscan for Ethereum and Blockchain.info for Bitcoin) to check if the generated wallets contain any balance.
    
4. **Logging Results**: If a balance is found, the script writes the mnemonic, the derived addresses, and the wallet balances to a file (`wallets_with_balance.txt`), preserving the potentially valuable information for further examination.
    

Through the integration of BIP39 and BIP44 protocols, EnigmaCracker serves as a practical example of how the **Master Seed** forms the bedrock of cryptocurrency wallets, allowing for a secure, hierarchical structure of key derivation and management.

## Installation

Clone the repository using:

```
git clone https://github.com/yaron4u/EnigmaCracker
```
Remember to install the required libraries using:
```
pip install -r requirements.txt
```
## Configuration

1. Obtain an Etherscan API key following the instructions [here](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics).
2. Navigate to the script's directory and insert your API key in EnigmaCracker.env:
```
# In EnigmaCracker.env
etherscan_api_key = your_api_key_here <--- Replace with your actual API key
```
## Execution

Run EnigmaCracker from the command line:

```
cd path/to/EnigmaCracker
python EnigmaCracker.py
```

## Updates

- EnigmaCracker now supports detection of both BTC and ETH wallets.

## How to open the discovered wallet?

For assistance with accessing a discovered wallet, reach out to [vanitious@gmail.com](mailto:vanitious@gmail.com), I will personally help you!

### Contributions

If you want to thank me for the prize you found, I will appreciate it!

BTC: bc1qqa207jge9e48syfeevduumq0p6ct79cglu3gn6

ETH: 0xD8E91636cc6F55221545BFB7e1E417f0D2242d17

`Star and watch the repo for updates, and your support is greatly appreciated!`
