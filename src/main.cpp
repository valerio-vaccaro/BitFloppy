// based on https://raw.githubusercontent.com/Munsutari/esp32-s3-internal-flash-msc/main/flash_test.ino

#include <Bitcoin.h>
#include <DNSServer.h>
#include <FFat.h>
#include <FS.h>
#include <Preferences.h>
#include <Update.h>
#include <USB.h>
#include <USBMSC.h>
#include <WebServer.h>
#include <WiFi.h>

#include "crypto.h"
#include "eeprom.h"
#include "memory.h"

#define BLOCK_SIZE 4096

extern USBCDC USBSerial;
extern USBMSC msc;
extern const esp_partition_t* Partition;

extern int32_t restart_counter;

void setup() {
  Serial.begin(115200);
  Serial.println("StartingSerial"); 
  WiFi.mode(WIFI_STA);

  Serial.println("StartingNVS");
  nvsInit();

  if (nvsOpen()) {
    nvsGetCounter();
    nvsPutCounter(restart_counter++);
    nvsCommit();
    nvsClose();
  }

  Serial.println("Initializing FFat");

  internalMount();
  processStatus();

  nvsDeinit();
  internalUnmount();

  delay(100);

  externalMount();
}

void loop(){
  delay(5000);
}
