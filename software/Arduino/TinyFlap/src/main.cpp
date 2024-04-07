#include <TFT_eSPI.h>
#include <SPI.h>
#include <Ticker.h>
#include <Preferences.h>
//#include "bg.h" // Using background image requires some fiddling with transparent sprites that goes on top of the image.

#define LEFT 0
#define RIGHT 11

#define MODE_1_PROGRESSIVE 1
#define MODE_2_NORMAL 2
#define MODE_3_HARD 3

#define HIGH_SCORES "high_scores"

TFT_eSPI tft = TFT_eSPI();
TFT_eSprite sprite = TFT_eSprite(&tft);
TFT_eSprite logoSpr = TFT_eSprite(&tft);
TFT_eSprite logoBgSpr = TFT_eSprite(&tft);
TFT_eSprite gameOverSpr = TFT_eSprite(&tft);

const int REFRESH_RATE = 20;
unsigned long lastFrame = 0;

bool jumpButtonPressed = false;

float gravity = 0.3;
float jumpStrength = 2.2;

uint16_t modeTextColor ;
uint16_t modeBgColor;

const int BIRD_W = 26;
const int BIRD_H = 20;
uint16_t birdColor;
float birdY = 64;
float birdSpeed = 0;
int birdAngle = 0;

int pipeX = 128;
int pipeGapY = 60;
int pipeGapSize = 40;
int pipeSpeed = 2; // Even numbers only

const int GROUND_STRIPE_HEIGHT = 5;
const int GROUND_STRIPE_WIDTH = 8;
int groundPos = 0;
int groundSpeed = pipeSpeed / 2;

int cloud1X = 20;
int cloud1Y = 20;
int cloud2X = 80;
int cloud2Y = 40;

const float FLAP_INTERVAL = 0.15;
Ticker flapTicker;

int score = 0;
Preferences highScores;
int bestScore = 0;
bool newBestScore = false;

bool ready = false;
bool collision = false;

const int flapStates[] = {1, 2, 3, 2};
const int numFlapStates = sizeof(flapStates) / sizeof(flapStates[0]);
int currentFlapStateIndex = 0;
int flapState = flapStates[currentFlapStateIndex];

const int gameModes[] = {1, 2, 3};
const int numGameModes = sizeof(gameModes) / sizeof(gameModes[0]);
int currentGameModeIndex = 1;
int gameMode = gameModes[currentGameModeIndex];
void setGameMode(int pGameMode);
void flapTick() ;
void setup() {

  pinMode(LEFT, INPUT_PULLUP);
  pinMode(RIGHT, INPUT_PULLUP);

  highScores.begin(HIGH_SCORES, false);

  flapTicker.attach(FLAP_INTERVAL, flapTick);

  tft.init();
  tft.setRotation(2);
  //tft.setSwapBytes(true);

  sprite.createSprite(128,128);
  //sprite.setSwapBytes(true);

  logoBgSpr.createSprite(128, 64);
  logoSpr.createSprite(128, 64);

  setGameMode(gameMode);

}

void setGameMode(int pGameMode) {
  switch(pGameMode) {
    case MODE_1_PROGRESSIVE:
      gravity = 0.3;
      jumpStrength = 2.2;
      pipeGapSize = 160;
      birdColor = TFT_CYAN;
      modeTextColor = TFT_BLACK;
      break;
    case MODE_2_NORMAL:
      gravity = 0.3;
      jumpStrength = 2.2;
      pipeGapSize = 40;
      birdColor = TFT_GOLD;
      modeTextColor = TFT_BLACK;
      break;
    case MODE_3_HARD:
      gravity = 0.4;
      jumpStrength = 4;
      pipeGapSize = 40;
      birdColor = TFT_OLIVE;
      modeTextColor = TFT_WHITE;
      break;
    default:
      ;
  }
  modeBgColor = birdColor;
}

void toggleGameMode() {
  currentGameModeIndex = (currentGameModeIndex + 1) % numGameModes;
  gameMode = gameModes[currentGameModeIndex];

  setGameMode(gameMode);
}

void flapTick() {
  currentFlapStateIndex = (currentFlapStateIndex + 1) % numFlapStates;
  flapState = flapStates[currentFlapStateIndex];
}

TFT_eSprite drawBird() {

  if (collision) {
    birdColor = TFT_LIGHTGREY; // TFT_RED;
  } 

  float x = (BIRD_W / 2) - 4;
  float y = BIRD_H / 2;

  TFT_eSprite birdBackSpr = TFT_eSprite(&tft);
  birdBackSpr.createSprite(BIRD_W + 2, BIRD_H + 2);
  birdBackSpr.fillSprite(TFT_SKYBLUE);

  TFT_eSprite birdSpr = TFT_eSprite(&tft);
  birdSpr.createSprite(BIRD_W, BIRD_H);
  birdSpr.fillSprite(TFT_SKYBLUE);

  // Body and Head
  birdSpr.fillSmoothCircle(x, y, 7, TFT_BLACK); // Body outline
  birdSpr.fillSmoothCircle(x + 5, y, 6, TFT_BLACK); // Head outline
  birdSpr.fillSmoothCircle(x, y, 6, birdColor);
  birdSpr.fillSmoothCircle(x + 5, y, 5, birdColor);

  // Beak
  birdSpr.fillSmoothRoundRect(x + 5, y - 1, 9, 7, 2, TFT_BLACK);
  birdSpr.fillSmoothRoundRect(x + 6, y, 7, 5, 2, TFT_ORANGE);
  int mouthX = (collision) ? x + 7 : x + 8;
  int mouthY = (collision) ? y + 2 : y + 3;
  int mouthW = (collision) ? 6 : 5;
  birdSpr.drawFastHLine(mouthX, mouthY, mouthW, TFT_BLACK);

  // Eye
  birdSpr.fillSmoothCircle(x + 7, y - 3, 3, TFT_BLACK);
  birdSpr.fillSmoothCircle(x + 7, y - 3, 2, TFT_WHITE);
  int eyeBallX = (collision) ? x + 7 : x + 8;
  birdSpr.fillSmoothCircle(eyeBallX, y - 3, 1, TFT_BLACK);

  // Flappy wing
  if (collision) {
    flapState = 2;
  }
  switch(flapState) {
    case 1: // down
      birdSpr.fillSmoothRoundRect(x - 8, y - 1, 10, 7, 2, TFT_BLACK);
      birdSpr.fillSmoothRoundRect(x - 7, y, 8, 5, 2, birdColor);
      break;
    case 2: // neutral
      birdSpr.fillSmoothRoundRect(x - 8, y - 2, 10, 4, 2, TFT_BLACK);
      birdSpr.fillSmoothRoundRect(x - 7, y - 1, 8, 2, 2, birdColor);
      break;
    case 3: // up
      birdSpr.fillSmoothRoundRect(x - 7, y - 4, 10, 6, 2, TFT_BLACK);
      birdSpr.fillSmoothRoundRect(x - 6, y - 3, 8, 4, 2, TFT_PINK);
      break;
    default:
      ; 
  }

  birdSpr.pushRotated(&birdBackSpr, birdAngle, TFT_SKYBLUE);

  return birdBackSpr;
}

void drawCloud(int pX, int pY) {
  uint16_t cloudColor = TFT_WHITE;

  // Draw cloud circles
  sprite.fillCircle(pX, pY, 4, cloudColor);
  sprite.fillCircle(pX + 5, pY + 2, 5, cloudColor);
  sprite.fillCircle(pX + 12, pY, 4, cloudColor);
  sprite.fillCircle(pX + 9, pY - 2, 3, cloudColor);
}

void drawClouds() {
  // Update cloud positions
  cloud1X -= 1;
  cloud2X -= 1;

  if (cloud1X < -16) {
    cloud1X = 128;
    cloud1Y = random(15, 45);
  }

  if (cloud2X < -16) {
    cloud2X = 128;
    cloud2Y = random(15, 45);
  }

  // Draw clouds
  drawCloud(cloud1X, cloud1Y);
  drawCloud(cloud2X, cloud2Y);
}

void drawBackground() {
  // Using background image requires some fiddling with transparent sprites that goes on top of the image.
  return;
  //sprite.pushImage(0, 0, 128, 128, bg);
}

void drawPipes() {
  // Update pipe position
  pipeX -= pipeSpeed;

  if (pipeX < -6) {
    pipeX = 128;
    pipeGapY = random(24, 90);
    score += 1;

    if (gameMode == MODE_1_PROGRESSIVE && pipeGapSize > 40) {
      pipeGapSize -= 1;
    }
  }

  // Draw pipes
  int x = pipeX;
  int gapY = pipeGapY;

  // Upper pipe
  sprite.fillRect(x-1, 0-1, 6+2, (gapY - pipeGapSize / 2) + 2, TFT_BLACK);
  sprite.fillRectHGradient(x, 0, 3, gapY - pipeGapSize / 2, TFT_GREEN, TFT_DARKGREEN);
  sprite.fillRectHGradient(x+3, 0, 3, gapY - pipeGapSize / 2, TFT_DARKGREEN, TFT_GREEN);

  sprite.fillRect((x - 2) - 1, (gapY - pipeGapSize / 2 - 4) - 1, 10 + 2, 4 + 2, TFT_BLACK);
  sprite.fillRect(x - 2, gapY - pipeGapSize / 2 - 4, 10, 4, TFT_GREEN);
  
  // Lower pipe
  sprite.fillRect(x - 1, (gapY + pipeGapSize / 2) - 1, 6 + 2, (128 - (gapY + pipeGapSize / 2)) + 2, TFT_BLACK);
  sprite.fillRectHGradient(x, gapY + pipeGapSize / 2, 3, 128 - (gapY + pipeGapSize / 2), TFT_GREEN, TFT_DARKGREEN);
  sprite.fillRectHGradient(x+3, gapY + pipeGapSize / 2, 3, 128 - (gapY + pipeGapSize / 2), TFT_DARKGREEN, TFT_GREEN);

  sprite.fillRect((x - 2) - 1, (gapY + pipeGapSize / 2) - 1, 10 + 2, 4 + 2, TFT_BLACK);
  sprite.fillRect(x - 2, gapY + pipeGapSize / 2, 10, 4, TFT_GREEN);
}

void drawGround() {
  int screenOffsetX = -groundPos % GROUND_STRIPE_WIDTH * 2;
  int stripeCount = (tft.width() + GROUND_STRIPE_WIDTH) / GROUND_STRIPE_WIDTH + 1;

  sprite.drawFastHLine(0, 128 - 7, 128, TFT_BLACK);
  sprite.drawFastHLine(0, 128 - 6, 128, TFT_BROWN);
  
  // Draw the ground stripes at the current position
  for (int i = 0; i < stripeCount; i++) {
    uint16_t stripeColor = (i % 2 == 0) ? TFT_GREEN : TFT_DARKGREEN;
    int x = i * GROUND_STRIPE_WIDTH + screenOffsetX;
    int y = tft.height() - GROUND_STRIPE_HEIGHT;
    int w = GROUND_STRIPE_WIDTH;
    int h = GROUND_STRIPE_HEIGHT;
    if (x + w > 0 && x < tft.width()) {
      sprite.fillRect(max(x, 0), y, min(w, tft.width() - x), h, stripeColor);
    }
  }

  groundPos += groundSpeed;

  // If the ground has moved past the width of the screen, reset it's position
  if (groundPos >= GROUND_STRIPE_WIDTH) {
    groundPos = 0;
  }
}

void drawScore() {
  sprite.setTextColor(TFT_DARKGREY, TFT_SKYBLUE);
  sprite.setTextSize(2);
  sprite.setTextDatum(TR_DATUM);
  sprite.drawString(String(score), 126, 2);
}

void logo() {
  String logoText = "TinyFlap";
  
  logoBgSpr.fillSprite(TFT_SKYBLUE);
  logoBgSpr.setTextDatum(MC_DATUM);
  logoBgSpr.setTextSize(2);

  logoBgSpr.setTextColor(TFT_DARKGREEN, TFT_SKYBLUE);
  logoBgSpr.drawString(logoText, 66, 33);
  logoBgSpr.pushToSprite(&sprite, 0, 0, TFT_SKYBLUE);

  logoSpr.fillSprite(TFT_SKYBLUE);
  logoSpr.setTextDatum(MC_DATUM);
  logoSpr.setTextSize(2);

  logoSpr.setTextColor(TFT_GREENYELLOW, TFT_SKYBLUE);
  logoSpr.drawString(logoText, 64, 32);
  logoSpr.pushToSprite(&sprite, 0, 0, TFT_SKYBLUE);
}

void drawGetReady() {

  logo();

  sprite.setTextDatum(MC_DATUM);
  sprite.setTextSize(2);

  sprite.setTextColor(TFT_DARKGREY, TFT_SKYBLUE);
  sprite.setTextSize(1);

  sprite.drawString("GET READY!", 64, 64);

  String modeText;
  switch(gameMode) {
    case MODE_1_PROGRESSIVE:
      modeText = "- progressive -";
      break;
    case MODE_2_NORMAL:
      modeText = "- normal -";
      break;
    case MODE_3_HARD:
      modeText = "- hard -";
      break;
    default:
      ;
  }
  sprite.drawString(modeText, 64, 90); // Mode display

  sprite.setTextDatum(BR_DATUM);
  sprite.drawString("START", 124, 117); // Start

  sprite.setTextDatum(BL_DATUM);
  sprite.drawString("MODE", 4, 117); // Mode select
}

void gameOver() {
  gameOverSpr.createSprite(96, 105);

  gameOverSpr.fillSprite(TFT_SKYBLUE);
  gameOverSpr.fillSmoothRoundRect(0, 0, 80, 80, 5, TFT_BLACK); //, TFT_SKYBLUE
  gameOverSpr.fillSmoothRoundRect(1, 1, 78, 78, 4, modeBgColor);

  gameOverSpr.setTextColor(modeTextColor, modeBgColor);
  gameOverSpr.setTextSize(1);
  gameOverSpr.setTextDatum(TC_DATUM);

  gameOverSpr.drawString("SCORE", 40, 10);
  String bestScoreText;
  if (newBestScore) {
    bestScoreText = "NEW BEST";
  } else {
    bestScoreText = "BEST";
  }
  gameOverSpr.drawString(bestScoreText, 40, 45);

  gameOverSpr.setTextSize(2);
  gameOverSpr.drawString(String(score), 40, 22);
  gameOverSpr.drawString(String(bestScore), 40, 57);

  gameOverSpr.setTextColor(TFT_DARKGREY, TFT_SKYBLUE);
  gameOverSpr.setTextSize(1);
  gameOverSpr.setTextDatum(BR_DATUM);
  gameOverSpr.drawString("CONTINUE", 92, 101);

  gameOverSpr.pushSprite(32, 16);
}

void drawFrame() {
  sprite.fillSprite(TFT_SKYBLUE);

  drawBackground();

  drawClouds();

  if (ready) {
    drawPipes();
  }
  
  drawGround();

  if (ready && !collision) {
    drawScore();
  }
  
  drawBird().pushToSprite(&sprite, -1 /*Offset*/, birdY - (BIRD_H / 2), TFT_SKYBLUE);

  if (!ready) {
    drawGetReady();
  }

  sprite.pushSprite(0, 0);
}

int getHighScore() {
  int prefHighScore;
  switch(gameMode) {
    case MODE_1_PROGRESSIVE:
      prefHighScore = highScores.getInt("game_mode_1", 0);
      break;
    case MODE_2_NORMAL:
      prefHighScore = highScores.getInt("game_mode_2", 0);
      break;
    case MODE_3_HARD:
      prefHighScore = highScores.getInt("game_mode_3", 0);
      break;
    default:
      ;
  }
  return prefHighScore;
}

void setHighScore(int pScore) {
  switch(gameMode) {
    case MODE_1_PROGRESSIVE:
      highScores.putInt("game_mode_1", pScore);
      break;
    case MODE_2_NORMAL:
      highScores.putInt("game_mode_2", pScore);
      break;
    case MODE_3_HARD:
      highScores.putInt("game_mode_3", pScore);
      break;
    default:
      ;
  }
  bestScore = pScore;
}

void resetGame() {
  birdY = 64;
  birdSpeed = 0;
  birdAngle = 0;
  pipeX = 128;
  score = 0;
  bestScore = getHighScore();
  newBestScore = false;
  setGameMode(gameMode); // Calling this to reset values in "progressive mode", bird color etc.
  collision = false;
  ready = false;
}

void loop() {

  // Get ready
  while (!ready) {
    drawFrame();
    delay(REFRESH_RATE);

    if (digitalRead(RIGHT) == LOW) {
      resetGame();
      ready = true;
      break;
    }

    if (digitalRead(LEFT) == LOW) {
      toggleGameMode();
      while (digitalRead(LEFT) == LOW) {
        delay(REFRESH_RATE);
      }
    }
  }

  // Collision
  while (collision) {

    if (score > bestScore) {
      newBestScore = true;
      setHighScore(score);
    }

    delay(600);
    gameOver();

    while (jumpButtonPressed) { // Safty to avoid unintended game reset
      if (digitalRead(RIGHT) == HIGH) {
        jumpButtonPressed = false;
      }
    }

    bool halt = true;
    while (halt) {
      while (digitalRead(RIGHT) == LOW) {
        resetGame();
        halt = false;
      }

      // Clear high score
      if (digitalRead(LEFT) == LOW) {
        int resetStart = millis();
        while (digitalRead(LEFT) == LOW) {
          if (millis() - resetStart > 8000) {
            setHighScore(0); // Clearing high score
            gameOver(); // Re-drawing to refresh high score in view
            break;
          }
        }
      }

    }
  }

  // Gameplay
  unsigned long currentMillis = millis();
  if (currentMillis - lastFrame >= REFRESH_RATE) {
    lastFrame = currentMillis;

    // Update bird position and angle
    birdSpeed += gravity;
    birdY += birdSpeed;
    tft.setPivot(12, birdY);
    birdAngle = std::max(-45, std::min(static_cast<int>(birdSpeed * 7), 60));

    // Check for collisions
    if (birdY < -128 /* Top screen is not the limit */ 
      || birdY > 128 - 10 /*Bird*/ - 3 /* Ground */ 
      || (pipeX < 18 && pipeX > 0 && (birdY < pipeGapY - pipeGapSize / 2 
        || birdY > pipeGapY + pipeGapSize / 2))) 
    {
      collision = true;
    }

    drawFrame();

    // Check for input
    if (digitalRead(RIGHT) == LOW) {
      birdSpeed = -jumpStrength;
      birdAngle = -30;
      jumpButtonPressed = true;
    } else {
      jumpButtonPressed = false;
    }

    if (digitalRead(LEFT) == LOW) {
      pipeSpeed = 4;
    } else {
      pipeSpeed = 2;
    }
    groundSpeed = pipeSpeed / 2;
  }
}