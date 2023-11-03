# EnigmaCracker
EnigmaCracker is a tool for brute forcing crypto wallets

![2023-11-01 22-02-03](https://github.com/yaron4u/EnigmaCracker/assets/67191566/a165bd3e-1c79-4dfc-8c50-6da174c7a197)

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

If EnigmaCracker finds a wallet with a balance, it will create `wallets_with_balance.txt` file that will contain the info of the found wallet.

## Installation

```
git clone https://github.com/yaron4u/EnigmaCracker
```
Don't forget to `pip install ~library~` from `requirements.txt`

## Requirements

Before running EnigmaCracker you must enter your etherscan API key in the code (The code will not run if you don't do it)
```
navigate to the code installed: cd path\to\directory
edit EnigmaCracker.py
search for etherscan_api_key
etherscan_api_key = "YOUR_API_KEY" <- put your API key here
```
To get the API key follow this guide: https://docs.etherscan.io/getting-started/viewing-api-usage-statistics
## How to run (Recommended in cmd)

```
navigate to the code installed: cd path\to\directory
python EnigmaCracker.py
```

## Major updates

EnigmaCracker can now find wallets with BTC and ETH

## How to open the founded wallet?

Please contact me at vanitious@gmail.com for help, I will personally help you!

### Donation

If you want to thank me for the prize you found, I will appreciate it!

Also star the repo, it will really help me and everyone!

BTC: bc1qqa207jge9e48syfeevduumq0p6ct79cglu3gn6

ETH: 0xD8E91636cc6F55221545BFB7e1E417f0D2242d17
