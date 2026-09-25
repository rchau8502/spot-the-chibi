# Chibi Animal Spot It! (57 Cards Printable Game)

A complete, beautifully illustrated printable card game based on the finite projective plane of order 7, $PG(2, 7)$.

## 🎯 Game Features
- **57 Unique Cards**: Generated with mathematical precision.
- **8 Symbols Per Card**: Exactly 8 adorable 3D chibi animals on each card.
- **57 Total Chibi Animals**: Cat, Dog, Panda, Fox, Koala, Lion, Tiger, Frog, Owl, Dolphin, Unicorn, and 46 more!
- **The Golden Rule**: Every pair of cards shares **EXACTLY 1** matching animal (verified across all 1,596 pairs).
- **A4 Safe-Print Layout**: 6 cards per page with generous **16 mm safe margins** from all paper edges, guaranteed **NO CUT-OFF** on any printer.
- **Print & Cut Guides**: Features both subtle circular cut lines (84 mm / 3.3 in diameter) and precision corner crop marks for straight-edge paper trimmers.
- **Duplex Card Backs Included**: Symmetrically aligned 10-page card backs PDF for seamless double-sided printing.

---

## 🌐 Live Website Version (Hosted on Vercel)

🎮 **Play Online Now**: [**https://web-puce-nu-97.vercel.app**](https://web-puce-nu-97.vercel.app)
*(Alternative preview link: [https://web-8a12b56ff-richs-projects-646d2c36.vercel.app](https://web-8a12b56ff-richs-projects-646d2c36.vercel.app))*

### Web Version Features:
- **Real-Time 2-Card Arena**: Shows Card A vs Card B each round with 8 chibi animals each.
- **Manual Side Winner Input**: In real life, players spot the match and manually tap who won:
  - `👈 Player 1 Won (+1)` (Hotkey: `A` or `←` or `1`)
  - `👉 Player 2 Won (+1)` (Hotkey: `L` or `→` or `2`)
- **Reveal Match Button**: Settle any disputed call instantly by clicking **Reveal Match** to highlight the common animal in glowing gold!
- **Royalty-Free Kahoot-Style Background Music**: 100% procedural Web Audio API synth engine playing an upbeat, funky 4-on-the-floor groove with sound effects (coin chimes, card deals, victory fanfare).
- **Customizable Players & Score Target**: Click to rename players, choose target scores (first to 5, 10, 15, or free play), optional round countdown timers, and full-screen party mode.

---

## 📁 Included Files

| File | Description |
| :--- | :--- |
| **`chibi_animal_spot_it_cards_A4_duplex.pdf`** | **⭐ Complete Turnkey Duplex PDF (22 Pages)**<br>• Interleaved Front & Back: Sheet 1 Front, Sheet 1 Back, Sheet 2 Front, Sheet 2 Back...<br>• Perfect millimeter horizontal reflection symmetry for standard **"Flip on Long Edge"** printing.<br>• Includes **+3 mm bleed protection** on the backs to prevent white edges even if printer paper feeds with mechanical tolerance!<br>• Sheets 1–10: Cards #1–#57 + 3 Bonus Cards<br>• Sheet 11: Double-sided Rulebook (Rules on Front, 57 Animal Key on Back) |
| **`chibi_animal_spot_it_cards_A4.pdf`** | **Single-Sided Master PDF (12 Pages)**<br>• Pages 1–10: All card fronts<br>• Pages 11–12: Rulebook and Animal Key |
| **`chibi_animal_card_backs_A4.pdf`** | **Card Backs PDF (10 Pages)**<br>• Symmetrically mirrored 6-card grid with bleed for manual-feed printers |
| **`web/`** | Web application source directory (live on Vercel at [https://web-puce-nu-97.vercel.app](https://web-puce-nu-97.vercel.app)) |
| **`build_duplex_pdf.py`** | Python script generating the duplex PDF with mathematical horizontal symmetry and bleed |
| **`duplex_overlay_verification.png`** | Light-table transparency verification image showing perfect concentric front-to-back card alignment |
| **`preview_cards_page_1.png`** | Image preview of Page 1 (Cards 1–6). |
| **`preview_cards_page_10.png`** | Image preview of Page 10 (Cards 55–57 + Bonus Cards). |
| **`preview_rules_page_11.png`** | Image preview of Page 11 (Rulebook & Mini-Games). |
| **`preview_animal_key_page_12.png`** | Image preview of Page 12 (57 Chibi Animals Visual Key). |
| **`preview_card_backs.png`** | Image preview of the matching card backs. |



---

## 🖨️ Printing & Crafting Instructions

1. **Paper Selection**:
   - For best results, use heavy white cardstock (**200 to 300 gsm**).
   - If using regular printer paper, consider laminating the sheets before cutting for extra stiffness and durability.
2. **Printer Settings**:
   - Paper Size: **A4** (210 mm × 297 mm)
   - Scaling: **Actual Size** / **100%** (do not shrink or scale, the margins are already pre-calibrated with 16 mm padding).
3. **Double-Sided Printing (Optional)**:
   - In your printer dialog, select **Duplex / Double-Sided Printing** and set flip mode to **Flip on Long Edge**.
   - Print `chibi_animal_spot_it_cards_A4.pdf` (Pages 1–10) with `chibi_animal_card_backs_A4.pdf` on the back.
4. **Cutting the Cards**:
   - **Circular Cards**: Cut along the circular grey outlines using craft scissors or an **84 mm (3.3 inch)** circular punch cutter.
   - **Square Cards**: If you prefer straight cuts, follow the L-shaped corner crop marks with a paper trimmer or ruler & craft knife.

---

## 🎮 How to Play (5 Mini-Games)

### Core Rule:
Between any two cards, there is **always exactly ONE matching animal**. The first player to spot it and call out its name takes action!

1. **The Tower**: Deal 1 card face down to each player. Place the remaining deck face up in the center. All players flip their card simultaneously. The first player to spot and shout the matching animal between their card and the center card takes the center card onto their personal pile. The player with the most cards wins!
2. **The Well**: Place 1 card face up in the center. Deal all other cards equally to players. Players race to discard cards from their personal stack onto the center Well by spotting matches. First to empty their stack wins!
3. **Hot Potato**: Each player holds 1 card face up in their palm. When you spot a match with ANY opponent's card, shout it and place your card on theirs! They must now match their new top card to pass the growing stack. The last player left holding all cards loses the round.
4. **The Poisoned Gift**: Flip cards. Spot a match between the center card and ANY opponent's card to give the center card to them as a penalty. The player with the fewest cards wins!
5. **Triple Spot**: Lay out 9 cards in a 3×3 grid. Race to find 3 cards that share the exact same animal. Collect the triplet and replace with 3 new cards!

---

## 📐 Mathematical Proof ($PG(2, 7)$)
- **Field order**: $n = 7$ (prime number)
- **Total Points (Symbols)**: $N = n^2 + n + 1 = 49 + 7 + 1 = 57$
- **Total Lines (Cards)**: $M = n^2 + n + 1 = 57$
- **Points per Line (Symbols per Card)**: $k = n + 1 = 8$
- **Cards per Symbol**: $r = n + 1 = 8$
- **Pairwise intersection**: $\forall i \neq j, |Card_i \cap Card_j| = 1$
- **Pairwise combinations**: $\binom{57}{2} = 1,596$ unique card pairs, all 100% verified.
