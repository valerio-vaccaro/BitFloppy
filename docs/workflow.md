---
layout: default
title: Signing workflow
description: A step-by-step view of the BitFloppy offline PSBT workflow.
---

<p class="eyebrow">// SIGNING WORKFLOW</p>

# From transaction to signed file.

<p class="lead">BitFloppy uses files as the handoff between an online wallet application and an offline signing device. The process is intentionally linear and easy to inspect.</p>

<section class="workflow-list">
  <article>
    <span>01</span>
    <div><h2>Prepare in Sparrow</h2><p>Create a transaction in Sparrow Wallet and export it as a base64 PSBT. Review the recipient, amount, and fee before moving to the next step.</p></div>
  </article>
  <article>
    <span>02</span>
    <div><h2>Move the PSBT</h2><p>Connect BitFloppy as USB storage and create <code>PSBT.txt</code> containing the exported PSBT. Safely eject the drive when finished.</p></div>
  </article>
  <article class="workflow-emphasis">
    <span>03</span>
    <div><h2>Restart and sign</h2><p>Restart the board. BitFloppy processes the file and creates <code>PSBT_signed.txt</code>. Treat the device as sensitive while it is unlocked.</p></div>
  </article>
  <article>
    <span>04</span>
    <div><h2>Import and finalize</h2><p>Copy the signed PSBT back to Sparrow, inspect it again, and finalize or broadcast it from your connected computer.</p></div>
  </article>
</section>

<p class="callout">For the exact Sparrow actions and supported address types, visit <a href="sparrow.html">Sparrow integration</a>. Reboot BitFloppy once more after signing to return it to locked mode.</p>
