# Romhack
Repository to hold documentation, code and issue tickets for the BDSP Romhack

The folder structure is setup where it is expected for you to drop [Aldo's BDSP Repacker](https://github.com/Ai0796/BDSP-Repacker) and [z80Rotom's ev-as](https://github.com/z80rotom/ev-as) into the main folder.
Therefore, whenever you change a file, it can be reflected in the repo easily and is already available for you to repack into your game file.

All files provided must be from Brilliant Diamond 1.3.0

For Aldo's repacker:
- You will need to supply your own game's dumped assets into the `AssetFolder`, at the time of writing that is `battle_masterdatas`, `common_msbt`, `contest_masterdatas`, `effectdatabase`, `english`, `gamesettings`, `masterdata` (Fureai folder), `masterdatas` (from the DPR folder), `personal_masterdatas`, `ugdata`, and finally the `uimasterdatas`.

For z80Rotom's ev-as:
- You will need to create a folder called `Dpr` and supply your own `ev_script` file there.
- Then, parse the file, which will output to the `parsed` folder. 
- Ev-as reads from the `scripts` folder by default.

The .gitignore has all these folders and files already ignored, so you shouldn't need to worry about accidentally committing them.
