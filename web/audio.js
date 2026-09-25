// Web Audio API Synthesizer Engine
// 100% Royalty-Free, Zero-Copyright procedural Kahoot-style upbeat game music & SFX

class GameSoundEngine {
  constructor() {
    this.ctx = null;
    this.musicGain = null;
    this.sfxGain = null;
    this.masterGain = null;

    this.isPlayingMusic = false;
    this.isMuted = false;
    this.currentTempo = 126; // BPM (classic upbeat Kahoot feel)
    this.step = 0;
    this.timerId = null;

    this.musicVolume = 0.45;
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
  }

  ensureContext() {
    this.init();
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // --- Background Music (Kahoot-Style Electro Funk Beat) ---
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

  setVolume(val) {
    if (this.masterGain && this.ctx) {
      this.masterGain.gain.setValueAtTime(val, this.ctx.currentTime);
    }
  }

  setTempo(bpm) {
    this.currentTempo = Math.max(90, Math.min(160, bpm));
  }

  scheduleNextBeat() {
    if (!this.isPlayingMusic || !this.ctx) return;

    const secondsPer16th = 60.0 / (this.currentTempo * 4);
    const now = this.ctx.currentTime;

    this.playStep(this.step, now);

    this.step = (this.step + 1) % 32; // 2-bar 16th-note loop

    this.timerId = setTimeout(() => {
      this.scheduleNextBeat();
    }, secondsPer16th * 1000);
  }

  playStep(step, time) {
    // 16 steps per bar, 32 steps for 2-bar pattern
    const beatInBar = step % 16;
    const isQuarter = beatInBar % 4 === 0;
    const isBackbeat = beatInBar === 4 || beatInBar === 12;

    // 1. Kick Drum: on every beat 1, 2, 3, 4 (four-on-the-floor driving pulse)
    if (isQuarter) {
      this.synthKick(time);
    }

    // 2. Snare / Clap: on beats 2 and 4 (steps 4 and 12)
    if (isBackbeat) {
      this.synthSnare(time);
    }

    // 3. Hi-Hat / Shaker: 16th notes with groove velocity
    const hatVolume = isQuarter ? 0.35 : (beatInBar % 2 === 0 ? 0.25 : 0.15);
    this.synthHat(time, hatVolume);

    // 4. Funky Synth Bassline (D minor / F pentatonic groove)
    // Notes: D2 (73.4Hz), F2 (87.3Hz), G2 (98.0Hz), A2 (110.0Hz), C3 (130.8Hz)
    const bassLine = [
      73.4,  0, 73.4,  0,  // D2, _, D2, _
      0,  87.3, 98.0,  0,  // _, F2, G2, _
     73.4,  0, 110.0,  0,  // D2, _, A2, _
      0, 130.8, 98.0,  0,  // _, C3, G2, _
      // Bar 2
      73.4,  0, 73.4,  0,
     87.3,  0, 98.0,  0,
     110.0, 0, 130.8, 0,
     146.8, 0, 110.0, 98.0 // D3, _, A2, G2
    ];

    const freq = bassLine[step];
    if (freq > 0) {
      this.synthBass(time, freq);
    }

    // 5. Playful Arpeggio / Lead Pluck (Kahoot melodic sparkle)
    // D4 (293.6), F4 (349.2), G4 (392.0), A4 (440.0), C5 (523.2), D5 (587.3)
    const arpNotes = [
      293.6,     0, 349.2,     0, 392.0, 440.0,     0, 523.2,
      587.3, 523.2, 440.0, 392.0, 349.2,     0, 392.0,     0,
      // Bar 2
      293.6,     0, 440.0,     0, 523.2,     0, 587.3,     0,
      698.4, 587.3, 523.2, 440.0, 392.0, 349.2, 293.6,     0
    ];

    const leadFreq = arpNotes[step];
    if (leadFreq > 0) {
      this.synthLeadPluck(time, leadFreq);
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

  synthSnare(time) {
    // Noise buffer
    const bufferSize = this.ctx.sampleRate * 0.12;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 1000;

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.4, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.11);

    // Body tone
    const osc = this.ctx.createOscillator();
    const oscGain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(190, time);
    osc.frequency.exponentialRampToValueAtTime(80, time + 0.08);
    oscGain.gain.setValueAtTime(0.3, time);
    oscGain.gain.exponentialRampToValueAtTime(0.001, time + 0.08);

    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);

    osc.connect(oscGain);
    oscGain.connect(this.musicGain);

    noise.start(time);
    noise.stop(time + 0.12);
    osc.start(time);
    osc.stop(time + 0.08);
  }

  synthHat(time, vol = 0.2) {
    const bufferSize = this.ctx.sampleRate * 0.035;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 7500;

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
    const filter = this.ctx.createBiquadFilter();
    const gain = this.ctx.createGain();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, time);

    filter.type = 'lowpass';
    filter.Q.value = 4.0;
    filter.frequency.setValueAtTime(1200, time);
    filter.frequency.exponentialRampToValueAtTime(180, time + 0.16);

    gain.gain.setValueAtTime(0.35, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.18);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);

    osc.start(time);
    osc.stop(time + 0.18);
  }

  synthLeadPluck(time, freq) {
    const osc = this.ctx.createOscillator();
    const filter = this.ctx.createBiquadFilter();
    const gain = this.ctx.createGain();

    osc.type = 'square';
    osc.frequency.setValueAtTime(freq, time);

    filter.type = 'bandpass';
    filter.Q.value = 2.0;
    filter.frequency.setValueAtTime(freq * 2.2, time);

    gain.gain.setValueAtTime(0.18, time);
    gain.gain.exponentialRampToValueAtTime(0.001, time + 0.12);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.musicGain);

    osc.start(time);
    osc.stop(time + 0.12);
  }

  // --- Sound Effects (SFX) ---

  playScorePoint() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    // Cheerful ascending arpeggio (C5, E5, G5, C6)
    const notes = [523.25, 659.25, 783.99, 1046.5];
    notes.forEach((freq, idx) => {
      const t = now + idx * 0.06;
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

  playRevealSound() {
    this.ensureContext();
    const now = this.ctx.currentTime;
    // Sparkly chime chord (E5, B5, E6)
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
    // Crisp card whoosh
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
    // Major triumphant triad fanfare (G4, C5, E5, G5 sustained)
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
}

export const soundEngine = new GameSoundEngine();
