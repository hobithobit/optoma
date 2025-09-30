#include <Arduino.h>
#include <IRrecv.h>
#include <IRsend.h>
#include <IRutils.h>

#define IR_RECEIVE_PIN 4
#define IR_SEND_PIN    5

IRrecv irrecv(IR_RECEIVE_PIN);
IRsend irsend(IR_SEND_PIN);
decode_results results;

enum Mode { MODE_RX, MODE_TX };
Mode currentMode = MODE_TX;   // ← výchozí režim = vysílání

// Uložené kódy
uint32_t irCodes[] = {
  0x40FFD42B,  // UP
  0x40FF34CB,  // DOWN
  0x40FFB44B,  // LEFT
  0x40FF748B,  // RIGHT
  0x40FFF40B,  // OK
  0x40FF22DD   // SC_LOCK
};
const char* buttonNames[] = { "UP","DOWN","LEFT","RIGHT","OK","SC_LOCK" };

void setup() {
  Serial.begin(115200);
  irrecv.enableIRIn();
  irsend.begin();
  Serial.println("ESP IR ovladač – start");
  Serial.println("MODE:TX"); // hlášení výchozího režimu
}

void loop() {
  // čtení příkazů ze Serialu
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.equalsIgnoreCase("MODE RX")) {
      currentMode = MODE_RX;
      Serial.println("MODE:RX");

    } else if (cmd.equalsIgnoreCase("MODE TX")) {
      currentMode = MODE_TX;
      Serial.println("MODE:TX");

    } else if ((cmd.startsWith("SEND") || cmd.equalsIgnoreCase("LOCK")) && currentMode == MODE_TX) {
      String btn;

      if (cmd.equalsIgnoreCase("LOCK")) {
        btn = "SC_LOCK";
      } else {
        btn = cmd.substring(4);
        btn.trim();
      }

      for (int i = 0; i < sizeof(irCodes)/sizeof(irCodes[0]); i++) {
        if (btn.equalsIgnoreCase(buttonNames[i])) {
          irsend.sendNEC(irCodes[i], 32);
          Serial.print("SENT:");
          Serial.println(buttonNames[i]);
          break;
        }
      }
    }
  }

  // režim PŘÍJEM (jen názvy tlačítek)
  if (currentMode == MODE_RX) {
    if (irrecv.decode(&results)) {
      if (results.value != 0xFFFFFFFF) { // ignoruj repeat kódy
        bool found = false;
        for (int i = 0; i < sizeof(irCodes)/sizeof(irCodes[0]); i++) {
          if (results.value == irCodes[i]) {
            Serial.print("KEY:");
            Serial.println(buttonNames[i]);
            found = true;
            break;
          }
        }
        if (!found) {
          Serial.print("UNKNOWN:");
          Serial.println(resultToHexidecimal(&results));
        }
      }
      irrecv.resume();
    }
  }
}

