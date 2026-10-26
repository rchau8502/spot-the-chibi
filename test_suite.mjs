// Automated Comprehensive Test Suite for Spot The Chibi
// Run with: node test_suite.mjs

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { THEMES, CARDS, getSharedSymbol } from './web/cards.js';
import { MUSIC_TRACKS } from './web/audio.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    passed++;
    console.log(`  ✓ PASS: ${message}`);
  } else {
    failed++;
    console.error(`  ✗ FAIL: ${message}`);
  }
}

console.log('====================================================');
console.log('🧪 SPOT THE CHIBI COMPREHENSIVE TEST SUITE');
console.log('====================================================\n');

// 1. MATHEMATICAL INVARIANTS (Projective Plane PG(2, 7))
console.log('--- 1. Mathematical Invariant Verification ---');
assert(CARDS.length === 57, `CARDS contains exactly 57 cards (found ${CARDS.length})`);

let cardLengthsValid = true;
let cardUniqueSymbolsValid = true;
const symbolFrequency = new Array(57).fill(0);

for (let i = 0; i < CARDS.length; i++) {
  const card = CARDS[i];
  if (card.length !== 8) cardLengthsValid = false;
  const set = new Set(card);
  if (set.size !== 8) cardUniqueSymbolsValid = false;
  for (const sym of card) {
    if (sym >= 0 && sym < 57) {
      symbolFrequency[sym]++;
    }
  }
}
assert(cardLengthsValid, 'Every card has exactly 8 symbols');
assert(cardUniqueSymbolsValid, 'Every card has 8 unique symbols (no duplicate symbols on single card)');

const symbolFrequenciesValid = symbolFrequency.every(count => count === 8);
assert(symbolFrequenciesValid, 'Every symbol (0-56) appears on exactly 8 cards across the deck');

let pairwiseErrors = 0;
let getSharedSymbolErrors = 0;
let totalPairs = 0;

for (let i = 0; i < CARDS.length; i++) {
  for (let j = i + 1; j < CARDS.length; j++) {
    totalPairs++;
    const s1 = new Set(CARDS[i]);
    const common = CARDS[j].filter(x => s1.has(x));
    if (common.length !== 1) {
      pairwiseErrors++;
    }
    const shared = getSharedSymbol(i, j);
    if (shared !== common[0]) {
      getSharedSymbolErrors++;
    }
  }
}

assert(totalPairs === 1596, `Tested all 57 * 56 / 2 = 1,596 distinct card pairs`);
assert(pairwiseErrors === 0, `All 1,596 pairs share exactly ONE common symbol (errors: ${pairwiseErrors})`);
assert(getSharedSymbolErrors === 0, `getSharedSymbol() matches intersection for all pairs (errors: ${getSharedSymbolErrors})`);

// 2. THEMES & ASSET INTEGRITY
console.log('\n--- 2. Theme & Asset Integrity ---');
const expectedThemes = ['animals', 'food', 'heroes', 'space', 'vehicles', 'fantasy', 'ocean'];
const actualThemes = Object.keys(THEMES);
assert(actualThemes.length === 7, `7 themes registered (found ${actualThemes.length})`);

for (const themeKey of expectedThemes) {
  const theme = THEMES[themeKey];
  assert(!!theme, `Theme "${themeKey}" is defined`);
  assert(theme.symbols.length === 57, `Theme "${themeKey}" contains 57 symbol definitions`);

  let missingPngs = 0;
  for (const sym of theme.symbols) {
    const pngPath = path.join(__dirname, 'web', themeKey, `${sym.slug}.png`);
    if (!fs.existsSync(pngPath)) {
      missingPngs++;
    }
  }
  assert(missingPngs === 0, `Theme "${themeKey}": all 57 PNG image files exist on disk`);
}

// 3. PRINTABLE DUPLEX PDFS
console.log('\n--- 3. Printable Duplex PDF Verification ---');
const pdfFiles = [
  'chibi_animal_spot_it_cards_A4_duplex.pdf',
  'food_spot_it_cards_A4_duplex.pdf',
  'superheroes_spot_it_cards_A4_duplex.pdf',
  'space_spot_it_cards_A4_duplex.pdf',
  'vehicles_spot_it_cards_A4_duplex.pdf',
  'fantasy_spot_it_cards_A4_duplex.pdf',
  'ocean_spot_it_cards_A4_duplex.pdf'
];

for (const pdf of pdfFiles) {
  const webPdf = path.join(__dirname, 'web', 'pdf', pdf);
  const rootPdf = path.join(__dirname, 'PDFs', pdf);
  assert(fs.existsSync(webPdf), `web/pdf/${pdf} exists`);
  assert(fs.existsSync(rootPdf), `PDFs/${pdf} exists`);
  if (fs.existsSync(webPdf)) {
    const stat = fs.statSync(webPdf);
    assert(stat.size > 1024 * 1024, `web/pdf/${pdf} has valid file size (${(stat.size / 1024 / 1024).toFixed(1)} MB)`);
  }
}

// 4. WEB APP & PWA INTEGRITY
console.log('\n--- 4. Web & PWA Configuration ---');
const requiredWebFiles = [
  'web/index.html',
  'web/style.css',
  'web/app.js',
  'web/cards.js',
  'web/audio.js',
  'web/sw.js',
  'web/manifest.json',
  'web/qrcode.png'
];

for (const rf of requiredWebFiles) {
  assert(fs.existsSync(path.join(__dirname, rf)), `${rf} exists`);
}

// Verify index.html PDF links
const indexHtml = fs.readFileSync(path.join(__dirname, 'web/index.html'), 'utf8');
for (const pdf of pdfFiles) {
  assert(indexHtml.includes(`pdf/${pdf}`), `index.html contains download link to pdf/${pdf}`);
}

// Verify sw.js pre-cache references
const swJs = fs.readFileSync(path.join(__dirname, 'web/sw.js'), 'utf8');
const cachedAssets = ['./index.html', './style.css', './app.js', './cards.js', './audio.js', './manifest.json'];
for (const asset of cachedAssets) {
  const relPath = path.join('web', asset.replace('./', ''));
  assert(fs.existsSync(path.join(__dirname, relPath)), `sw.js cached asset ${asset} exists on disk`);
}

// 5. AUDIO ENGINE TRACKS
console.log('\n--- 5. Audio Synthesizer Tracks ---');
assert(MUSIC_TRACKS.length === 4, `4 procedural soundtrack tracks defined (found ${MUSIC_TRACKS.length})`);
for (const trk of MUSIC_TRACKS) {
  assert(trk.bpm >= 60 && trk.bpm <= 200, `Track "${trk.name}" has valid BPM (${trk.bpm})`);
}

console.log('\n====================================================');
console.log(`SUMMARY: ${passed} PASSED, ${failed} FAILED`);
console.log('====================================================');

if (failed > 0) {
  process.exit(1);
} else {
  console.log('🎉 ALL INTEGRITY AND REGRESSION TESTS PASSED CLEANLY!\n');
}
