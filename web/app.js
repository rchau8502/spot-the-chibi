import { THEMES, ANIMALS, CARDS, getSharedSymbol } from './cards.js';
import { soundEngine } from './audio.js';

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
  autoNextOnPoint: true,
  timerSeconds: 0,
  timerCurrent: 0,
  timerInterval: null,
  instanceId: '',
  currentTheme: localStorage.getItem('chibi_theme') || 'animals'
};

// Layout templates for 8 symbols inside circle (normalized 0-100%)
// Hand-crafted non-overlapping positions with varied sizes
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
  btnReveal: document.getElementById('btn-reveal'),
  btnNext: document.getElementById('btn-next'),
  btnResetScores: document.getElementById('btn-reset-scores'),
  btnMusic: document.getElementById('btn-music'),
  musicText: document.getElementById('music-text'),
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
  encyclopediaTitle: document.getElementById('encyclopedia-title')
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
    soundEngine.playScoreBeep();
  }
}

// --- Initialization ---
function init() {
  initInstance();
  updateThemeUI();
  setupEventListeners();
  populateEncyclopedia();
  dealNewRound();
}

// --- Deal New Round ---
function dealNewRound() {
  state.isRevealed = false;
  el.revealBanner.classList.add('hidden');

  // Pick 2 distinct cards from 0..56
  const total = CARDS.length;
  let c1 = Math.floor(Math.random() * total);
  let c2 = Math.floor(Math.random() * total);
  while (c2 === c1) {
    c2 = Math.floor(Math.random() * total);
  }

  state.currentCard1 = c1;
  state.currentCard2 = c2;
  state.sharedSymbol = getSharedSymbol(c1, c2);

  // Play deal sound
  if (state.sfxEnabled) {
    soundEngine.playCardDeal();
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

  // Update round indicator
  el.roundIndicator.textContent = `ROUND ${state.round}`;

  // Reset & start round timer if enabled
  resetRoundTimer();
}

// Render 8 animals inside a card
function renderCard(cardEl, symbolList, cardSide) {
  cardEl.innerHTML = '';

  // Select a layout preset and randomize slightly
  const presetIdx = Math.floor(Math.random() * LAYOUT_PRESETS.length);
  const layout = JSON.parse(JSON.stringify(LAYOUT_PRESETS[presetIdx]));

  // Random rotation offset for entire card to add organic variety
  const globalRot = Math.random() * 360;
  const rad = (globalRot * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);

  // Rotate layout around center (50, 50)
  layout.forEach(p => {
    const dx = p.x - 50;
    const dy = p.y - 50;
    p.x = 50 + dx * cos - dy * sin;
    p.y = 50 + dx * sin + dy * cos;
    p.rot += (Math.random() * 20 - 10);
  });

  // Shuffle symbols mapping to layout slots
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

    // Direct tap handler (for interactive touch screen play!)
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      handleAnimalTap(symIdx, cardSide);
    });

    cardEl.appendChild(item);
  });
}

// When a user taps an animal directly on a card
function handleAnimalTap(symIdx, side) {
  if (symIdx === state.sharedSymbol) {
    // Correct match tapped!
    revealMatch();
    if (side === 0) {
      scorePoint(1);
    } else {
      scorePoint(2);
    }
  } else {
    // Wrong animal clicked
    if (state.sfxEnabled) soundEngine.playBuzzer();
    const cardEl = side === 0 ? el.cardLeft : el.cardRight;
    cardEl.style.transform = 'translateX(-8px)';
    setTimeout(() => { cardEl.style.transform = 'translateX(8px)'; }, 80);
    setTimeout(() => { cardEl.style.transform = ''; }, 160);
  }
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
}

// --- Scoring ---
function scorePoint(player) {
  revealMatch();

  if (player === 1) {
    state.p1Score++;
    el.p1Score.textContent = state.p1Score;
    bumpScore(el.p1Score);
  } else {
    state.p2Score++;
    el.p2Score.textContent = state.p2Score;
    bumpScore(el.p2Score);
  }

  if (state.sfxEnabled) {
    soundEngine.playScorePoint();
  }

  // Check victory condition
  if (state.targetScore > 0) {
    if (state.p1Score >= state.targetScore) {
      triggerVictory(1);
      return;
    } else if (state.p2Score >= state.targetScore) {
      triggerVictory(2);
      return;
    }
  }

  // Auto-next round if enabled
  if (state.autoNextOnPoint) {
    setTimeout(() => {
      state.round++;
      dealNewRound();
    }, 1100);
  }
}

function bumpScore(element) {
  element.classList.remove('bump');
  void element.offsetWidth;
  element.classList.add('bump');
  setTimeout(() => element.classList.remove('bump'), 250);
}

// --- Victory ---
function triggerVictory(winner) {
  const winnerName = winner === 1 ? state.p1Name : state.p2Name;
  el.victoryTitle.textContent = `🎉 ${winnerName.toUpperCase()} WINS!`;
  el.victoryDetail.textContent = `Final Score: ${state.p1Score} - ${state.p2Score} in ${state.round} Rounds`;
  el.victoryModal.classList.remove('hidden');

  if (state.sfxEnabled) {
    soundEngine.playVictoryFanfare();
  }

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

// --- Timer System ---
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

    let x = 0, y = 0, grav = 0;
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
      // Re-render current round cards with new theme symbols
      renderCard(el.cardLeft, CARDS[state.currentCard1], 0);
      renderCard(el.cardRight, CARDS[state.currentCard2], 1);
      if (state.isRevealed) {
        const theme = getCurrentTheme();
        const matchSym = theme.symbols[state.sharedSymbol];
        el.revealName.textContent = matchSym.name;
        el.revealImg.src = `${theme.folder}/${matchSym.slug}.png`;
      }
      if (state.sfxEnabled) {
        soundEngine.playScoreBeep();
      }
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
    if (confirm('Reset scores to 0?')) {
      resetScores();
    }
  });

  // Music Toggle
  el.btnMusic.addEventListener('click', () => {
    soundEngine.ensureContext();
    const isPlaying = soundEngine.toggleMusic();
    if (isPlaying) {
      el.btnMusic.classList.add('playing');
      el.musicText.textContent = 'Music: ON';
    } else {
      el.btnMusic.classList.remove('playing');
      el.musicText.textContent = 'Music: OFF';
    }
  });

  // SFX Toggle
  el.btnSfx.addEventListener('click', () => {
    state.sfxEnabled = !state.sfxEnabled;
    el.sfxIcon.textContent = state.sfxEnabled ? '🔊' : '🔇';
  });

  // Player Name Inputs
  el.p1Name.addEventListener('input', (e) => {
    state.p1Name = e.target.value.trim() || 'Player 1';
    el.btnP1Label.textContent = state.p1Name;
  });

  el.p2Name.addEventListener('input', (e) => {
    state.p2Name = e.target.value.trim() || 'Player 2';
    el.btnP2Label.textContent = state.p2Name;
  });

  // Modals
  el.btnRules.addEventListener('click', () => el.rulesModal.classList.remove('hidden'));
  el.btnCloseRules.addEventListener('click', () => el.rulesModal.classList.add('hidden'));

  el.btnSettings.addEventListener('click', () => el.settingsModal.classList.remove('hidden'));
  el.btnCloseSettings.addEventListener('click', () => el.settingsModal.classList.add('hidden'));

  // QR Modal
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
      soundEngine.ensureContext();
      const shareUrl = 'https://spotthechibi.vercel.app' + (state.instanceId ? `#room=${state.instanceId}` : '');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(shareUrl).then(() => {
          showCopyToast('✓ Game Link copied to clipboard!');
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
  });

  el.btnCloseVictory.addEventListener('click', () => {
    el.victoryModal.classList.add('hidden');
  });

  // Close modals on background click
  [el.rulesModal, el.settingsModal, el.victoryModal, el.qrModal].forEach(modal => {
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
      });
    }
  });

  // Settings inputs
  el.settingTarget.addEventListener('change', (e) => {
    state.targetScore = parseInt(e.target.value, 10);
    el.targetDisplay.textContent = state.targetScore > 0 ? `First to ${state.targetScore} Wins` : 'Free Play (Unlimited)';
  });

  el.settingTimer.addEventListener('change', (e) => {
    state.timerSeconds = parseInt(e.target.value, 10);
    resetRoundTimer();
  });

  el.settingAutonext.addEventListener('change', (e) => {
    state.autoNextOnPoint = e.target.checked;
  });

  el.settingVolume.addEventListener('input', (e) => {
    soundEngine.setVolume(parseFloat(e.target.value));
  });

  // Fullscreen
  el.btnFullscreen.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });

  // Keyboard Shortcuts for Party Play!
  window.addEventListener('keydown', (e) => {
    // Ignore keystrokes when typing into name input
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
    }
  });

  // Resume Web Audio Context on very first click anywhere on screen
  window.addEventListener('click', () => {
    soundEngine.ensureContext();
  }, { once: true });
}

// Start
document.addEventListener('DOMContentLoaded', init);
