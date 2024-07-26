#include "memory.h"

USBCDC USBSerial;
USBMSC msc;
EspClass _flash;
const esp_partition_t* Partition;

extern String mnemonic;
extern String passphrase;
extern int32_t restart_counter;
extern uint8_t status;
extern bool testnet;

File logFile;

void log(String s) {
  Serial.println(s);
  logFile.print(s);
  logFile.flush();
}

void deriveBIP(int index, bool unlocked) {
  HDPrivateKey hd(mnemonic, passphrase);
  String directory = "/bip" + String(index);
  String path = "m/" + String(index) + "'/";
  if (testnet) {
    path = path + "1";
  } else {
    path = path + "0";
  }
  path = path + "'/0'";
  log("Deriving " + path + " addresses!\n");
  HDPrivateKey account = hd.derive(path);
  File mFile = FFat.open(directory + "/xpriv.txt", FILE_WRITE, true);
  String xpriv = unlocked ? account.xprv() : "**********";
  mFile.println(xpriv);
  mFile.close();
  mFile = FFat.open(directory + "/xpub.txt", FILE_WRITE, true);
  mFile.println(account.xpub());
  mFile.close();
  log("\t" + path + "\tXPUB " + account.xpub() + "\n");
  String inpath;
  mFile = FFat.open(directory + "/addresses.txt", FILE_WRITE, true);
  for (int i=0; i<10; i++) {
    inpath = "m/0/" + String(i);
    HDPrivateKey derived =  account.derive(inpath);
    String address = derived.address();
    String key = unlocked ? derived.wif() : "**********";
    mFile.println(path + inpath.substring(1) + "\t" + address + "\t" + key);
    log("\t" + path + inpath.substring(1) + "\t" + address + "\n");
  }
  mFile.close();
  mFile = FFat.open(directory + "/changes.txt", FILE_WRITE, true);
  for (int i=0; i<10; i++) {
    inpath = "m/1/" + String(i);
    HDPrivateKey derived =  account.derive(inpath);
    String address = derived.address();
    String key = unlocked ? derived.wif() : "**********";
    mFile.println(path + inpath.substring(1) + "\t" + address + "\t" + key);
    log("\t" + path + inpath.substring(1) + "\t" + address + "\n");
  }
  mFile.close();
}

void internalMount(void) {
  if(!FFat.begin()){
    Serial.println("Mount Failed, formatting...");
    // If mount fails, format the partition (Feels cleaner than FFat.begin(true))
    if(FFat.format(FFAT_WIPE_FULL)) {
      Serial.println("Format Success");
    } else {
      Serial.println("Format Failed");
      delay(5000);
      ESP.restart();
    }
  }else{
    Serial.println("fat success");
  }

  logFile = FFat.open("/log.txt", FILE_WRITE, true);
}

String readMnemonic(void) {
  File mFile = FFat.open("/mnemonic.txt", FILE_READ);
  String payload = "";
  if (mFile) {
  while (mFile.available()) {
      payload = payload + String(mFile.readString());
    }
    mFile.close();
    log("File mnemonic.txt exists!\n");
    return payload;
  }
  return "";
}

String readPassphrase(void) {
  File mFile = FFat.open("/passphrase.txt", FILE_READ);
  String payload = "";
  if (mFile) {
  while (mFile.available()) {
      payload = payload + String(mFile.readString());
    }
    mFile.close();
    log("File passphrase.txt exists!\n");
    return payload;
  }
  return "";
}

bool readNetwork(void) {
  File mFile = FFat.open("/network.txt", FILE_READ);
  if (mFile) {
    String network_str;
    while (mFile.available()) {
      network_str = network_str + mFile.readString();
    }
    mFile.close();
    log("File network.txt exists!\n");
    network_str.toLowerCase();
    if (network_str.indexOf("testnet") == -1) {
      return false;
    } else {
      return true;
    }
  }
  return true;
}

void writeHelp(void) {
  File mFile;
  mFile = FFat.open("/README.txt", FILE_WRITE, true);
  mFile.println("ESP32MEMORY");
  mFile.println("-----------");
  mFile.println("");
  mFile.println("Unlock");
  mFile.println("");
  mFile.println("If you want to shows mnemonic, passphrase, xpriv keys and address private keys you just need to:");
  mFile.println("- write a file with name UNLOCK.txt,");
  mFile.println("- unmount the volume,");
  mFile.println("- restart the board.");
  mFile.println("The board will generate new files (e.g. the file with menmonic) and shows keys close to addresses.");
  mFile.println("");
  mFile.println("-----------");
  mFile.println("");
  mFile.println("Format");
  mFile.println("");
  mFile.println("If you want change the mnemonic you have to:");
  mFile.println("- write a file with name FORMAT.txt,");
  mFile.println("- write a file with name MNEMONIC.txt if you want a custom mnemonic or remove it if you dont want,");
  mFile.println("- write a file with name PASSPHRASE.txt if you want a custom passphrase or remove it if you dont want,");
  mFile.println("- write a file with name NEWTWORK.txt if you want a custom network or remove it if you want use testnet,");
  mFile.println("- unmount the volume,");
  mFile.println("- restart the board.");
  mFile.println("The board will remove all previouse informations generate or load secrets.");
  mFile.close();
}

void writePreferences(String mnemonic, String passphrase, bool network) {
  File mFile;
  mFile = FFat.open("/mnemonic.txt", FILE_WRITE, true);
  mFile.print(mnemonic);
  mFile.close();
  mFile = FFat.open("/passphrase.txt", FILE_WRITE, true);
  mFile.print(passphrase);
  mFile.close();
  mFile = FFat.open("/network.txt", FILE_WRITE, true);
  mFile.print(testnet ? "testnet": "mainnet");
  mFile.close();
  mFile = FFat.open("/UNLOCKED.txt", FILE_WRITE, true);
  mFile.close();
}

void deleteAllFiles(bool custom) {
  if (!custom) {
    FFat.remove("/mnemonic.txt");
    FFat.remove("/passphrase.txt");
    FFat.remove("/network.txt");
  }
  FFat.remove("/LOCKED.txt");
  FFat.remove("/UNLOCKED.txt");
  FFat.remove("/CUSTOM.txt");
  FFat.rmdir("/bip44");
  FFat.rmdir("/bip49");
  FFat.rmdir("/bip84");
}

void checkFormat(void) {
  if (FFat.exists("/FORMAT.txt")) {
    // set status
    status = STATUS_FORMAT;
    if (nvsOpen()) {
      nvsPutStatus(status);
      nvsCommit();
      nvsClose();
    }
    // remove file
    FFat.remove("/FORMAT.txt");
  }
} 

void checkUnlock(void) {
  if (FFat.exists("/UNLOCK.txt")) {
    // set status
    if (status == STATUS_LOCKED) {
      status = STATUS_UNLOCKED;
    } else if (status == STATUS_CUSTOM_LOCKED) {
      status = STATUS_CUSTOM_UNLOCKED;
    } else {
      log("UNLOCK with wrong status!\n");
    }
    if (nvsOpen()) {
      nvsPutStatus(status);
      nvsCommit();
      nvsClose();
    }
    // remove file
    FFat.remove("/UNLOCK.txt");
  }
}

bool checkCustom(void) {
  if (FFat.exists("/mnemonic.txt")) {
    return true;
  }
  return false;
}

void internalUnmount(void){
  logFile.close();
  FFat.end();
}

const esp_partition_t* partition(void){
  // Return the first FAT partition found (should be the only one)
  return esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_DATA_FAT, NULL);
}

int32_t onWrite(uint32_t lba, uint32_t offset, uint8_t* buffer, uint32_t bufsize){
  _flash.partitionEraseRange(Partition, offset + (lba * BLOCK_SIZE), bufsize);
  _flash.partitionWrite(Partition, offset + (lba * BLOCK_SIZE), (uint32_t*)buffer, bufsize);
  return bufsize;
}

int32_t onRead(uint32_t lba, uint32_t offset, void* buffer, uint32_t bufsize){
  _flash.partitionRead(Partition, offset + (lba * BLOCK_SIZE), (uint32_t*)buffer, bufsize);
  return bufsize;
}

bool onStartStop(uint8_t power_condition, bool start, bool load_eject){
  return true;
}

void externalMount(void) {
  Serial.println("Getting partition info");
  Partition = partition();
  Serial.println("Initializing MSC");
  msc.vendorID("ESP32");
  msc.productID("USB_MSC");
  msc.productRevision("1.0");
  msc.onRead(onRead);
  msc.onWrite(onWrite);
  msc.onStartStop(onStartStop);
  msc.mediaPresent(true);
  msc.begin(Partition->size/BLOCK_SIZE, BLOCK_SIZE);

  Serial.println("Initializing USB");
  USB.begin();

  Serial.println("Printing flash size");
  char buf[50];
  snprintf(buf, 50, "Flash Size: %d", Partition->size);
  Serial.println(buf);
}

void externalUnmount(void) {
}