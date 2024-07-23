#pragma once

#include <Arduino.h>
#include <Bitcoin.h>

#include <mbedtls/md.h>
#include <Preferences.h>
#include <secp256k1.h>
#include <wally_core.h>
#include <wally_bip32.h>
#include <wally_bip39.h>
#include <wally_address.h>
#include <wally_crypto.h>

#include "eeprom.h"
#include "memory.h"

#define STATUS_UNKNOWN          0
#define STATUS_EMPTY            1
#define STATUS_LOCKED           2
#define STATUS_UNLOCKED         3
#define STATUS_CUSTOM_EMPTY     4
#define STATUS_CUSTOM_LOCKED    5
#define STATUS_CUSTOM_UNLOCKED  6
#define STATUS_FORMAT           7

void initLeds(void);
String generateMnemonic(void);
void processStatus(void);