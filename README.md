# GTPR
Genshin Impact Power Ranking - a tool for determining which character's artifacts are the most worthwhile building.

GTPR considers:
- The build level of a character.
- The difficulty of upgrading a character.  

# Formulas
The build level of a character is determined as:  

$current\ DPS$: The team's current DPS  
$DPS\ floor$: The team's DPS with all of the character's offensive substats removed
           (keeping required stats like ER and CR for fav).  
$DPS\ ceiling$: The team's DPS with the character using mathematically perfect substats.

```math
Character\ build\ level\ (\%) = \dfrac{current\ DPS - DPS\ floor}{DPS\ ceiling - DPS\ floor}
```

The difficulty of upgrading a character is determined as:
> [!NOTE]
> The number is in the form of a negative modifier - a smaller value means more difficult.

$roll\ value$: The total amount of useful rolls on the current character where 1 max roll = 100.
            This assumes that the number of useful rolls of a particular stat is never greater 
            than the number of rolls of that stat given by the rolls assigned in the DPS ceiling.  
$45$: The maximum number of rolls for any character.  
$15$: The standard deviation of roll distribution among all artifacts.  
```math
Upgrade\ difficulty\ modifier\ (\%) = \dfrac{e^{-\left( \dfrac{roll\ value}{1500}\right)^2} - e^{-\left( \dfrac{4500}{1500}\right)^2}}{1-e^{-\left(\dfrac{4500}{1500} \right)^2}}
```

The priority score of upgrading a character is determined as:
> [!NOTE]
> This value takes into account the difficulty of an upgrade and with that normalized calculates 
by how much would team DPS increase by were that upgrade to be made.  

current DPS: The team's current DPS  
DPS ceiling: The team's DPS with the character using mathematically perfect substats.  
Upgrade difficulty modifier: Explained above  
$Priority\ score\ (raw) = (DPS\ ceiling - current\ DPS) \times (Upgrade\ difficulty\ modifier)$

## Obtaining the values used in the formulas
Current DPS:
- Using GCSIM (RECOMMENDED):
    - Use [gcsim](https://gcsim.app/simulator) to find your desired rotation/team.
    - Replace static values e.g. constellations, weapons, artifact sets and talent levels with your own.
    - Run a sample simulation and download it.
    - Use [gcsim to multiopt](https://thebertdark.github.io/gcsim-to-multiopt/) to convert the rotation into an accurate 
    Genshin Optimiser multi-optimisation target.
    - Use a scanner such as [Irminsul](https://konkers.github.io/irminsul/02-quickstart.html) to get all your current 
    characters, their builds and your artifacts.
    - Import the data into [Genshin Optimiser](https://frzyc.github.io/genshin-optimizer). Add any external 
    requirements e.g. ER, or CR for fav.
    - Create a new multi-optimisation target and import your config from the gcsim to multiopt website.
    - Optimize and equip your artifacts. Determine your new stats from in game and input these back into the gcsim 
    simulation.
    - Rerun the simulation. You now have your current DPS.
- You could also use a Miliastra Wonderland DPS tester level to test how close you match the simulated DPS.
- As long as DPS floor, ceiling and current DPS are consistent for all characters, you could technically use heuristics 
and set the current DPS as your artifact roll value directly.  

DPS floor (per character):
- Using gcsim (RECOMMENDED):
    - Simply remove all the listed stats except for needed ones such as ER and CR if using fav, (for 1 character) 
    and rerun the simulation.
- If using heuristics using roll value directly, just leave it at 0.

DPS ceiling (per character):
- Using gcsim (RECOMMENDED):
  - In Genshin Optimiser, Create a new TC (Theorycraft) build.
  - Add the same weapon you used, and the most optimal mainstats (the ones used in the original gcsim simulation).
  - Optimise using your multi-optimisation target. Click the gcsim Export button and copy the main and substat values.
  - Replace the character's stats with the copied stats and rerun the simulation. You now have the DPS ceiling.
- If using heuristics using roll value directly, enter 4500.

Roll value (per character):
- Using gcsim:
  - Make note of the number of rolls in each stat for the DPS ceiling calculated from Genshin Optimiser.
  - Switch to your current (non-TC) build in Genshin Optimiser. The overview screen shows the roll values for each 
  substat (e.g. 450% = 450).
  - Sum these up for the relevant stats the TC build optimised for, ensuring you don't exceed 
  the number of rolls given (e.g. if the TC Build only put 2 rolls into flat ATK, only count 200% as the max possible 
  rolls.).
  - This is your roll value. Average values range from 1000 to 4000 (e.g. 10 good max rolls to 40/45 good max rolls).

# Installation
Binaries are not provided yet. The only way to run the app is through the source code.  
Requirements:
- uv: 0.12.7+
- make: 4.4.1+

While the latest commit on the master branch will always run, for a stable experience I recommend cloning the repo at 
the latest tagged version.

```bash
# Remove --branch if you just want the latest commit
git clone --depth 1 --branch <tag_name> https://github.com/r5ne/gtpr
cd gtpr
make
```

# Credits
- The creator of Irminsul: https://github.com/konkers
- The Genshin Optimiser contributors: https://github.com/frzyc/genshin-optimizer/graphs/contributors
- The gcsim contributors: https://github.com/genshinsim/gcsim/graphs/contributors
- The creator of the gcsim-to-multiopt tool: https://github.com/thebertdark