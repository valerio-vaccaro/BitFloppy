---
layout: default
title: Offline signer
description: BitFloppy is an offline Bitcoin signer that uses a simple, file-based workflow.
---

<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">// BITCOIN HARDWARE WALLET</p>
    <h1>Wallet on a floppy.</h1>
    <p>An offline Bitcoin signer with a simple file-based workflow. Move PSBT files by USB and keep signing keys off the network.</p>
    <p class="status-line">SYSTEM STATUS: READY<span class="cursor">_</span></p>
    <div class="button-row">
      <a class="pixel-button" href="flashing.html">FLASH FIRMWARE</a>
      <a class="pixel-button alt" href="sparrow.html">USE WITH SPARROW</a>
    </div>
  </div>
  <div class="floppy-stage">
    <figure class="floppy-photo">
      <img src="images/bitfloppy-retro-room.jpg" alt="Retro pixel-art room featuring the BitFloppy Bitcoin wallet">
      <figcaption>BITFLOPPY // OFFLINE BY DESIGN</figcaption>
    </figure>
  </div>
</section>

<section>
  <p class="eyebrow">// QUICK START</p>
  <div class="panel-grid">
    <article class="panel">
      <h3>01. Flash it</h3>
      <p>Install BitFloppy on a supported Lolin S2 Mini.</p>
      <p><a href="flashing.html">Open flashing guide →</a></p>
    </article>
    <article class="panel">
      <h3>02. Connect it</h3>
      <p>Use the board as a small, familiar USB storage drive.</p>
      <p><a href="user-guide.html">Read the user guide →</a></p>
    </article>
    <article class="panel">
      <h3>03. Sign offline</h3>
      <p>Copy a PSBT to the drive and retrieve the signed result.</p>
      <p><a href="sparrow.html">Set up Sparrow →</a></p>
    </article>
  </div>
</section>

<section class="overview-section">
  <div>
    <p class="eyebrow">// THE OFFLINE PATH</p>
    <h2>One file, one direction.</h2>
    <p class="section-intro">BitFloppy keeps the signing step deliberately small. Prepare a transaction on your computer, move a PSBT to the device, then bring back the signed result.</p>
    <a class="text-link" href="workflow.html">See the complete signing workflow <span>→</span></a>
  </div>
  <div class="flow-chart" role="img" aria-label="A three-step flow: create a PSBT, move it to BitFloppy, retrieve the signed PSBT">
    <div class="flow-step"><span>01</span><strong>Prepare</strong><small>Create a PSBT</small></div>
    <i aria-hidden="true">→</i>
    <div class="flow-step active"><span>02</span><strong>Sign offline</strong><small>Use BitFloppy</small></div>
    <i aria-hidden="true">→</i>
    <div class="flow-step"><span>03</span><strong>Finalize</strong><small>Import result</small></div>
  </div>
</section>

<section class="safety-section">
  <div>
    <p class="eyebrow">// EXPOSURE AT A GLANCE</p>
    <h2>Choose the smallest surface.</h2>
    <p class="section-intro">Keep the device locked for normal wallet access. Unlock only for the brief signing step, then reboot to return to the safer default state.</p>
    <a class="text-link" href="security.html">Read the safety model <span>→</span></a>
  </div>
  <div class="exposure-chart" role="img" aria-label="Exposure chart showing locked mode with limited public wallet data and unlocked mode with sensitive signing material">
    <div class="chart-head"><span>Device state</span><span>Data exposure</span></div>
    <div class="chart-row"><strong>Locked</strong><div class="bar"><b style="width: 32%"></b></div><em>Public wallet files</em></div>
    <div class="chart-row"><strong>Unlocked</strong><div class="bar warn"><b style="width: 78%"></b></div><em>Sensitive key material</em></div>
    <p class="chart-note">Reboot after signing to return to locked mode.</p>
  </div>
</section>
