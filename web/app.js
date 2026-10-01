import { THEMES, ANIMALS, CARDS, getSharedSymbol } from './cards.js';
import { soundEngine, MUSIC_TRACKS } from './audio.js';

// --- Game State ---
const state = {
  p1Score: 0,
  p2Score: 0,
  p1Name: 'Player 1',
  p2Name: 'Player 2',
  round: 1,
  targetScore: 10,
  currentCard1: 0,
  currentCard2: 1,
  sharedSymbol: -1,
  isRevealed: false,
  sfxEnabled: true,
  hapticsEnabled: localStorage.getItem('chibi_haptics') !== 'false',
  autoNextOnPoint: true,
  timerSeconds: 0,
  timerCurrent: 0,
  timerInterval: null,
  instanceId: '',
  currentTheme: localStorage.getItem('chibi_theme') || 'animals',
  gameMode: 'versus', // 'versus' | 'tabletop' | 'survival' | 'solo' | 'zen' | 'deck'
  tabletopActive: false,
  p1Locked: false,
  p2Locked: false,
  antispamEnabled: true,
  soloStartTime: 0,
  soloTimerInterval: null,
  soloMatches: 0,
  soloTarget: 10,
  survivalTime: 8.0,
  survivalMaxTime: 10.0,
  survivalStreak: 0,
  survivalMatches: 0,
  survivalInterval: null,
  deckCards: [],
  deckIndex: 0,
  hasUserInteracted: false
};

// --- Haptic Feedback Engine ---
const haptics = {
  impact(style = 'light') {
    if (!state.hapticsEnabled) return;
    try {
      if (navigator.vibrate) {
        if (style === 'light') navigator.vibrate(25);
        else navigator.vibrate(45);
      }
      if (window.Capacitor?.isPluginAvailable?.('Haptics')) {
        window.Capacitor.Plugins.Haptics.impact({ style: style.toUpperCase() });
      }
    } catch (_) {}
  },
  success() {
    if (!state.hapticsEnabled) return;
    try {
      if (navigator.vibrate) navigator.vibrate([30, 25, 40]);
      if (window.Capacitor?.isPluginAvailable?.('Haptics')) {
        window.Capacitor.Plugins.Haptics.notification({ type: 'SUCCESS' });
      }
    } catch (_) {}
  },
  warning() {
    if (!state.hapticsEnabled) return;
    try {
      if (navigator.vibrate) navigator.vibrate([60, 40, 60]);
      if (window.Capacitor?.isPluginAvailable?.('Haptics')) {
        window.Capacitor.Plugins.Haptics.notification({ type: 'WARNING' });
      }
    } catch (_) {}
  }
};

// Layout templates for 8 symbols inside circle (normalized 0-100%)
const LAYOUT_PRESETS = [
  // 1 center, 7 outer ring
  [
    { x: 50, y: 50, size: 28, rot: 5 },
    { x: 50, y: 19, size: 23, rot: -10 },
    { x: 77, y: 31, size: 22, rot: 15 },
    { x: 81, y: 62, size: 21, rot: -20 },
    { x: 64, y: 83, size: 24, rot: 10 },
    { x: 36, y: 83, size: 22, rot: -15 },
    { x: 19, y: 62, size: 23, rot: 25 },
    { x: 23, y: 31, size: 21, rot: -8 }
  ],
  // 2 inner, 6 outer
  [
    { x: 38, y: 44, size: 26, rot: -15 },
    { x: 62, y: 56, size: 26, rot: 12 },
    { x: 50, y: 18, size: 22, rot: 8 },
    { x: 79, y: 33, size: 23, rot: -18 },
    { x: 80, y: 72, size: 21, rot: 14 },
    { x: 42, y: 83, size: 24, rot: -10 },
    { x: 18, y: 68, size: 22, rot: 20 },
    { x: 20, y: 28, size: 21, rot: -5 }
  ],
  // 3 inner, 5 outer
  [
    { x: 40, y: 38, size: 25, rot: 10 },
    { x: 62, y: 40, size: 24, rot: -12 },
    { x: 50, y: 65, size: 26, rot: 18 },
    { x: 50, y: 16, size: 22, rot: -8 },
    { x: 82, y: 48, size: 23, rot: 15 },
    { x: 70, y: 81, size: 21, rot: -14 },
    { x: 28, y: 81, size: 22, rot: 10 },
    { x: 18, y: 48, size: 23, rot: -20 }
  ]
];

// --- DOM Elements ---
const el = {
  p1Score: document.getElementById('p1-score'),
  p2Score: document.getElementById('p2-score'),
  p1Name: document.getElementById('p1-name'),
  p2Name: document.getElementById('p2-name'),
  p1Panel: document.getElementById('p1-panel'),
  p2Panel: document.getElementById('p2-panel'),
  btnP1Label: document.getElementById('btn-p1-label'),
  btnP2Label: document.getElementById('btn-p2-label'),
  roundIndicator: document.getElementById('round-indicator'),
  targetDisplay: document.getElementById('target-display'),
  timerBox: document.getElementById('timer-box'),
  timerSeconds: document.getElementById('timer-seconds'),
  cardLeft: document.getElementById('card-left'),
  cardRight: document.getElementById('card-right'),
  revealBanner: document.getElementById('reveal-banner'),
  revealName: document.getElementById('reveal-name'),
  revealImg: document.getElementById('reveal-img'),
  btnWinP1: document.getElementById('btn-win-p1'),
  btnWinP2: document.getElementById('btn-win-p2'),
  btnTabletopWinP2: document.getElementById('btn-tabletop-win-p2'),
  btnTabletopP2Label: document.getElementById('btn-tabletop-p2-label'),
  tabletopP2Dock: document.getElementById('tabletop-p2-dock'),
  btnTabletopToggle: document.getElementById('btn-tabletop-toggle'),
  btnReveal: document.getElementById('btn-reveal'),
  btnHint: document.getElementById('btn-hint'),
  btnNext: document.getElementById('btn-next'),
  btnResetScores: document.getElementById('btn-reset-scores'),
  btnMusic: document.getElementById('btn-music'),
  musicText: document.getElementById('music-text'),
  musicTrackSelect: document.getElementById('music-track-select'),
  btnSfx: document.getElementById('btn-sfx'),
  sfxIcon: document.getElementById('sfx-icon'),
  btnRules: document.getElementById('btn-rules'),
  rulesModal: document.getElementById('rules-modal'),
  btnCloseRules: document.getElementById('btn-close-rules'),
  encyclopediaGrid: document.getElementById('encyclopedia-grid'),
  btnSettings: document.getElementById('btn-settings'),
  settingsModal: document.getElementById('settings-modal'),
  btnCloseSettings: document.getElementById('btn-close-settings'),
  settingTarget: document.getElementById('setting-target'),
  settingTimer: document.getElementById('setting-timer'),
  settingSoundtrack: document.getElementById('setting-soundtrack'),
  settingTabletop: document.getElementById('setting-tabletop'),
  settingAntispam: document.getElementById('setting-antispam'),
  settingAutonext: document.getElementById('setting-autonext'),
  settingVolume: document.getElementById('setting-volume'),
  btnFullscreen: document.getElementById('btn-fullscreen'),
  victoryModal: document.getElementById('victory-modal'),
  victoryTitle: document.getElementById('victory-title'),
  victoryDetail: document.getElementById('victory-detail'),
  btnRematch: document.getElementById('btn-rematch'),
  btnCloseVictory: document.getElementById('btn-close-victory'),
  confettiContainer: document.getElementById('confetti-container'),
  instanceTag: document.getElementById('instance-tag'),
  btnQr: document.getElementById('btn-qr'),
  qrModal: document.getElementById('qr-modal'),
  btnCloseQr: document.getElementById('btn-close-qr'),
  btnCopyLink: document.getElementById('btn-copy-link'),
  btnNewInstance: document.getElementById('btn-new-instance'),
  copyToast: document.getElementById('copy-toast'),
  themeSelect: document.getElementById('theme-select'),
  logoMascot: document.getElementById('logo-mascot'),
  logoTitle: document.getElementById('logo-title'),
  rulesTitle: document.getElementById('rules-title'),
  rulesGoldenText: document.getElementById('rules-golden-text'),
  encyclopediaTitle: document.getElementById('encyclopedia-title'),
  settingSfxCheck: document.getElementById('setting-sfx-check'),
  settingHapticsCheck: document.getElementById('setting-haptics-check'),
  btnOpenRulesSettings: document.getElementById('btn-open-rules-settings'),
  btnOpenPdfModal: document.getElementById('btn-open-pdf-modal'),
  pdfModal: document.getElementById('pdf-modal'),
  btnClosePdf: document.getElementById('btn-close-pdf'),
  gameModeSelect: document.getElementById('game-mode-select'),
  gameContainer: document.getElementById('game-container'),
  survivalHud: document.getElementById('survival-hud'),
  survivalBar: document.getElementById('survival-bar'),
  survivalTimerText: document.getElementById('survival-timer-text'),
  streakBadge: document.getElementById('streak-badge'),
  matchPointBanner: document.getElementById('match-point-banner'),
  iosBadge: document.getElementById('ios-badge')
};

// --- Theme Management ---
function getCurrentTheme() {
  return THEMES[state.currentTheme] || THEMES.animals;
}

function updateThemeUI() {
  const theme = getCurrentTheme();
  if (el.themeSelect) el.themeSelect.value = state.currentTheme;
  if (el.logoMascot) el.logoMascot.src = theme.mascot;
  if (el.logoTitle) el.logoTitle.textContent = theme.title;
  if (el.rulesTitle) el.rulesTitle.textContent = `📖 Game Rules & 57 Symbols (${theme.name})`;
  if (el.rulesGoldenText) {
    el.rulesGoldenText.innerHTML = `Between <strong>any two cards</strong> in the entire 57-card deck, there is <strong>always exactly ONE shared symbol</strong>. Spot it first to score!`;
  }
  if (el.encyclopediaTitle) {
    el.encyclopediaTitle.textContent = `All 57 ${theme.name} (Visual Dictionary)`;
  }
}

// --- Unique Instance Management ---
function generateInstanceId() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = '';
  for (let i = 0; i < 4; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return 'CHIBI-' + code;
}

function initInstance() {
  const hash = window.location.hash.replace('#', '').trim();
  if (hash.startsWith('room=')) {
    state.instanceId = hash.replace('room=', '');
  } else if (!state.instanceId) {
    state.instanceId = generateInstanceId();
    try {
      history.replaceState(null, '', `#room=${state.instanceId}`);
    } catch (_) {}
  }
  if (el.instanceTag) {
    el.instanceTag.textContent = `Room #${state.instanceId}`;
  }
}

function createNewInstance() {
  state.instanceId = generateInstanceId();
  try {
    history.replaceState(null, '', `#room=${state.instanceId}`);
  } catch (_) {}
  if (el.instanceTag) {
    el.instanceTag.textContent = `Room #${state.instanceId}`;
  }
  resetScores();
  if (state.sfxEnabled) {
    soundEngine.playCardDeal();
  }
}

// --- iOS Platform Detection ---
function detectIOSPlatform() {
  const isIOS = window.Capacitor?.isNativePlatform?.() || /iPad|iPhone|iPod/.test(navigator.userAgent);
  if (isIOS) {
    document.body.classList.add('ios-platform');
    if (el.iosBadge) el.iosBadge.classList.remove('hidden');
  }
}

// --- Initialization ---
function init() {
  detectIOSPlatform();
  initInstance();
  updateThemeUI();
  setupEventListeners();
  populateEncyclopedia();
  initSoundtrackUI();
  dealNewRound();
}

// --- Music UI Sync ---
function initSoundtrackUI() {
  if (el.musicTrackSelect) el.musicTrackSelect.value = soundEngine.currentTrack;
  if (el.settingSoundtrack) el.settingSoundtrack.value = soundEngine.currentTrack;
}

// --- Solo Time Attack Timer ---
function startSoloTimer() {
  if (state.soloStartTime > 0) return;
  state.soloStartTime = Date.now();
  el.timerBox.classList.remove('hidden');
  el.timerBox.classList.add('stopwatch');
  
  if (state.soloTimerInterval) clearInterval(state.soloTimerInterval);
  state.soloTimerInterval = setInterval(() => {
    const elapsedMs = Date.now() - state.soloStartTime;
    const totalSec = elapsedMs / 1000;
    const mins = Math.floor(totalSec / 60);
    const secs = (totalSec % 60).toFixed(1);
    el.timerSeconds.textContent = `${mins > 0 ? mins + 'm ' : ''}${secs.padStart(4, '0')}s`;
  }, 100);
}

function stopSoloTimer() {
  if (state.soloTimerInterval) {
    clearInterval(state.soloTimerInterval);
    state.soloTimerInterval = null;
  }
}

// --- Survival Blitz Mode Engine ---
function startSurvivalBlitz() {
  stopSurvivalBlitz();
  state.survivalTime = 8.0;
  state.survivalMaxTime = 10.0;
  state.survivalStreak = 0;
  state.survivalMatches = 0;
  updateSurvivalUI();

  state.survivalInterval = setInterval(() => {
    state.survivalTime = Math.max(0, state.survivalTime - 0.1);
    updateSurvivalUI();

    if (state.survivalTime <= 2.5 && state.survivalTime > 0) {
      if (state.sfxEnabled) soundEngine.playTick();
    }

    if (state.survivalTime <= 0) {
      stopSurvivalBlitz();
      triggerSurvivalGameOver();
    }
  }, 100);
}

function stopSurvivalBlitz() {
  if (state.survivalInterval) {
    clearInterval(state.survivalInterval);
    state.survivalInterval = null;
  }
}

function updateSurvivalUI() {
  if (!el.survivalBar || !el.survivalTimerText || !el.streakBadge) return;
  const pct = Math.max(0, Math.min(100, (state.survivalTime / state.survivalMaxTime) * 100));
  el.survivalBar.style.width = `${pct}%`;
  el.survivalTimerText.textContent = `${state.survivalTime.toFixed(1)}s`;
  el.streakBadge.textContent = `🔥 STREAK: x${state.survivalStreak}`;

  if (state.survivalTime <= 2.5) {
    el.survivalBar.classList.add('critical');
  } else {
    el.survivalBar.classList.remove('critical');
  }
}

function triggerSurvivalGameOver() {
  if (state.sfxEnabled) soundEngine.playBuzzer();
  haptics.warning();

  let rank = 'Bronze Reflexes';
  if (state.survivalMatches >= 25) rank = '⚡ S+ Lightning God';
  else if (state.survivalMatches >= 18) rank = '🏆 S Superhuman';
  else if (state.survivalMatches >= 12) rank = '⭐ A Master Spotter';
  else if (state.survivalMatches >= 6) rank = '🎯 B Sharp Eye';

  el.victoryTitle.textContent = '💥 TIME IS UP!';
  el.victoryDetail.innerHTML = `
    <div style="font-size: 1.8rem; font-weight: 800; color: #DC2626; margin: 8px 0;">${state.survivalMatches} Matches Spotted</div>
    <div style="font-size: 1.1rem; font-weight: 800; color: #1E293B;">Highest Streak: x${state.survivalStreak}</div>
    <div style="font-size: 1.05rem; font-weight: 700; color: #4F46E5; margin-top: 6px;">Rank: ${rank}</div>
  `;
  el.victoryModal.classList.remove('hidden');
}

// --- Deal New Round ---
function dealNewRound() {
  state.isRevealed = false;
  el.revealBanner.classList.add('hidden');

  let c1, c2;
  if (state.gameMode === 'deck') {
    if (state.deckCards.length < 2) {
      state.deckCards = Array.from({length: CARDS.length}, (_, i) => i).sort(() => Math.random() - 0.5);
      state.deckIndex = 0;
    }
    if (state.deckIndex >= state.deckCards.length - 1) {
      triggerDeckCompletion();
      return;
    }
    c1 = state.deckCards[state.deckIndex];
    c2 = state.deckCards[state.deckIndex + 1];
    state.deckIndex++;
    const remaining = state.deckCards.length - state.deckIndex;
    el.targetDisplay.textContent = `Deck: ${remaining} Cards Left`;
    el.roundIndicator.textContent = `CARD ${state.deckIndex} / 56`;
  } else if (state.gameMode === 'solo') {
    const total = CARDS.length;
    c1 = Math.floor(Math.random() * total);
    c2 = Math.floor(Math.random() * total);
    while (c2 === c1) c2 = Math.floor(Math.random() * total);
    el.roundIndicator.textContent = `MATCH ${state.soloMatches + 1} / ${state.soloTarget}`;
    el.targetDisplay.textContent = `Spot 10 Matches as fast as you can!`;
    startSoloTimer();
  } else if (state.gameMode === 'survival') {
    const total = CARDS.length;
    c1 = Math.floor(Math.random() * total);
    c2 = Math.floor(Math.random() * total);
    while (c2 === c1) c2 = Math.floor(Math.random() * total);
    el.roundIndicator.textContent = `MATCH #${state.survivalMatches + 1}`;
    el.targetDisplay.textContent = `Streak Blitz! Beat the clock!`;
  } else if (state.gameMode === 'zen') {
    const total = CARDS.length;
    c1 = Math.floor(Math.random() * total);
    c2 = Math.floor(Math.random() * total);
    while (c2 === c1) c2 = Math.floor(Math.random() * total);
    el.roundIndicator.textContent = `ZEN PLAY`;
    el.targetDisplay.textContent = `Relaxed unlimited card discovery`;
  } else {
    // Normal 2P Versus or Tabletop
    const total = CARDS.length;
    c1 = Math.floor(Math.random() * total);
    c2 = Math.floor(Math.random() * total);
    while (c2 === c1) c2 = Math.floor(Math.random() * total);
    el.roundIndicator.textContent = `ROUND ${state.round}`;
    checkMatchPoint();
  }

  state.currentCard1 = c1;
  state.currentCard2 = c2;
  state.sharedSymbol = getSharedSymbol(c1, c2);

  // Play deal sound & haptic feedback (only after user has interacted to respect autoplay/vibrate policies)
  if (state.hasUserInteracted) {
    if (state.sfxEnabled) {
      soundEngine.playCardDeal();
    }
    haptics.impact('light');
  }

  // Render both cards
  renderCard(el.cardLeft, CARDS[c1], 0);
  renderCard(el.cardRight, CARDS[c2], 1);

  // Card deal animation
  el.cardLeft.classList.remove('deal-anim');
  el.cardRight.classList.remove('deal-anim');
  void el.cardLeft.offsetWidth; // trigger reflow
  el.cardLeft.classList.add('deal-anim');
  el.cardRight.classList.add('deal-anim');

  // Reset round timer if configured in versus
  if (state.gameMode === 'versus' || state.gameMode === 'tabletop') {
    resetRoundTimer();
  }
}

// Render 8 symbols inside circle
function renderCard(cardEl, symbolList, cardSide) {
  cardEl.innerHTML = '';

  const presetIdx = Math.floor(Math.random() * LAYOUT_PRESETS.length);
  const layout = JSON.parse(JSON.stringify(LAYOUT_PRESETS[presetIdx]));

  const globalRot = Math.random() * 360;
  const rad = (globalRot * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);

  layout.forEach(p => {
    const dx = p.x - 50;
    const dy = p.y - 50;
    p.x = 50 + dx * cos - dy * sin;
    p.y = 50 + dx * sin + dy * cos;
    p.rot += (Math.random() * 20 - 10);
  });

  const shuffled = [...symbolList].sort(() => Math.random() - 0.5);
  const theme = getCurrentTheme();

  shuffled.forEach((symIdx, i) => {
    const symbol = theme.symbols[symIdx];
    const pos = layout[i];

    const item = document.createElement('div');
    item.className = 'card-item';
    item.dataset.symbol = symIdx;
    item.dataset.side = cardSide;

    item.style.left = `${pos.x}%`;
    item.style.top = `${pos.y}%`;
    item.style.width = `${pos.size}%`;
    item.style.height = `${pos.size}%`;
    item.style.transform = `translate(-50%, -50%) rotate(${pos.rot}deg)`;

    const img = document.createElement('img');
    img.src = `${theme.folder}/${symbol.slug}.png`;
    img.alt = symbol.name;
    img.loading = 'eager';

    item.appendChild(img);

    // Direct tap handler for touchscreen play
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      handleAnimalTap(symIdx, cardSide);
    });

    cardEl.appendChild(item);
  });
}

// When a user taps a symbol directly on a card
function handleAnimalTap(symIdx, side) {
  if (symIdx === state.sharedSymbol) {
    // Correct match tapped!
    haptics.success();
    revealMatch();

    if (state.gameMode === 'survival') {
      handleSurvivalMatch();
    } else if (state.gameMode === 'solo') {
      scorePoint(1);
    } else if (state.gameMode === 'zen') {
      if (state.sfxEnabled) soundEngine.playStreakChime(1);
      setTimeout(() => dealNewRound(), 800);
    } else {
      scorePoint(side === 0 ? 1 : 2);
    }
  } else {
    // Wrong symbol tapped!
    if (state.gameMode === 'survival') {
      state.survivalStreak = 0;
      updateSurvivalUI();
      if (state.sfxEnabled) soundEngine.playBuzzer();
      haptics.warning();
    } else if (state.gameMode === 'versus' || state.gameMode === 'tabletop') {
      triggerPenalty(side === 0 ? 1 : 2);
    } else {
      haptics.warning();
      if (state.sfxEnabled) soundEngine.playBuzzer();
    }

    const cardEl = side === 0 ? el.cardLeft : el.cardRight;
    cardEl.style.transform = 'translateX(-8px)';
    setTimeout(() => { cardEl.style.transform = 'translateX(8px)'; }, 80);
    setTimeout(() => { cardEl.style.transform = ''; }, 160);
  }
}

// --- Anti-Spam Lockout Penalty ---
function triggerPenalty(player) {
  if (!state.antispamEnabled) return;

  if (player === 1) {
    if (state.p1Locked) return;
    state.p1Locked = true;
    el.btnWinP1.classList.add('penalty-lock');
    el.cardLeft.classList.add('penalty-lock');
    if (state.sfxEnabled) soundEngine.playPenaltySound();
    haptics.warning();
    setTimeout(() => {
      state.p1Locked = false;
      el.btnWinP1.classList.remove('penalty-lock');
      el.cardLeft.classList.remove('penalty-lock');
    }, 1200);
  } else {
    if (state.p2Locked) return;
    state.p2Locked = true;
    el.btnWinP2.classList.add('penalty-lock');
    if (el.btnTabletopWinP2) el.btnTabletopWinP2.classList.add('penalty-lock');
    el.cardRight.classList.add('penalty-lock');
    if (state.sfxEnabled) soundEngine.playPenaltySound();
    haptics.warning();
    setTimeout(() => {
      state.p2Locked = false;
      el.btnWinP2.classList.remove('penalty-lock');
      if (el.btnTabletopWinP2) el.btnTabletopWinP2.classList.remove('penalty-lock');
      el.cardRight.classList.remove('penalty-lock');
    }, 1200);
  }
}

// --- Survival Match Handler ---
function handleSurvivalMatch() {
  state.survivalMatches++;
  state.survivalStreak++;
  state.survivalTime = Math.min(state.survivalMaxTime, state.survivalTime + 2.0);

  if (state.sfxEnabled) {
    soundEngine.playStreakChime(state.survivalStreak);
  }
  haptics.success();

  if (el.streakBadge) {
    el.streakBadge.classList.add('fire');
    setTimeout(() => el.streakBadge.classList.remove('fire'), 300);
  }

  updateSurvivalUI();

  setTimeout(() => {
    dealNewRound();
  }, 600);
}

// --- Reveal Match ---
function revealMatch() {
  if (state.isRevealed) return;
  state.isRevealed = true;

  const theme = getCurrentTheme();
  const matchSymbol = theme.symbols[state.sharedSymbol];
  el.revealName.textContent = matchSymbol.name;
  el.revealImg.src = `${theme.folder}/${matchSymbol.slug}.png`;
  el.revealBanner.classList.remove('hidden');

  // Highlight on both cards
  document.querySelectorAll(`.card-item[data-symbol="${state.sharedSymbol}"]`).forEach(node => {
    node.classList.add('is-match-highlight');
  });

  if (state.sfxEnabled) {
    soundEngine.playRevealSound();
  }
  haptics.impact('light');
}

// --- Hint for Zen / Practice ---
function triggerHint() {
  document.querySelectorAll(`.card-item[data-symbol="${state.sharedSymbol}"]`).forEach(node => {
    node.classList.add('is-hint-pulse');
    setTimeout(() => node.classList.remove('is-hint-pulse'), 1800);
  });
  if (state.sfxEnabled) soundEngine.playRevealSound();
  haptics.impact('light');
}

// --- Scoring ---
function scorePoint(player) {
  if (player === 1 && state.p1Locked) return;
  if (player === 2 && state.p2Locked) return;

  revealMatch();
  haptics.success();

  if (state.gameMode === 'solo') {
    state.soloMatches++;
    el.p1Score.textContent = `${state.soloMatches} / ${state.soloTarget}`;
    bumpScore(el.p1Score);

    if (state.sfxEnabled) {
      soundEngine.playPointP1();
    }

    if (state.soloMatches >= state.soloTarget) {
      stopSoloTimer();
      const elapsed = ((Date.now() - state.soloStartTime) / 1000).toFixed(2);
      triggerSoloVictory(elapsed);
      return;
    }

    if (state.autoNextOnPoint) {
      setTimeout(() => {
        dealNewRound();
      }, 700);
    }
    return;
  }

  // Versus or Tabletop or Deck
  if (player === 1) {
    state.p1Score++;
    el.p1Score.textContent = state.p1Score;
    bumpScore(el.p1Score);
    if (state.sfxEnabled) soundEngine.playPointP1();
  } else {
    state.p2Score++;
    el.p2Score.textContent = state.p2Score;
    bumpScore(el.p2Score);
    if (state.sfxEnabled) soundEngine.playPointP2();
  }

  // Check victory condition
  if ((state.gameMode === 'versus' || state.gameMode === 'tabletop') && state.targetScore > 0) {
    if (state.p1Score >= state.targetScore) {
      triggerVictory(1);
      return;
    } else if (state.p2Score >= state.targetScore) {
      triggerVictory(2);
      return;
    }
    checkMatchPoint();
  }

  // Auto-next round if enabled
  if (state.autoNextOnPoint) {
    setTimeout(() => {
      state.round++;
      dealNewRound();
    }, 1100);
  }
}

function checkMatchPoint() {
  if (!el.matchPointBanner) return;
  if (state.targetScore <= 0 || (state.gameMode !== 'versus' && state.gameMode !== 'tabletop')) {
    el.matchPointBanner.classList.add('hidden');
    return;
  }
  const isP1MatchPoint = state.p1Score === state.targetScore - 1;
  const isP2MatchPoint = state.p2Score === state.targetScore - 1;

  if (isP1MatchPoint && isP2MatchPoint) {
    el.matchPointBanner.classList.remove('hidden');
    el.matchPointBanner.textContent = '🔥 DEUCE! NEXT POINT WINS! 🔥';
  } else if (isP1MatchPoint) {
    el.matchPointBanner.classList.remove('hidden');
    el.matchPointBanner.textContent = `⚡ MATCH POINT FOR ${state.p1Name.toUpperCase()}! ⚡`;
  } else if (isP2MatchPoint) {
    el.matchPointBanner.classList.remove('hidden');
    el.matchPointBanner.textContent = `⚡ MATCH POINT FOR ${state.p2Name.toUpperCase()}! ⚡`;
  } else {
    el.matchPointBanner.classList.add('hidden');
  }
}

function bumpScore(element) {
  element.classList.remove('bump');
  void element.offsetWidth;
  element.classList.add('bump');
  setTimeout(() => element.classList.remove('bump'), 250);
}

// --- Tabletop Mode Toggle ---
function setTabletop(active) {
  state.tabletopActive = active;
  document.body.classList.toggle('tabletop-active', active);
  if (el.gameContainer) el.gameContainer.classList.toggle('tabletop-active', active);
  if (el.tabletopP2Dock) el.tabletopP2Dock.classList.toggle('hidden', !active);
  if (el.settingTabletop) el.settingTabletop.checked = active;
  if (el.btnTabletopToggle) el.btnTabletopToggle.classList.toggle('active', active);

  if (active && state.gameMode !== 'tabletop' && state.gameMode !== 'versus') {
    setGameMode('tabletop');
  }
}

// --- Set Game Mode ---
function setGameMode(mode) {
  state.gameMode = mode;
  if (el.gameModeSelect) el.gameModeSelect.value = mode;

  stopSoloTimer();
  stopSurvivalBlitz();
  if (el.victoryModal) el.victoryModal.classList.add('hidden');
  if (el.survivalHud) el.survivalHud.classList.add('hidden');
  if (el.btnHint) el.btnHint.classList.add('hidden');
  if (el.matchPointBanner) el.matchPointBanner.classList.add('hidden');

  if (mode === 'tabletop') {
    setTabletop(true);
  } else {
    setTabletop(false);
  }

  if (mode === 'survival') {
    el.gameContainer.classList.add('solo-mode');
    el.p1Name.value = 'Survival';
    el.btnP1Label.textContent = '⚡ Found Match!';
    el.p2Name.value = 'Streak';
    el.p2Score.textContent = 'x0';
    el.targetDisplay.textContent = 'Speed Blitz Survival!';
    if (el.survivalHud) el.survivalHud.classList.remove('hidden');
    startSurvivalBlitz();
  } else if (mode === 'zen') {
    el.gameContainer.classList.add('solo-mode');
    el.p1Name.value = 'Zen Explorer';
    el.btnP1Label.textContent = 'Found Match!';
    el.p2Name.value = 'Practice';
    el.p2Score.textContent = '∞';
    el.targetDisplay.textContent = 'Unlimited discovery (no timer)';
    if (el.btnHint) el.btnHint.classList.remove('hidden');
  } else if (mode === 'solo') {
    el.gameContainer.classList.add('solo-mode');
    state.soloMatches = 0;
    state.soloStartTime = 0;
    el.p1Name.value = 'Matches';
    el.p1Score.textContent = `0 / ${state.soloTarget}`;
    el.btnP1Label.textContent = '⚡ Found Match!';
    const best = localStorage.getItem(`chibi_solo_best_${state.currentTheme}`);
    el.p2Name.value = 'Record';
    el.p2Score.textContent = best ? `${best}s` : '--';
    el.targetDisplay.textContent = `Spot 10 Matches!`;
    el.timerBox.classList.remove('hidden');
    el.timerBox.classList.add('stopwatch');
    el.timerSeconds.textContent = '00:00.0';
  } else if (mode === 'deck') {
    el.gameContainer.classList.remove('solo-mode');
    el.p1Name.value = state.p1Name || 'Player 1';
    el.p2Name.value = state.p2Name || 'Player 2';
    el.btnP1Label.textContent = el.p1Name.value;
    el.btnP2Label.textContent = el.p2Name.value;
    el.timerBox.classList.add('hidden');
    el.timerBox.classList.remove('stopwatch');
    state.deckCards = Array.from({length: CARDS.length}, (_, i) => i).sort(() => Math.random() - 0.5);
    state.deckIndex = 0;
    el.targetDisplay.textContent = 'Deck: 57 Cards';
  } else {
    // Versus
    el.gameContainer.classList.remove('solo-mode');
    el.p1Name.value = state.p1Name || 'Player 1';
    el.p2Name.value = state.p2Name || 'Player 2';
    el.btnP1Label.textContent = el.p1Name.value;
    el.btnP2Label.textContent = el.p2Name.value;
    el.timerBox.classList.add('hidden');
    el.timerBox.classList.remove('stopwatch');
    el.targetDisplay.textContent = state.targetScore > 0 ? `First to ${state.targetScore} Wins` : 'Free Play';
  }

  dealNewRound();
}

// --- Victory Celebrations ---
function triggerVictory(winner) {
  const winnerName = winner === 1 ? state.p1Name : state.p2Name;
  el.victoryTitle.textContent = `🎉 ${winnerName.toUpperCase()} WINS!`;
  el.victoryDetail.textContent = `Final Score: ${state.p1Score} - ${state.p2Score} in ${state.round} Rounds`;
  el.victoryModal.classList.remove('hidden');

  if (state.sfxEnabled) {
    soundEngine.playVictoryFanfare();
  }
  haptics.success();
  fireConfetti();
}

function triggerSoloVictory(elapsed) {
  const key = `chibi_solo_best_${state.currentTheme}`;
  const prevBestStr = localStorage.getItem(key);
  const prevBest = prevBestStr ? parseFloat(prevBestStr) : 9999;
  const currentNum = parseFloat(elapsed);
  const isNewRecord = currentNum < prevBest;

  if (isNewRecord) {
    localStorage.setItem(key, elapsed);
    el.p2Score.textContent = `${elapsed}s`;
  }

  let rank = '🎯 Sharp Eye';
  let rankDesc = 'Solid spotting reflexes!';
  if (currentNum < 15) {
    rank = '⚡ Lightning Master (Rank S+)';
    rankDesc = 'Unbelievable reaction speed!';
  } else if (currentNum < 25) {
    rank = '🚀 Expert Spotter (Rank A)';
    rankDesc = 'Fast & accurate reflexes!';
  } else if (currentNum < 35) {
    rank = '⭐ Quick Spotter (Rank B)';
    rankDesc = 'Great visual acuity!';
  }

  el.victoryTitle.textContent = isNewRecord ? '🏆 NEW RECORD!' : '🎉 CHALLENGE COMPLETE!';
  el.victoryDetail.innerHTML = `
    <div style="font-size: 1.8rem; font-weight: 800; color: #4F46E5; margin: 8px 0;">${elapsed}s</div>
    <div style="font-size: 1.05rem; font-weight: 700; color: #1E293B;">${rank}</div>
    <p style="color: #64748B; font-size: 0.85rem; margin-top: 4px;">${rankDesc} (${state.soloTarget} matches found)</p>
  `;
  el.victoryModal.classList.remove('hidden');

  if (state.sfxEnabled) {
    soundEngine.playVictoryFanfare();
  }
  haptics.success();
  fireConfetti();
}

function triggerDeckCompletion() {
  el.victoryTitle.textContent = '🃏 FULL DECK CLEARED!';
  el.victoryDetail.textContent = `All 57 cards explored with zero repetitions!`;
  el.victoryModal.classList.remove('hidden');
  if (state.sfxEnabled) soundEngine.playVictoryFanfare();
  haptics.success();
  fireConfetti();
}

function resetScores() {
  state.p1Score = 0;
  state.p2Score = 0;
  state.round = 1;
  el.p1Score.textContent = '0';
  el.p2Score.textContent = '0';
  dealNewRound();
}

// --- Round Countdown Timer (Versus) ---
function resetRoundTimer() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
  }

  if (state.timerSeconds > 0) {
    el.timerBox.classList.remove('hidden');
    state.timerCurrent = state.timerSeconds;
    el.timerSeconds.textContent = state.timerCurrent;

    state.timerInterval = setInterval(() => {
      state.timerCurrent--;
      el.timerSeconds.textContent = state.timerCurrent;

      if (state.timerCurrent <= 3 && state.timerCurrent > 0) {
        if (state.sfxEnabled) soundEngine.synthHat(soundEngine.ctx.currentTime, 0.4);
      }

      if (state.timerCurrent <= 0) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
        if (state.sfxEnabled) soundEngine.playBuzzer();
        revealMatch();
      }
    }, 1000);
  } else {
    el.timerBox.classList.add('hidden');
  }
}

// --- Confetti Explosion ---
function fireConfetti() {
  const colors = ['#FF5A79', '#3B82F6', '#F59E0B', '#10B981', '#8B5CF6', '#EC4899'];
  const count = 75;

  for (let i = 0; i < count; i++) {
    const piece = document.createElement('div');
    piece.style.position = 'fixed';
    piece.style.top = '40%';
    piece.style.left = '50%';
    piece.style.width = `${Math.random() * 10 + 6}px`;
    piece.style.height = `${Math.random() * 12 + 6}px`;
    piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    piece.style.zIndex = '1001';
    piece.style.pointerEvents = 'none';

    const angle = Math.random() * Math.PI * 2;
    const velocity = Math.random() * 450 + 200;
    const vx = Math.cos(angle) * velocity;
    const vy = Math.sin(angle) * velocity - 200;

    el.confettiContainer.appendChild(piece);

    let x = 0, y = 0;
    const start = performance.now();

    function stepAnim(t) {
      const dt = (t - start) / 1000;
      if (dt > 1.8) {
        piece.remove();
        return;
      }
      x = vx * dt;
      y = vy * dt + 0.5 * 980 * dt * dt;
      piece.style.transform = `translate(${x}px, ${y}px) rotate(${dt * 600}deg)`;
      piece.style.opacity = `${Math.max(0, 1 - dt / 1.8)}`;
      requestAnimationFrame(stepAnim);
    }
    requestAnimationFrame(stepAnim);
  }
}

// --- Encyclopedia Population ---
function populateEncyclopedia() {
  const theme = getCurrentTheme();
  el.encyclopediaGrid.innerHTML = '';
  theme.symbols.forEach((a, i) => {
    const card = document.createElement('div');
    card.className = 'encyclopedia-item';
    card.innerHTML = `
      <img src="${theme.folder}/${a.slug}.png" alt="${a.name}" loading="lazy">
      <span>#${i + 1} ${a.name}</span>
    `;
    el.encyclopediaGrid.appendChild(card);
  });
}

// --- Event Listeners & Shortcuts ---
function setupEventListeners() {
  // Theme Switcher
  if (el.themeSelect) {
    el.themeSelect.value = state.currentTheme;
    el.themeSelect.addEventListener('change', (e) => {
      soundEngine.ensureContext();
      state.currentTheme = e.target.value;
      try {
        localStorage.setItem('chibi_theme', state.currentTheme);
      } catch (_) {}
      updateThemeUI();
      populateEncyclopedia();
      renderCard(el.cardLeft, CARDS[state.currentCard1], 0);
      renderCard(el.cardRight, CARDS[state.currentCard2], 1);
      if (state.isRevealed) {
        const theme = getCurrentTheme();
        const matchSym = theme.symbols[state.sharedSymbol];
        el.revealName.textContent = matchSym.name;
        el.revealImg.src = `${theme.folder}/${matchSym.slug}.png`;
      }
      if (state.sfxEnabled) {
        soundEngine.playCardDeal();
      }
    });
  }

  // Soundtrack Switcher
  function handleSoundtrackChange(val) {
    soundEngine.setTrack(val);
    if (el.musicTrackSelect) el.musicTrackSelect.value = val;
    if (el.settingSoundtrack) el.settingSoundtrack.value = val;
    if (soundEngine.isPlayingMusic) {
      soundEngine.stopMusic();
      soundEngine.startMusic();
    }
  }

  if (el.musicTrackSelect) {
    el.musicTrackSelect.addEventListener('change', (e) => handleSoundtrackChange(e.target.value));
  }
  if (el.settingSoundtrack) {
    el.settingSoundtrack.addEventListener('change', (e) => handleSoundtrackChange(e.target.value));
  }

  // Tabletop Mode Quick Toggle
  if (el.btnTabletopToggle) {
    el.btnTabletopToggle.addEventListener('click', () => {
      soundEngine.ensureContext();
      haptics.impact('light');
      setTabletop(!state.tabletopActive);
    });
  }

  if (el.settingTabletop) {
    el.settingTabletop.addEventListener('change', (e) => {
      setTabletop(e.target.checked);
    });
  }

  // Anti-Spam Lockout Setting
  if (el.settingAntispam) {
    el.settingAntispam.addEventListener('change', (e) => {
      state.antispamEnabled = e.target.checked;
    });
  }

  // Hint Button (Zen / Practice)
  if (el.btnHint) {
    el.btnHint.addEventListener('click', () => {
      soundEngine.ensureContext();
      triggerHint();
    });
  }

  // Manual Winner Buttons
  el.btnWinP1.addEventListener('click', () => {
    soundEngine.ensureContext();
    scorePoint(1);
  });

  el.btnWinP2.addEventListener('click', () => {
    soundEngine.ensureContext();
    scorePoint(2);
  });

  if (el.btnTabletopWinP2) {
    el.btnTabletopWinP2.addEventListener('click', () => {
      soundEngine.ensureContext();
      scorePoint(2);
    });
  }

  el.btnReveal.addEventListener('click', () => {
    soundEngine.ensureContext();
    revealMatch();
  });

  el.btnNext.addEventListener('click', () => {
    soundEngine.ensureContext();
    state.round++;
    dealNewRound();
  });

  el.btnResetScores.addEventListener('click', () => {
    soundEngine.ensureContext();
    resetScores();
  });

  // Name Editing
  el.p1Name.addEventListener('change', (e) => {
    state.p1Name = e.target.value || 'Player 1';
    el.btnP1Label.textContent = state.p1Name;
    checkMatchPoint();
  });

  el.p2Name.addEventListener('change', (e) => {
    state.p2Name = e.target.value || 'Player 2';
    el.btnP2Label.textContent = state.p2Name;
    if (el.btnTabletopP2Label) el.btnTabletopP2Label.textContent = state.p2Name;
    checkMatchPoint();
  });

  // Music Toggle
  el.btnMusic.addEventListener('click', () => {
    const isPlaying = soundEngine.toggleMusic();
    el.musicText.textContent = isPlaying ? 'Music: ON' : 'Music: OFF';
    el.btnMusic.classList.toggle('active', isPlaying);
  });

  // SFX Toggle
  el.btnSfx.addEventListener('click', () => {
    state.sfxEnabled = !state.sfxEnabled;
    el.sfxIcon.textContent = state.sfxEnabled ? '🔊' : '🔇';
    el.btnSfx.classList.toggle('off', !state.sfxEnabled);
    if (el.settingSfxCheck) el.settingSfxCheck.checked = state.sfxEnabled;
  });

  if (el.settingSfxCheck) {
    el.settingSfxCheck.addEventListener('change', (e) => {
      state.sfxEnabled = e.target.checked;
      el.sfxIcon.textContent = state.sfxEnabled ? '🔊' : '🔇';
      el.btnSfx.classList.toggle('off', !state.sfxEnabled);
    });
  }

  // Modals
  el.btnRules.addEventListener('click', () => {
    soundEngine.ensureContext();
    el.rulesModal.classList.remove('hidden');
  });

  el.btnCloseRules.addEventListener('click', () => {
    el.rulesModal.classList.add('hidden');
  });

  el.btnSettings.addEventListener('click', () => {
    soundEngine.ensureContext();
    el.settingsModal.classList.remove('hidden');
  });

  el.btnCloseSettings.addEventListener('click', () => {
    el.settingsModal.classList.add('hidden');
  });

  if (el.btnOpenRulesSettings) {
    el.btnOpenRulesSettings.addEventListener('click', () => {
      el.settingsModal.classList.add('hidden');
      el.rulesModal.classList.remove('hidden');
    });
  }

  // QR Code Modal
  if (el.btnQr && el.qrModal) {
    el.btnQr.addEventListener('click', () => {
      soundEngine.ensureContext();
      el.qrModal.classList.remove('hidden');
    });
  }

  if (el.btnCloseQr && el.qrModal) {
    el.btnCloseQr.addEventListener('click', () => {
      el.qrModal.classList.add('hidden');
    });
  }

  if (el.btnCopyLink) {
    el.btnCopyLink.addEventListener('click', () => {
      const shareUrl = window.location.origin + window.location.pathname + `#room=${state.instanceId}`;
      if (navigator.clipboard?.writeText) {
        navigator.clipboard.writeText(shareUrl).then(() => {
          showCopyToast('✓ Game Link Copied to Clipboard!');
        }).catch(() => {
          prompt('Copy this link:', shareUrl);
        });
      } else {
        prompt('Copy this link:', shareUrl);
      }
    });
  }

  if (el.btnNewInstance) {
    el.btnNewInstance.addEventListener('click', () => {
      soundEngine.ensureContext();
      createNewInstance();
      showCopyToast(`✓ Started new instance #${state.instanceId}!`);
    });
  }

  function showCopyToast(msg) {
    if (!el.copyToast) return;
    el.copyToast.textContent = msg;
    el.copyToast.classList.remove('hidden');
    setTimeout(() => {
      el.copyToast.classList.add('hidden');
    }, 2500);
  }

  el.btnRematch.addEventListener('click', () => {
    el.victoryModal.classList.add('hidden');
    resetScores();
    if (state.gameMode === 'survival') startSurvivalBlitz();
  });

  if (el.btnCloseVictory) {
    el.btnCloseVictory.addEventListener('click', () => {
      el.victoryModal.classList.add('hidden');
    });
  }

  // Game Mode Selector
  if (el.gameModeSelect) {
    el.gameModeSelect.addEventListener('change', (e) => {
      soundEngine.ensureContext();
      haptics.impact('light');
      setGameMode(e.target.value);
    });
  }

  // Haptics Toggle
  if (el.settingHapticsCheck) {
    el.settingHapticsCheck.checked = state.hapticsEnabled;
    el.settingHapticsCheck.addEventListener('change', (e) => {
      state.hapticsEnabled = e.target.checked;
      try {
        localStorage.setItem('chibi_haptics', state.hapticsEnabled ? 'true' : 'false');
      } catch (_) {}
      if (state.hapticsEnabled) haptics.impact('light');
    });
  }

  // PDF Modal
  if (el.btnOpenPdfModal && el.pdfModal) {
    el.btnOpenPdfModal.addEventListener('click', () => {
      soundEngine.ensureContext();
      el.settingsModal.classList.add('hidden');
      el.pdfModal.classList.remove('hidden');
    });
  }

  if (el.btnClosePdf && el.pdfModal) {
    el.btnClosePdf.addEventListener('click', () => {
      el.pdfModal.classList.add('hidden');
    });
  }

  // Close modals on background click
  [el.rulesModal, el.settingsModal, el.victoryModal, el.qrModal, el.pdfModal].forEach(modal => {
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
      });
    }
  });

  // Settings inputs
  if (el.settingTarget) {
    el.settingTarget.addEventListener('change', (e) => {
      state.targetScore = parseInt(e.target.value, 10);
      el.targetDisplay.textContent = state.targetScore > 0 ? `First to ${state.targetScore} Wins` : 'Free Play (Unlimited)';
      checkMatchPoint();
    });
  }

  if (el.settingTimer) {
    el.settingTimer.addEventListener('change', (e) => {
      state.timerSeconds = parseInt(e.target.value, 10);
      resetRoundTimer();
    });
  }

  if (el.settingAutonext) {
    el.settingAutonext.addEventListener('change', (e) => {
      state.autoNextOnPoint = e.target.checked;
    });
  }

  if (el.settingVolume) {
    el.settingVolume.addEventListener('input', (e) => {
      soundEngine.setVolume(parseFloat(e.target.value));
    });
  }

  // Fullscreen
  if (el.btnFullscreen) {
    el.btnFullscreen.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  // Keyboard Shortcuts for Party Play
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    soundEngine.ensureContext();

    switch (e.key.toLowerCase()) {
      case 'a':
      case 'arrowleft':
      case '1':
        scorePoint(1);
        break;
      case 'l':
      case 'arrowright':
      case '2':
        scorePoint(2);
        break;
      case ' ':
        e.preventDefault();
        state.round++;
        dealNewRound();
        break;
      case 'r':
        revealMatch();
        break;
      case 'm':
        el.btnMusic.click();
        break;
      case 'h':
        triggerHint();
        break;
    }
  });

  const markInteracted = () => {
    state.hasUserInteracted = true;
    soundEngine.ensureContext();
  };
  window.addEventListener('pointerdown', markInteracted, { once: true, passive: true });
  window.addEventListener('keydown', markInteracted, { once: true, passive: true });

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js').catch(() => {});
    });
  }
}

// Start
document.addEventListener('DOMContentLoaded', init);
