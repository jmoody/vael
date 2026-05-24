# D-Scan Overview Filters — Hauler / Survival Setup

Quick-build reference for setting up a dedicated D-Scan overview tab in EVE Online.
Optimized for hauling, exploration, and "I just want to know if something is hunting me."

## Setup

Right-click overview tab → **Open Overview Settings** → **Tabs** → **New Tab** → name it `DScan-Threats`.

## Tab: `DScan-Threats`

### Filter → Types (check ONLY these)

| Category | Subgroups | Why |
|---|---|---|
| **Ship** | ALL | Anything that can shoot you |
| **Drone** | Combat Drones, Fighter, Fighter-Bomber | Active fights on grid |
| **Deployable** | Mobile Warp Disruptor (bubbles), Mobile Cyno Inhibitor | Tackle + ambush prep |
| **Charge** | Scanner Probe (ALL — Core + Combat) | **CRITICAL: combat probes = active hunter** |
| **Celestial** | Wreck | Recent kills = active PvP nearby |

### Filter → Types (UNCHECK everything else)

- Asteroid (noise)
- Station / Stargate / Structure (always there, noise)
- Cargo Container (mostly junk)
- NPC / Entity (PvE noise)
- Orbital infrastructure (POCO, etc.)

### Filter → States (keep ALL checked)

- Pilot has security status above 0
- Pilot has security status below 0
- Pilot has bounty
- Pilot is at war
- Pilot is in your fleet → **UNCHECK** (don't hide blues; you want to see everyone)
- Pilot is in your alliance
- Pilot is in your corporation
- Pilot has neutral standing
- Pilot has positive/negative standing (all)

## D-Scan Window Settings

- **Range slider:** MAX (`14,300,000,000` m = 14.3 AU)
- **Angle:** 360° for normal pulses
- **"Use Active Overview Settings":** CHECKED (while DScan-Threats tab is active)

## Optional Pro Move: Second Tab `DScan-Narrow`

Same filters as `DScan-Threats`. Use this tab + narrow angle (5°) + camera-point-at-celestial to triangulate hunters or safespotted ships.

## Usage Discipline

- **Press `V` every 5-10 seconds** while in space. Always.
- **In station:** still pulse d-scan periodically. If combat probes appear before undock, **WAIT**.
- **On gates (cloaked):** spam d-scan. New ships = inbound jumpers.
- **In lowsec/nullsec:** d-scan immediately on grid load, before doing anything else.

## Red-Flag D-Scan Hits

| Ship Class | Names | Threat |
|---|---|---|
| Interceptors | Stiletto, Crow, Malediction, Ares, Crusader, Raptor, Taranis, Claw | Fast tackle, ignores bubbles |
| Interdictors | Sabre, Flycatcher, Heretic, Eris | **Drops bubbles** — cloak is your only out |
| Heavy Interdictors | Broadsword, Phobos, Onyx, Devoter | Infinite point + bubble |
| Recons (cloaky) | Arazu, Lachesis, Rapier, Huginn, Pilgrim, Curse, Falcon, Rook | Long-range tackle / jam |
| T3 Cruisers | Loki, Proteus, Tengu, Legion | Cloaky, deadly, common in lowsec |
| **Combat Scanner Probes** | (in scan, not on grid) | **Someone is actively hunting** |

## Last Word

D-scan is free. Paranoia is professionalism. The pilot who pulses every 5 seconds doesn't die to gate camps.
