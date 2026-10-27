# Spot The Chibi! (57 Cards Matching Party Game)

[![CI](https://github.com/rchau8502/spot-the-chibi/actions/workflows/ci.yml/badge.svg)](https://github.com/rchau8502/spot-the-chibi/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 76 Passed](https://img.shields.io/badge/Tests-76%20Passed-brightgreen.svg)](test_suite.mjs)
[![PWA Ready](https://img.shields.io/badge/PWA-Ready-blue.svg)](web/manifest.json)
[![iOS: 1.1 (Build 4)](https://img.shields.io/badge/iOS-1.1%20(Build%204)-purple.svg)](ios/)

A complete, beautifully illustrated card game and web/iOS application based on the finite projective plane of order 7, $PG(2, 7)$.

## 🎯 Game Features
- **57 Unique Cards Per Deck**: Generated with mathematical precision.
- **8 Symbols Per Card**: Exactly 8 adorable 3D symbols per card.
- **7 Vibrant Themes (399 Total Symbols)**:
  - 🐾 **Chibi Animals**: Panda, Koala, Lion, Tiger, Dolphin, Unicorn, Cat, Dog...
  - 🍕 **Food & Snacks**: Pizza, Burger, Taco, Sushi, Donut, Boba, Ice Cream...
  - 🦸 **Superheroes**: Lightning, Shield, Cape, Mask, Gauntlet, Hammer, City Key...
  - 🚀 **Space & Galaxy**: Rocket, Astronaut, Alien, Planet, UFO, Nebula, Comet...
  - 🚗 **Vehicles & Travel**: Sports Car, Airplane, Train, Yacht, Helicopter, Submarine...
  - 🧙 **Magic & Fantasy**: Dragon, Wizard, Castle, Phoenix, Crystal, Potion, Magic Hat...
  - 🌊 **Ocean Wonders**: Dolphin, Shark, Coral Reef, Sea Turtle, Octopus, Submarine...
- **The Golden Rule**: Every pair of cards shares **EXACTLY 1** matching symbol (mathematically verified across all 1,596 pairs).
- **A4 Safe-Print Layout**: 6 cards per page with generous **16 mm safe margins** from all paper edges, guaranteed **NO CUT-OFF** on any printer.
- **Print & Cut Guides**: Features both subtle circular cut lines (84 mm / 3.3 in diameter) and precision corner crop marks for straight-edge paper trimmers.
- **Duplex Card Backs Included**: Symmetrically aligned 22-page duplex PDFs for all 7 themes with +3 mm bleed protection for seamless double-sided printing.

---

## 🌐 Web & Native App Features

- **Multi-Platform Support**:
  - Web & PWA with offline caching (Service Worker v2)
  - Native iOS App with full **`UIScene` lifecycle support** (compatible with iOS 18/19/27 & iPadOS 18+)
- **6 Engaging Game Modes**:
  - 🥊 **2-Player Versus**: Classic quick-match duel with custom score targets.
  - 🔄 **Tabletop 180° Face-to-Face**: Player 2's card and win button rotate 180° so two players can duel sitting across each other on an iPad or phone placed flat on a table!
  - ⏱️ **Solo Time Attack**: Spot 10 matches against the clock with millisecond accuracy and rank grading (S+, A, B, C).
  - 🔥 **Survival Blitz**: Race against a depleting timer (+2s per correct match), building streak combos.
  - 🃏 **Full Deck Exploration**: Clear through all 57 cards sequentially with zero repeats.
  - 🧘 **Zen Practice Mode**: Relaxed discovery with on-demand hint highlighting.
- **100% Procedural Synthesizer Sound Engine**:
  - Zero-copyright, royalty-free Web Audio API music in 4 styles: 🎉 Party Beat, 👾 8-Bit Arcade, ☕ Lo-Fi Chill, and ⚔️ PvP Showdown.
  - Sound effects for deals, correct spots, streaks, penalties, and victory fanfares.
  - Native haptic feedback integration (`@capacitor/haptics`).

---

## 📁 Included Printable PDFs (A4 Duplex Ready)

All 7 complete 22-page master PDFs are included in `PDFs/` and downloadable in the web app under `web/pdf/`:

| Theme Deck | Duplex PDF Path | Details |
| :--- | :--- | :--- |
| 🐾 **Chibi Animals** | `PDFs/chibi_animal_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |
| 🍕 **Food & Snacks** | `PDFs/food_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |
| 🦸 **Superheroes** | `PDFs/superheroes_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |
| 🚀 **Space & Galaxy** | `PDFs/space_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |
| 🚗 **Vehicles & Travel** | `PDFs/vehicles_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |
| 🧙 **Magic & Fantasy** | `PDFs/fantasy_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |
| 🌊 **Ocean Wonders** | `PDFs/ocean_spot_it_cards_A4_duplex.pdf` | 57 Cards + 3 Bonus Cards + Duplex Backs + Rules + Visual Key |

---

## 📱 iOS App Store Assets & iPhone Duo Ready

Located in `AppStore_Assets/` and `~/Desktop/Spot_The_Chibi_AppStore_Assets/`:
- **1024 x 1024 px** High-Res App Store Icon (`AppStore_Icon_1024x1024.png`)
- **iPhone Duo Inner Display** (2007 x 2853 px) in `Screenshots_iPhone_Duo_Inner_2007x2853/`
- **iPhone Duo Outer Display** (1398 x 2034 px) in `Screenshots_iPhone_Duo_Outer_1398x2034/`
- **6.7" Screenshots** (1290 x 2796 px) in `Screenshots_6.7_inch/`
- **6.5" Screenshots** (1284 x 2778 px) in `Screenshots_6.5_inch/`
- **iPhone Duo Adaptive Layout**: Full support for dual-screen foldables, W3C viewport segments (`horizontal-viewport-segments`, `vertical-viewport-segments`), and seamless 180° Tabletop 1v1 play in tent and tabletop postures.
- Zero data collection, privacy-first privacy policy (`web/privacy.html`)

---

## 🖨️ Printing & Crafting Instructions

1. **Paper Selection**: Use heavy white cardstock (**200 to 300 gsm**), or laminate regular paper before cutting.
2. **Printer Settings**: Paper Size **A4** (210 mm × 297 mm), Scaling **Actual Size / 100%**.
3. **Double-Sided Printing**: In your printer dialog, select **Duplex / Double-Sided Printing** and set flip mode to **Flip on Long Edge**.
4. **Cutting the Cards**:
   - **Circular**: Cut along the circular outlines with craft scissors or an **84 mm (3.3 inch)** punch cutter.
   - **Square**: Follow the L-shaped corner crop marks with a paper trimmer.

---

## 🧪 Automated Testing

Run the comprehensive 76-check mathematical invariant and asset integrity test suite:

```bash
npm test
```

This verifies:
- All 57 cards have exactly 8 unique symbols.
- All 1,596 distinct card pairs share exactly ONE common symbol ($PG(2, 7)$ invariant).
- All 399 symbol PNG images exist across all 7 themes.
- All 7 duplex printable A4 PDFs are valid and present.
- All PWA pre-cached assets and audio synthesizer sound tracks are operational.

---

## 🎮 How to Play (5 Mini-Games)

Between any two cards, there is **always exactly ONE matching symbol**. The first player to spot it and call out its name takes action!

1. **The Tower**: Deal 1 card face down to each player. Remaining deck face up in center. Players flip together; first to spot a match takes the center card. Most cards wins!
2. **The Well**: Place 1 card face up in center. Deal all others equally. Race to discard onto the center Well by spotting matches. First to empty hand wins!
3. **Hot Potato**: Each player holds 1 card face up. Spot a match with ANY opponent's card to pass your card onto theirs. Last player left holding cards loses the round!
4. **The Poisoned Gift**: Flip cards. Spot a match between the center card and ANY opponent's card to give the center card to them as a penalty. Fewest cards wins!
5. **Triple Spot**: Lay out 9 cards in a 3×3 grid. Race to find 3 cards that share the exact same symbol. Collect the triplet and replenish 3 new cards!

---

## 📐 Mathematical Proof ($PG(2, 7)$)
- **Field order**: $n = 7$ (prime number)
- **Total Points (Symbols)**: $N = n^2 + n + 1 = 49 + 7 + 1 = 57$
- **Total Lines (Cards)**: $M = n^2 + n + 1 = 57$
- **Points per Line (Symbols per Card)**: $k = n + 1 = 8$
- **Cards per Symbol**: $r = n + 1 = 8$
- **Pairwise intersection**: $\forall i \neq j, |Card_i \cap Card_j| = 1$
- **Pairwise combinations**: $\binom{57}{2} = 1,596$ unique card pairs, all 100% verified.
