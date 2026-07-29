---
layout: default
title: Safety model
description: Understand BitFloppy device states and the safety boundaries of its offline signing workflow.
---

<p class="eyebrow">// SAFETY MODEL</p>

# Offline is a boundary, not a promise.

<p class="lead">BitFloppy is a testnet/signet proof of concept. Its primary safety boundary is the separation between a networked wallet application and the private signing material on the board.</p>

<section class="state-grid">
  <article class="state-card"><p>DEFAULT STATE</p><h2>Locked</h2><ul><li>Public wallet files are available.</li><li>Private material stays unavailable.</li><li>Use this state for normal operation.</li></ul></article>
  <article class="state-card emphasis"><p>SIGNING STATE</p><h2>Unlocked</h2><ul><li>Private material is exposed to the device workflow.</li><li>Required for transaction signing.</li><li>Keep this period short and controlled.</li></ul></article>
</section>

## Practical safety checklist

<div class="checklist">
  <div><span>✓</span><p>Use testnet or signet only. Do not use this proof of concept with real funds.</p></div>
  <div><span>✓</span><p>Verify transaction details in your wallet application before creating a PSBT.</p></div>
  <div><span>✓</span><p>Safely eject the USB drive before restarting the board.</p></div>
  <div><span>✓</span><p>Restart the board after signing to return to the locked state.</p></div>
</div>

<p class="callout">Need the underlying file and state details? Read the <a href="user-guide.html">user guide</a>.</p>
