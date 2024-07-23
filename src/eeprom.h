#pragma once

#include <Arduino.h>
#include <nvs_flash.h>
#include <nvs.h>

void nvsDeinit(void);
void nvsErase(void);
void nvsInit(void);
void nvsGet(void);
void nvsPut(void);

bool nvsOpen(void);
void nvsClose(void);
bool nvsCommit(void);

bool nvsGetCounter();
bool nvsPutCounter(int32_t value);

bool nvsGetMnemonic();
bool nvsPutMnemonic(String mnemonic);

bool nvsGetPassphrase();
bool nvsPutPassphrase(String passphrase);

bool nvsGetStatus();
bool nvsPutStatus(uint8_t status);

bool nvsGetNetwork();
bool nvsPutNetwork(bool testnet);