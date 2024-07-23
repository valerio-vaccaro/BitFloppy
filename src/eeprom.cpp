#include "eeprom.h"

nvs_handle_t nvsHandler;

extern String mnemonic;
extern String passphrase;
extern int32_t restart_counter;
extern uint8_t status;
extern bool testnet;

void nvsInit(void) {
  esp_err_t err = nvs_flash_init();
  if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      // NVS partition was truncated and needs to be erased
      // Retry nvs_flash_init
      ESP_ERROR_CHECK(nvs_flash_erase());
      err = nvs_flash_init();
  }
  ESP_ERROR_CHECK(err);
}

bool nvsOpen(void) {
  Serial.println("Opening Non-Volatile Storage (NVS) handle... ");
  
  esp_err_t err = nvs_open("storage", NVS_READWRITE, &nvsHandler);

  if (err != ESP_OK) {
    Serial.print("Error (");
    Serial.print(esp_err_to_name(err));
    Serial.println(") opening NVS handle!");
    return false;
  } else {
    Serial.println("Done\n");
    return true;
  }
}

void nvsClose(void) {
  nvs_close(nvsHandler);
}

bool nvsCommit(void) {
  Serial.print("Committing updates in NVS ... ");
  esp_err_t err = nvs_commit(nvsHandler);
  Serial.print((err != ESP_OK) ? "Failed!\n" : "Done\n");
  ESP_ERROR_CHECK(err);
  return (err == ESP_OK);
}

bool nvsGetCounter(void) {
  Serial.print("Reading restart counter from NVS ... ");
  esp_err_t err = nvs_get_i32(nvsHandler, "restart_counter", &restart_counter);
  switch (err) {
      case ESP_OK:
          Serial.print("Done\n");
          Serial.print("Restart counter = %");
          char buf[20];
          snprintf(buf, 20, "%d", restart_counter);
          Serial.println(buf);
          return true;
          break;
      case ESP_ERR_NVS_NOT_FOUND:
          Serial.print("The value is not initialized yet!\n");
          break;
      default :
          Serial.print("Error (");
          Serial.print(esp_err_to_name(err));
          Serial.print("reading!\n");
  }
  return false;
}

bool nvsPutCounter(int32_t value) {
  Serial.print("Updating restart counter in NVS ... ");
  esp_err_t err = nvs_set_i32(nvsHandler, "restart_counter", value);
  Serial.print((err != ESP_OK) ? "Failed!\n" : "Done\n");
  ESP_ERROR_CHECK(err);
  return (err == ESP_OK);
}

bool nvsGetMnemonic(void) {
  Serial.print("Reading mnemonic from NVS ... ");
  char buf[256];
  size_t len;
  esp_err_t err = nvs_get_str(nvsHandler, "mnemonic", buf, &len);
  mnemonic = String(buf);
  switch (err) {
      case ESP_OK:
          Serial.print("Done\n");
          Serial.print("Mnemonic = %");
          Serial.println(mnemonic);
          return true;
          break;
      case ESP_ERR_NVS_NOT_FOUND:
          Serial.print("The value is not initialized yet!\n");
          break;
      default :
          Serial.print("Error (");
          Serial.print(esp_err_to_name(err));
          Serial.print("reading!\n");
  }
  return false;
}

bool nvsPutMnemonic(String value) {
  Serial.print("Updating mnemonic in NVS ... ");
  esp_err_t err = nvs_set_str(nvsHandler, "mnemonic", value.c_str());
  Serial.print((err != ESP_OK) ? "Failed!\n" : "Done\n");
  ESP_ERROR_CHECK(err);
  return (err == ESP_OK);
}

bool nvsGetPassphrase(void) {
  Serial.print("Reading passphrase from NVS ... ");
  char buf[256];
  size_t len;
  esp_err_t err = nvs_get_str(nvsHandler, "passphrase", buf, &len);
  passphrase = String(buf);
  switch (err) {
      case ESP_OK:
          Serial.print("Done\n");
          Serial.print("Passphrase = %");
          Serial.println(passphrase);
          return true;
          break;
      case ESP_ERR_NVS_NOT_FOUND:
          Serial.print("The value is not initialized yet!\n");
          break;
      default :
          Serial.print("Error (");
          Serial.print(esp_err_to_name(err));
          Serial.print("reading!\n");
  }
  return false;
}

bool nvsPutPassphrase(String value) {
  Serial.print("Updating passphrase in NVS ... ");
  esp_err_t err = nvs_set_str(nvsHandler, "passphrase", value.c_str());
  Serial.print((err != ESP_OK) ? "Failed!\n" : "Done\n");
  ESP_ERROR_CHECK(err);
  return (err == ESP_OK);
}

bool nvsGetNetwork(void) {
  Serial.print("Reading network from NVS ... ");
  esp_err_t err = nvs_get_i8(nvsHandler, "testnet", (int8_t *) &testnet);
  switch (err) {
      case ESP_OK:
          Serial.print("Done\n");
          Serial.print("Network = %");
          char buf[20];
          snprintf(buf, 20, "%d", testnet);
          Serial.println(buf);
          return true;
          break;
      case ESP_ERR_NVS_NOT_FOUND:
          Serial.print("The value is not initialized yet!\n");
          break;
      default :
          Serial.print("Error (");
          Serial.print(esp_err_to_name(err));
          Serial.print("reading!\n");
  }
  return false;
}

bool nvsPutNetwork(bool value) {
  Serial.print("Updating network in NVS ... ");
  esp_err_t err = nvs_set_i8(nvsHandler, "testnet", value);
  Serial.print((err != ESP_OK) ? "Failed!\n" : "Done\n");
  ESP_ERROR_CHECK(err);
  return (err == ESP_OK);
}

bool nvsGetStatus(void) {
  Serial.print("Reading status from NVS ... ");
  esp_err_t err = nvs_get_u8(nvsHandler, "status", &status);
  switch (err) {
      case ESP_OK:
          Serial.print("Done\n");
          Serial.print("Status = %");
          char buf[20];
          snprintf(buf, 20, "%d", status);
          Serial.println(buf);
          return true;
          break;
      case ESP_ERR_NVS_NOT_FOUND:
          Serial.print("The value is not initialized yet!\n");
          break;
      default :
          Serial.print("Error (");
          Serial.print(esp_err_to_name(err));
          Serial.print("reading!\n");
  }
  return false;
}

bool nvsPutStatus(uint8_t value) {
  Serial.print("Updating status in NVS ... ");
  esp_err_t err = nvs_set_u8(nvsHandler, "status", value);
  Serial.print((err != ESP_OK) ? "Failed!\n" : "Done\n");
  ESP_ERROR_CHECK(err);
  return (err == ESP_OK);
}

void nvsErase() {
  esp_err_t err = nvs_flash_erase();
  ESP_ERROR_CHECK(err);
}

void nvsDeinit(void) {
  esp_err_t err = nvs_flash_deinit();
  ESP_ERROR_CHECK(err);
}