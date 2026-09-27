import test from 'node:test';
import assert from 'node:assert/strict';

const BASE_URL = 'http://localhost:3000';

test('Nirixa Episteme OS PRD Scenarios Automated Test Suite', async (t) => {
  
  // --- Scenario 1: Raw Thought Triage ---
  await t.test('Scenario 1: Raw Thought Triage and Ingestion', async () => {
    const testQId = `Q-TEST-${Date.now()}`;
    // 1. Create a proposed question from raw capture
    const res = await fetch(`${BASE_URL}/api/episteme/questions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: testQId,
        eo_id: 'EO-001',
        text: 'Does mobile voice friction reveal deeper cognitive scars than typed keyboard notes?',
        priority: 'high',
        provenance: 'Telegram Mobile Capture #307',
      }),
    });
    const json = await res.json();
    assert.equal(json.success, true, 'Failed to create question from raw thought');
    assert.equal(json.id, testQId);

    // 2. Verify retrieval
    const qRes = await fetch(`${BASE_URL}/api/episteme/questions?eoId=EO-001`);
    const qJson = await qRes.json();
    assert.equal(qJson.success, true);
    const found = qJson.data.find((q) => q.id === testQId);
    assert.ok(found, 'Created question was not found under EO-001');
    assert.equal(found.provenance, 'Telegram Mobile Capture #307');
  });

  // --- Scenario 2 & 3: Literature & Media Claim Extraction ---
  await t.test('Scenario 2 & 3: Provenance-Preserving Evidence Extraction', async () => {
    const lineageRes = await fetch(`${BASE_URL}/api/episteme/lineage?eoId=EO-001`);
    const json = await lineageRes.json();
    assert.equal(json.success, true);
    assert.ok(json.data.eo, 'EO-001 missing in lineage');
    assert.ok(Array.isArray(json.data.questions), 'Questions must be an array');
    assert.ok(Array.isArray(json.data.evidence), 'Evidence must be an array');
    assert.ok(Array.isArray(json.data.beliefs), 'Beliefs must be an array');
  });

  // --- Scenario 4: Non-destructive Belief Revision ---
  await t.test('Scenario 4: Non-destructive Belief Change with Provenance Preservation', async () => {
    // 1. Create seed belief
    const testBeliefId = `B-TEST-${Date.now()}`;
    const createRes = await fetch(`${BASE_URL}/api/episteme/beliefs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: testBeliefId,
        eo_id: 'EO-001',
        proposition: 'Early prompt engineering holds durable 10-year value.',
        holder: 'human',
        status: 'working_belief',
        confidence: 0.70,
        supporting_evidence: 'Manual prompt templates work well in short conversations.',
      }),
    });
    const createJson = await createRes.json();
    assert.equal(createJson.success, true);

    // 2. Revise belief non-destructively
    const patchRes = await fetch(`${BASE_URL}/api/episteme/beliefs`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: testBeliefId,
        newProposition: 'Prompt engineering inverts into ambient telemetry and machine initiation (OTA-044).',
        newStatus: 'supported',
        newConfidence: 0.94,
        reasonForChange: 'Observed across 300+ production agent interactions that prompt initiation inverts.',
      }),
    });
    const patchJson = await patchRes.json();
    assert.equal(patchJson.success, true);
    assert.ok(patchJson.revisionId, 'Missing revisionId for audit log');

    // 3. Verify belief history is preserved and queryable
    const verifyRes = await fetch(`${BASE_URL}/api/episteme/beliefs?eoId=EO-001`);
    const verifyJson = await verifyRes.json();
    const updated = verifyJson.data.find((b) => b.id === testBeliefId);
    assert.ok(updated, 'Updated belief not found');
    assert.equal(updated.proposition, 'Prompt engineering inverts into ambient telemetry and machine initiation (OTA-044).');
    assert.equal(updated.confidence, 0.94);
    assert.ok(updated.revisions.length >= 1, 'Historical revision log must not be empty');
    assert.equal(updated.revisions[0].previous_proposition, 'Early prompt engineering holds durable 10-year value.');
  });

  // --- Scenario 5: Unexpected Discovery ---
  await t.test('Scenario 5: Unprompted AI Discovery Surface & Canonization', async () => {
    const res = await fetch(`${BASE_URL}/api/episteme/discoveries`);
    const json = await res.json();
    assert.equal(json.success, true);
    assert.ok(json.data.length >= 1, 'Expected at least one discovery');

    const firstDisc = json.data[0];
    assert.ok(firstDisc.confidence > 0, 'Discovery confidence must be positive');
    assert.ok(Array.isArray(firstDisc.objectsInvolved), 'Objects involved must be array');

    // Mutate status to investigating
    const patchRes = await fetch(`${BASE_URL}/api/episteme/discoveries`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: firstDisc.id, status: 'investigating' }),
    });
    const patchJson = await patchRes.json();
    assert.equal(patchJson.success, true);
  });

  // --- Scenario 6: Adversarial Epistemic Challenge ---
  await t.test('Scenario 6: Active Epistemic Disagreement and Premise Defense', async () => {
    const res = await fetch(`${BASE_URL}/api/episteme/challenges`);
    const json = await res.json();
    assert.equal(json.success, true);
    assert.ok(json.data.length >= 1, 'Expected active challenges');

    const firstChal = json.data[0];
    assert.ok(firstChal.challenge_thesis, 'Counter-thesis required for challenge');
    assert.ok(firstChal.counter_evidence || firstChal.potential_falsifier, 'Falsifier or counter-evidence required');

    // Respond to challenge by defending premise
    const patchRes = await fetch(`${BASE_URL}/api/episteme/challenges`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: firstChal.id, status: 'defended' }),
    });
    const patchJson = await patchRes.json();
    assert.equal(patchJson.success, true);
  });

  // --- Scenario 7: Longitudinal Self-Inquiry (Ask Nirixa) ---
  await t.test('Scenario 7: Longitudinal Self-Inquiry via Jarvis Engine', async () => {
    const res = await fetch(`${BASE_URL}/api/episteme/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'How have I changed since I started using Nirixa?' }),
    });
    const json = await res.json();
    assert.equal(json.success, true);
    assert.equal(json.type, 'self_inquiry');
    assert.ok(json.summary.includes('epistemic trajectory') || json.summary.includes('Monish'));
    assert.ok(json.data.coevolutionEvents, 'Coevolution events missing in response');
  });

  // --- Scenario 8: Thought Lineage Traversal ---
  await t.test('Scenario 8: Complete Thought Lineage Hierarchy Traversal', async () => {
    const res = await fetch(`${BASE_URL}/api/episteme/lineage?eoId=EO-001`);
    const json = await res.json();
    assert.equal(json.success, true);
    assert.equal(json.data.eo.id, 'EO-001');
    assert.ok(json.data.lineageSummary.includes('EO-001'), 'Lineage summary must include anchor ID');
  });

  // --- Scenario 9: 2026 -> 2029 Coevolution Horizon ---
  await t.test('Scenario 9: 2026-2029 Coevolution Horizon Telemetry', async () => {
    const res = await fetch(`${BASE_URL}/api/cockpit`);
    const json = await res.json();
    assert.equal(json.success, true);
    assert.ok(json.data.metrics.capturesCount > 0, 'Captures count must be positive');
    assert.ok(json.data.chapters.length >= 1, 'Book chapters must be populated');
  });

  // --- Scenario 10: Human-AI Contribution Lineage ---
  await t.test('Scenario 10: Attribution Analysis of AI vs Human Contribution', async () => {
    const res = await fetch(`${BASE_URL}/api/episteme/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'Which of my ideas were discovered by AI?' }),
    });
    const json = await res.json();
    assert.equal(json.success, true);
    assert.equal(json.type, 'attribution');
    assert.ok(json.data.aiInfluencedBeliefs, 'AI-influenced beliefs missing');
  });

});
