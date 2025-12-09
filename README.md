# BIOS4096
*A procedurally generated top-down action dungeon crawler built in Python + Pygame.*

---

## Overview

**BIOS4096** is a fast-paced rogue-lite dungeon crawler featuring:

- Procedural dungeon generation (PCG)
- Dynamic enemy AI (roaming, chasing, ranged attacks, charge attacks)
- Ranged and melee combat
- Player upgrades and inventory system
- Multi-stage boss fights
- Sound effects and dynamic music transitions
- Minimap exploration system
- Resolution scaling and settings menu

The game is built in **Python** using **Pygame**, with modular architecture for easy expansion.

---

## Features

### Procedural Dungeon Generation (PCG)
Every run is different thanks to fully procedural systems:

- Random room graph generation  
- Start, treasure, and boss room selection  
- Procedural tilemap generation  
- Random floor and wall tiles  
- Door placement based on room connectivity  

---

### Combat System
The player can:

- Fire ranged weapons  
- Perform melee slashes  
- Swap weapons  
- Knock back enemies  
- Fight enemies with unique AI behaviors  

Enemy types include:

- **Grunts** — ranged shooters  
- **Brutes** — fast charging melee units  
- **Bosses** — multi-stage encounters with unique attack pools  

---

### Upgrade System
Treasure rooms contain randomly selected upgrades such as:

- Movement speed boosts  
- Weapon damage boosts  
- Projectile color/behavior changes  

Upgrades appear visually in the room and are added to the player's inventory when collected.

---

### Minimap Visualizer
Shows:

- Rooms the player has visited  
- Player’s current location  
- Special rooms (Start, Treasure, Boss)  

Updates dynamically with dungeon exploration.

---

### Audio System
Features:

- **Menu music**
- **Level / dungeon music**
- **Boss battle music**
- Sound effects for:
  - Shooting  
  - Melee attacks  
  - Player death  
  - Grunt death  
  - Brute death  
  - Upgrade pickup  

Music can be toggled or adjusted via the Settings Menu.

---

### Settings Menu
Players can:

- Toggle music on/off  
- Change music volume  
- Switch between multiple resolutions  
- Return to main menu with **ESC**  

All UI elements scale with the selected resolution.

---

## Installation

### Requirements
- Python 3.9+
- Pygame 2.0+

### Install Dependencies
 - ```bash
 - pip install pygame

## Controls
 - Action	        Key
 - Move	            WASD
 - Shoot / Attack	SPACE
 - Switch Weapon	X
 - Return to Menu	ESC
 - Toggle Music	    M
 - Volume Up / Down	↑ / ↓
 - Settings Menu	From Main Menu

## Enemy AI System

 - Enemy AI operates using a simple but effective  state machine:

 - Roaming — Enemies wander randomly when unaware of the player

 - Chasing — Enemies pursue the player when within aggro distance

 - Attacking — Enemies perform ranged or melee attacks depending on type

 - Charge Attack (Brute)

 - Windup → Charge → Cooldown cycle

 - Collision-aware movement

 - Player knockback on hit

 - Bosses feature:

 - Multi-stage combat based on HP thresholds

 - Unique attack lists

 - Large sprites and arena-centered positioning

## Author
 - Nathan Vaughn
 - Developer & Designer of BIOS4096