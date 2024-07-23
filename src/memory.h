#pragma once

#include <Bitcoin.h>
#include <FFat.h>
#include <FS.h>
#include <USB.h>
#include <USBMSC.h>

#include "crypto.h"

#define BLOCK_SIZE 4096

// internal primitives
bool checkCustom(void);
void checkFormat(void);
void checkUnlock(void);
void deleteAllFiles(bool custom);
void deriveBIP(int index, bool unlocked);
void internalMount(void);
void internalUnmount(void);
void log(String s);
int32_t onWrite(uint32_t lba, uint32_t offset, uint8_t* buffer, uint32_t bufsize);
int32_t onRead(uint32_t lba, uint32_t offset, void* buffer, uint32_t bufsize);
bool onStartStop(uint8_t power_condition, bool start, bool load_eject);
const esp_partition_t* partition(void);
String readMnemonic(void);
String readPassphrase(void);
bool readNetwork(void);
void writeHelp(void);
void writePreferences(String mnemonic, String passphrase, bool network);

// usb primitives
void externalMount(void);
void externalUnmount(void);
