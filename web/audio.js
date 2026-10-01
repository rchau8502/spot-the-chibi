// Web Audio API Synthesizer Engine
// 100% Royalty-Free, Zero-Copyright procedural synthesized music & SFX
// Features 4 selectable soundtrack styles: Party Beat, 8-Bit Arcade, Lo-Fi Chill, and PvP Showdown

export const MUSIC_TRACKS = [
  { id: 'party', name: '🎉 Party Beat', bpm: 126 },
  { id: 'arcade', name: '👾 8-Bit Arcade', bpm: 142 },
  { id: 'lofi', name: '☕ Lo-Fi Chill', bpm: 86 },
  { id: 'battle', name: '⚔️ PvP Showdown', bpm: 144 }
];

class GameSoundEngine {
  constructor() {
    this.ctx = null;
    this.musicGain = null;
    this.sfxGain = null;
    this.masterGain = null;

    this.isPlayingMusic = false;
    this.currentTrack = localStorage.getItem('chibi_music_track') || 'party';
    this.currentTempo = 126;
    this.step = 0;
    this.timerId = null;

    this.musicVolume = 0.40;
    this.sfxVolume = 0.65;
  }

  init() {
    if (this.ctx) return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContextClass();

    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.setValueAtTime(1.0, this.ctx.currentTime);
    this.masterGain.connect(this.ctx.destination);

    this.musicGain = this.ctx.createGain();
    this.musicGain.gain.setValueAtTime(this.musicVolume, this.ctx.currentTime);
    this.musicGain.connect(this.masterGain);

    this.sfxGain = this.ctx.createGain();
    this.sfxGain.gain.setValueAtTime(this.sfxVolume, this.ctx.currentTime);
    this.sfxGain.connect(this.masterGain);

    this.updateTrackTempo();
  }

  ensureContext() {
    this.init();
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  updateTrackTempo() {
    const track = MUSIC_TRACKS.find(t => t.id === this.currentTrack) || MUSIC_TRACKS[0];
    this.currentTempo = track.bpm;
  }

  setTrack(trackId) {
    if (this.currentTrack === trackId) return;
    this.currentTrack = trackId;
    localStorage.setItem('chibi_music_track', trackId);
    this.updateTrackTempo();
    this.step = 0;
  }

  nextTrack() {
    const idx = MUSIC_TRACKS.findIndex(t => t.id === this.currentTrack);
    const nextIdx = (idx + 1) % MUSIC_TRACKS.length;
    this.setTrack(MUSIC_TRACKS[nextIdx].id);
    return MUSIC_TRACKS[nextIdx];
  }

  startMusic() {
    this.ensureContext();
    if (this.isPlayingMusic) return;
    this.isPlayingMusic = true;
    this.step = 0;
    this.scheduleNextBeat();
  }

  stopMusic() {
    this.isPlayingMusic = false;
    if (this.timerId) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
  }

  toggleMusic() {
    if (this.isPlayingMusic) {
      this.stopMusic();
      return false;
    } else {
      this.startMusic();
      return true;
    }
  }

  scheduleNextBeat() {
    if (!this.isPlayingMusic || !this.ctx) return;

    const secondsPer16th = 60.0 / (this.currentTempo * 4);
    const now = this.ctx.currentTime;

    if (this.currentTrack === 'arcade') {
      this.playArcadeStep(this.step, now);
    } else if (this.currentTrack === 'lofi') {
      this.playLofiStep(this.step, now);
    } else if (this.currentTrack === 'battle') {
      this.playBattleStep(this.step, now);
    } else {
      this.playPartyStep(this.step, now);
    }

    this.step = (this.step + 1) % 32;

    this.timerId = setTimeout(() => {
      this.scheduleNextBeat();
    }, secondsPer16th * 1000);
  }

  // --- Track 1: Party Beat (Bouncy Kahoot-style) ---
  playPartyStep(step, time) {
    const beatInBar = step % 16;
    const isQuarter = beatInBar % 4 === 0;
    const isBackbeat = beatInBar === 4 || beatInBar === 12;

    if (isQuarter) this.synthKick(time);
    if (isBackbeat) this.synthSnare(time);
    const hatVol = isQuarter ? 0.35 : (beatInBar % 2 === 0 ? 0.22 : 0.12);
    this.synthHat(time, hatVol);

    const bassLine = [
      73.4,  0, 73.4,  0,  0, 87.3, 98.0,  0,  73.4,  0, 110.0, 0,  0, 130.8, 98.0, 0,
      73.4,  0, 73.4,  0, 87.3,  0, 98.0,  0, 110.0, 0, 130.8, 0, 146.8, 0, 110.0, 98.0
    ];
    if (bassLine[step] > 0) this.synthBass(time, bassLine[step]);

    const arpNotes = [
      293.6, 0, 349.2, 0, 392.0, 440.0, 0, 523.2, 587.3, 523.2, 440.0, 392.0, 349.2, 0, 392.0, 0,
      293.6, 0, 440.0, 0, 523.2, 0, 587.3, 0, 698.4, 587.3, 523.2, 440.0, 392.0, 349.2, 293.6, 0
    ];
    if (arpNotes[step] > 0) this.synthLeadPluck(time, arpNotes[step]);
  }

  // --- Track 2: 8-Bit Arcade (Chiptune rush) ---
  playArcadeStep(step, time) {
    const beatInBar = step % 16;
    if (beatInBar === 0 || beatInBar === 8) this.synthSquareKick(time);
    if (beatInBar === 4 || beatInBar === 12) this.synthNoiseSnare(time);
    if (beatInBar % 2 === 0) this.synthHat(time, 0.18);

    // Fast arpeggiated chiptune melody (A minor pentatonic)
    const chipArp = [
      220.0, 329.6, 440.0, 659.2, 220.0, 329.6, 440.0, 523.2,
      261.6, 329.6, 523.2, 659.2, 196.0, 293.6, 392.0, 587.3,
      220.0, 329.6, 440.0, 659.2, 293.6, 392.0, 587.3, 783.9,
      329.6, 440.0, 659.2, 880.0, 261.6, 329.6, 523.2, 440.0
    ];
    this.synthSquare(time, chipArp[step], 0.18, 0.08);

    // Sub chip bass
    if (step % 4 === 0) {
      const bassNotes = [110, 110, 130.8, 98.0, 110, 146.8, 164.8, 130.8];
      this.synthSquare(time, bassNotes[Math.floor(step / 4)], 0.28, 0.16);
    }
  }

  // --- Track 3: Lo-Fi Chill (Smooth coffeehouse groove) ---
  playLofiStep(step, time) {
    const beatInBar = step % 16;
    // Soft kick on beat 1 and syncopated beat 3.5
    if (beatInBar === 0 || beatInBar === 10) this.synthSoftKick(time);
    if (beatInBar === 4 || beatInBar === 12) this.synthRimshot(time);
    // Swing shaker
    const shakerVol = beatInBar % 2 === 1 ? 0.2 : 0.08;
    this.synthHat(time, shakerVol);

    // Electric Piano Chord stab on beat 1 & 7
    if (step === 0 || step === 12 || step === 16 || step === 26) {
      this.synthRhodesChord(time, step < 16 ? [261.6, 329.6, 392.0, 493.8] : [220.0, 261.6, 329.6, 392.0]);
    }

    // Walking Lo-Fi Bassline
    const lofiBass = [
      65.4, 0, 0, 65.4, 0, 73.4, 0, 82.4, 0, 0, 87.3, 0, 98.0, 0, 87.3, 0,
      55.0, 0, 0, 55.0, 0, 65.4, 0, 73.4, 0, 0, 82.4, 0, 73.4, 0, 65.4, 0
    ];
    if (lofiBass[step] > 0) this.synthSoftBass(time, lofiBass[step]);
  }

  // --- Track 4: PvP Showdown (High stakes electronic battle) ---
  playBattleStep(step, time) {
    const beatInBar = step % 16;
    // Hard 4/4 driving industrial kick
    if (beatInBar % 4 === 0) this.synthPunchKick(time);
    if (beatInBar === 4 || beatInBar === 12) this.synthHardClap(time);
    this.synthHat(time, 0.25);

    // Aggressive saw bassline
    const sawBass = [
      65.4, 65.4, 0, 65.4, 77.8, 65.4, 87.3, 0, 65.4, 65.4, 0, 98.0, 87.3, 77.8, 65.4, 0,
      58.3, 58.3, 0, 58.3, 65.4, 58.3, 77.8, 0, 65.4, 0, 87.3, 0, 98.0, 116.5, 98.0, 87.3
    ];
    if (sawBass[step] > 0) this.synthSawBass(time, sawBass[step]);

    // Siren / synth lead arp on second bar
    if (step >= 16 && step % 2 === 0) {
      const battleLead = [523.2, 587.3, 622.2, 698.4, 783.9, 698.4, 622.2, 587.3];
      this.synthLeadPluck(time, battleLead[(step - 16) / 2]);
    }
  }

  // --- Instrument Synthesisers ---

  synthKick(time) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(140, time);
    osc.frequency.exponentialRampToValueAtTime(38, time + 0.09);
    gain.gain.setValueAtTime(0.7, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.15);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.15);
  }

  synthSoftKick(time) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(100, time);
    osc.frequency.exponentialRampToValueAtTime(42, time + 0.12);
    gain.gain.setValueAtTime(0.5, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.16);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.16);
  }

  synthPunchKick(time) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(180, time);
    osc.frequency.exponentialRampToValueAtTime(45, time + 0.1);
    gain.gain.setValueAtTime(0.85, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.16);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.16);
  }

  synthSquareKick(time) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(150, time);
    osc.frequency.exponentialRampToValueAtTime(35, time + 0.08);
    gain.gain.setValueAtTime(0.5, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.1);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.1);
  }

  synthSnare(time) {
    const bufferSize = this.ctx.sampleRate * 0.12;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 1000;
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.4, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.11);
    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    noise.start(time);
    noise.stop(time + 0.12);
  }

  synthNoiseSnare(time) {
    const bufferSize = this.ctx.sampleRate * 0.08;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = (Math.random() * 2 - 1) * 0.8;
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.35, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.08);
    noise.connect(gain);
    gain.connect(this.musicGain);
    noise.start(time);
    noise.stop(time + 0.08);
  }

  synthRimshot(time) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(450, time);
    osc.frequency.exponentialRampToValueAtTime(220, time + 0.04);
    gain.gain.setValueAtTime(0.25, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.05);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.05);
  }

  synthHardClap(time) {
    const bufferSize = this.ctx.sampleRate * 0.14;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 1400;
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.5, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.13);
    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    noise.start(time);
    noise.stop(time + 0.14);
  }

  synthHat(time, vol = 0.2) {
    const bufferSize = this.ctx.sampleRate * 0.035;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 6500;
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(vol, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.035);
    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    noise.start(time);
    noise.stop(time + 0.035);
  }

  synthBass(time, freq) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, time);
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(600, time);
    filter.frequency.exponentialRampToValueAtTime(180, time + 0.14);
    gain.gain.setValueAtTime(0.45, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.16);
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.16);
  }

  synthSoftBass(time, freq) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, time);
    gain.gain.setValueAtTime(0.4, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.28);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.28);
  }

  synthSawBass(time, freq) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, time);
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(900, time);
    filter.frequency.exponentialRampToValueAtTime(250, time + 0.18);
    gain.gain.setValueAtTime(0.5, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.18);
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.18);
  }

  synthSquare(time, freq, vol = 0.2, dur = 0.1) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(freq, time);
    gain.gain.setValueAtTime(vol, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + dur);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + dur);
  }

  synthLeadPluck(time, freq) {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, time);
    gain.gain.setValueAtTime(0.3, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.22);
    osc.connect(gain);
    gain.connect(this.musicGain);
    osc.start(time);
    osc.stop(time + 0.22);
  }

  synthRhodesChord(time, freqs) {
    freqs.forEach(f => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(f, time);
      gain.gain.setValueAtTime(0.12, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + 0.7);
      osc.connect(gain);
      gain.connect(this.musicGain);
      osc.start(time);
      osc.stop(time + 0.7);
    });
  }

  // --- Sound Effects (SFX) ---

  playPointP1() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    [523.25, 659.25, 783.99].forEach((freq, idx) => {
      const t = now + idx * 0.04;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, t);
      gain.gain.setValueAtTime(0.4, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
      osc.connect(gain);
      gain.connect(this.sfxGain);
      osc.start(t);
      osc.stop(t + 0.2);
    });
  }

  playPointP2() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    [392.00, 523.25, 659.25].forEach((freq, idx) => {
      const t = now + idx * 0.04;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, t);
      gain.gain.setValueAtTime(0.45, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
      osc.connect(gain);
      gain.connect(this.sfxGain);
      osc.start(t);
      osc.stop(t + 0.22);
    });
  }

  playRevealSound() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    [659.25, 987.77, 1318.51].forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now + idx * 0.03);
      gain.gain.setValueAtTime(0.3, now + idx * 0.03);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
      osc.connect(gain);
      gain.connect(this.sfxGain);
      osc.start(now + idx * 0.03);
      osc.stop(now + 0.45);
    });
  }

  playCardDeal() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    const bufferSize = this.ctx.sampleRate * 0.08;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
    }
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 1800;
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.25, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.sfxGain);
    noise.start(now);
    noise.stop(now + 0.08);
  }

  playVictoryFanfare() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    const melody = [
      { f: 392.0, d: 0.12, wait: 0.0 },
      { f: 523.25, d: 0.12, wait: 0.12 },
      { f: 659.25, d: 0.12, wait: 0.24 },
      { f: 783.99, d: 0.6, wait: 0.36 }
    ];
    melody.forEach(n => {
      const t = now + n.wait;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(n.f, t);
      gain.gain.setValueAtTime(0.45, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + n.d);
      osc.connect(gain);
      gain.connect(this.sfxGain);
      osc.start(t);
      osc.stop(t + n.d);
    });
  }

  playPenaltySound() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(140, now);
    osc.frequency.exponentialRampToValueAtTime(60, now + 0.25);
    gain.gain.setValueAtTime(0.38, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.25);
  }

  playBuzzer() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(120, now);
    osc.frequency.setValueAtTime(110, now + 0.1);
    gain.gain.setValueAtTime(0.3, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.22);
  }

  playTick() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(800, now);
    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.04);
  }

  playStreakChime(streak = 1) {
    this.ensureContext();
    const now = this.ctx.currentTime;
    const baseFreq = 440 * Math.pow(1.08, Math.min(15, streak));
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(baseFreq, now);
    osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.5, now + 0.18);
    gain.gain.setValueAtTime(0.35, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.28);
  }
}

export const soundEngine = new GameSoundEngine();
