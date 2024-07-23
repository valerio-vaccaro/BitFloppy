# ESP32S3MEMORY

SEARCHING FOR A BETTER NAME!

This is just a proof of concept for a simple hardware for key derivations (and maybe PSBT decoding/signing in future).

## How it works?

Every time you restart the board the software will update status and perform needed actions, when these actions ends the board will show a 1,44 MB Mass Storage interface with various files.

## Status

A board can be in one of the following status: 
- UNKNOWN, board is new and never used, the firmware will set the status to EMPTY,
- EMPTY, board don't have secret material, secret material will be generated and status change to LOCKED,
- LOCKED, board derive all files and wait,
- UNLOCKED, board derive all files including secrets and wait,
- CUSTOM_EMPTY, board don't have secret material, secret material will be generated using provided files and status change to CUSTOM_LOCKED,
- CUSTOM_LOCKED, board derive all files and wait,
- CUSTOM_UNLOCKED,  board derive all files including secrets and wait,
- FORMAT, board will delete files and secret and move to EMPTY or CUSTOM_EMPTY.

## Generated files

The memory of the board contains the following files:
- mnemonic.txt, the menmonic used (this file is present only in unlocked status),
- network.txt, the network used,
- passphrase.txt, the passphrase used (this file is present only in unlocked status),
- log.txt, complete log of all action perfomed,
- README.txt, brief explanation similar to this file.

Plus 3 directories, bip44, bip49 and bip 84 with the following files:
- addresses.txt, list of derived addresses with derivation 0/*,
- changes.txt, list of derived adddresses with derivation 1/*,
- xpub.txt, extended public key,
- xpriv.txt extended private key (or some *** if locked).

## Actions

TBD

## Supported hardware

Supported boards:
- Lolin S2 mini

## Status

This project is just a Proof-of-Concept, use only with testnet or signet funds!