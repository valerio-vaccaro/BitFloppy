#include "crypto.h"

String mnemonic = "";
String passphrase = "";
int32_t restart_counter = 0;
uint8_t status = STATUS_UNKNOWN;
bool testnet = true;

String generateMnemonic(void) {
    uint8_t entropy[16];
    esp_fill_random(entropy, sizeof(entropy));
    return mnemonicFromEntropy(entropy, sizeof(entropy));
}

void printStatus(uint8_t status) {
  switch (status) {
    case STATUS_UNKNOWN:
      log("Status: 0 UNKNOWN\n");
      break;
    case STATUS_EMPTY:
      log("Status: 1 EMPTY, a new mnemonic will be created soon.\n");
      break;
    case STATUS_LOCKED:
      log("Status: 2 LOCKED, addressed will be generated.\n");
      break;
    case STATUS_UNLOCKED:
      log("Status: 3 UNLOCKED, check MNEMONIC file!!!\n");
      break;
    case STATUS_CUSTOM_EMPTY:
      log("Status: 4 CUSTOM EMPTY, a new mnemonic will be imported soon.\n");
      break;
    case STATUS_CUSTOM_LOCKED:
      log("Status: 5 CUSTOM LOCKED, addressed will be generated.\n");
      break;
    case STATUS_CUSTOM_UNLOCKED:
      log("Status: 6 CUSTOM UNLOCKED, check MNEMONIC file!!!\n");
      break;
    case STATUS_FORMAT:
      log("Status: 7 FORMAT, format request.\n");
      break;
    default :
      log("Status: ???\n");
  }
}

void processStatus(void) {
  log("Get status...\n");
  if (nvsOpen()) {
    nvsGetStatus();
    nvsClose();
  }

  checkFormat();
  checkUnlock();
  
  switch (status) {
    case STATUS_UNKNOWN:
      printStatus(status);
      status = STATUS_EMPTY;
      if (nvsOpen()) {
        nvsPutStatus(status);
        nvsCommit();
        nvsClose();
      }
    case STATUS_EMPTY:
      printStatus(status);
      writeHelp();
      mnemonic = generateMnemonic();
      passphrase = "";
      testnet = true;
      status = STATUS_LOCKED;
      if (nvsOpen()) {
        nvsPutMnemonic(mnemonic);
        nvsPutPassphrase(passphrase);
        nvsPutNetwork(testnet);
        nvsPutStatus(status);
        nvsCommit();
        nvsClose();
      }
      ESP.restart();
    case STATUS_LOCKED:
      printStatus(status);
      writeHelp();
      if (nvsOpen()) {
        nvsGetMnemonic();
        nvsGetPassphrase();
        nvsGetNetwork();
        nvsClose();

        deriveBIP(44, false);
        deriveBIP(49, false);
        deriveBIP(84, false);
      }
      break;
    case STATUS_UNLOCKED:
      printStatus(status);
      writeHelp();
      if (nvsOpen()) {
        nvsGetMnemonic();
        nvsGetPassphrase();
        nvsGetNetwork();
        nvsClose();

        deriveBIP(44, true);
        deriveBIP(49, true);
        deriveBIP(84, true);

        writePreferences(mnemonic, passphrase, testnet);
      }
      break;
    case STATUS_CUSTOM_EMPTY:
      printStatus(status);
      writeHelp();
      mnemonic = readMnemonic();
      passphrase = readPassphrase();
      testnet = readNetwork();
      status = STATUS_CUSTOM_LOCKED;
      if (nvsOpen()) {
        nvsPutMnemonic(mnemonic);
        nvsPutPassphrase(passphrase);
        nvsPutNetwork(testnet);
        nvsPutStatus(status);
        nvsCommit();
        nvsClose();
      }
      ESP.restart();
    case STATUS_CUSTOM_LOCKED:
      printStatus(status);
      writeHelp();
      if (nvsOpen()) {
        nvsGetMnemonic();
        nvsGetPassphrase();
        nvsGetNetwork();
        nvsClose();

        deriveBIP(44, false);
        deriveBIP(49, false);
        deriveBIP(84, false);
      }
      break;
    case STATUS_CUSTOM_UNLOCKED:
      printStatus(status);
      writeHelp();
      if (nvsOpen()) {
        nvsGetMnemonic();
        nvsGetPassphrase();
        nvsGetNetwork();
        nvsClose();

        deriveBIP(44, true);
        deriveBIP(49, true);
        deriveBIP(84, true);

        writePreferences(mnemonic, passphrase, testnet);
      }
      break;
    case STATUS_FORMAT:
      printStatus(status);
      bool custom;
      custom = checkCustom();
      status = custom ? STATUS_CUSTOM_EMPTY : STATUS_EMPTY;
      if (nvsOpen()) {
        nvsErase();
        nvsPutStatus(status);
        nvsCommit();
        nvsClose();
      }
      deleteAllFiles(custom);
      ESP.restart();
      break;
    default :
      log("Status: ???\n");
  }
}
