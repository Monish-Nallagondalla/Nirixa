import Database from 'better-sqlite3';

export function initializeEpistemicSchema(db: Database.Database) {
  // 1. Core Epistemic Primitives per PRD Sections 5 & 6
  db.exec(`
    CREATE TABLE IF NOT EXISTS epistemic_objects (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      description TEXT,
      status TEXT DEFAULT 'active', -- active, dormant, decomposed, superseded, archived
      maturity INTEGER DEFAULT 10,  -- 0 to 100
      uncertainty REAL DEFAULT 0.5, -- 0.0 to 1.0
      category TEXT DEFAULT 'Epistemology',
      provenance TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS questions (
      id TEXT PRIMARY KEY,
      eo_id TEXT,
      text TEXT NOT NULL,
      status TEXT DEFAULT 'investigating', -- open, investigating, partially_answered, answered, reopened, dormant, superseded
      priority TEXT DEFAULT 'high',        -- high, medium, low
      provenance TEXT,
      history TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (eo_id) REFERENCES epistemic_objects(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS beliefs (
      id TEXT PRIMARY KEY,
      eo_id TEXT,
      proposition TEXT NOT NULL,
      holder TEXT DEFAULT 'human',          -- human, ai, joint
      status TEXT DEFAULT 'working_belief', -- hypothesis, working_belief, uncertain, supported, challenged, rejected, superseded
      confidence REAL DEFAULT 0.70,         -- 0.0 to 1.0
      supporting_evidence TEXT,
      counter_evidence TEXT,
      falsifier TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (eo_id) REFERENCES epistemic_objects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS evidence (
      id TEXT PRIMARY KEY,
      source_id TEXT,
      eo_id TEXT,
      claim TEXT NOT NULL,
      content TEXT,
      type TEXT DEFAULT 'observation',      -- observation, source_claim, experimental_result, data, argument, counterexample, personal_experience, literature_finding
      strength REAL DEFAULT 0.75,          -- 0.0 to 1.0
      interpretation TEXT,
      provenance TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (eo_id) REFERENCES epistemic_objects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS connections (
      id TEXT PRIMARY KEY,
      source_id TEXT NOT NULL,
      target_id TEXT NOT NULL,
      relationship_type TEXT NOT NULL,      -- SUPPORTS, CONTRADICTS, EXTENDS, REFINES, DERIVES_FROM, INSPIRED_BY, ANALOGOUS_TO, QUESTIONS, GENERATES
      reason TEXT,
      confidence REAL DEFAULT 0.80,
      human_verified INTEGER DEFAULT 0,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS discoveries (
      id TEXT PRIMARY KEY,
      type TEXT NOT NULL,                   -- unexpected_connection, contradiction, forgotten_idea, neglected_question, research_opportunity, pattern
      title TEXT NOT NULL,
      description TEXT NOT NULL,
      objects_involved TEXT,                -- JSON string array e.g. ["EO-004", "Q-017"]
      reasoning TEXT,
      confidence REAL DEFAULT 0.85,
      status TEXT DEFAULT 'candidate',      -- candidate, investigating, accepted, dismissed, challenged
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS challenges (
      id TEXT PRIMARY KEY,
      belief_id TEXT,
      claim TEXT NOT NULL,
      challenge_thesis TEXT NOT NULL,
      counter_evidence TEXT,
      potential_falsifier TEXT,
      status TEXT DEFAULT 'active',         -- active, defended, investigating, revised, rejected, deferred
      created_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (belief_id) REFERENCES beliefs(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS coevolution_events (
      id TEXT PRIMARY KEY,
      timestamp TEXT DEFAULT (datetime('now')),
      human_state_change TEXT,
      ai_state_change TEXT,
      interaction_summary TEXT,
      downstream_effect TEXT,
      evidence TEXT
    );

    CREATE TABLE IF NOT EXISTS epistemic_work (
      id TEXT PRIMARY KEY,
      actor TEXT DEFAULT 'human',           -- human, ai, joint
      work_type TEXT NOT NULL,              -- discovery, inquiry, synthesis, validation, challenge, reflection, revision, experimentation
      target_eo_id TEXT,
      before_state TEXT,
      action_taken TEXT NOT NULL,
      epistemic_change TEXT NOT NULL,
      after_state TEXT,
      evidence_id TEXT,
      confidence REAL DEFAULT 0.85,
      timestamp TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (target_eo_id) REFERENCES epistemic_objects(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS belief_revisions (
      id TEXT PRIMARY KEY,
      belief_id TEXT NOT NULL,
      previous_proposition TEXT,
      new_proposition TEXT NOT NULL,
      previous_status TEXT,
      new_status TEXT NOT NULL,
      previous_confidence REAL,
      new_confidence REAL,
      reason_for_change TEXT NOT NULL,
      work_id TEXT,
      revised_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (belief_id) REFERENCES beliefs(id) ON DELETE CASCADE
    );
  `);

  // 2. Auto-seed Epistemic Objects from existing ota_assets if empty
  try {
    const insertEo = db.prepare(`
      INSERT OR IGNORE INTO epistemic_objects (id, title, description, category, maturity, uncertainty, provenance)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `);

    // Ensure core PRD EOs always exist
    insertEo.run('EO-001', 'Questions as Computational Primitives', 'Inquiry precedes answers and compounds over time.', 'Epistemology', 90, 0.2, 'PRD Seed');
    insertEo.run('EO-004', 'Contextual Retrieval of Human Intentions', 'Retrieving context based on human epistemic trajectories.', 'AI Architecture', 80, 0.3, 'PRD Seed');
    insertEo.run('EO-010', 'Persistent AI Disagreement & Sparring', 'AI that challenges premises instead of auto-completing.', 'Cognition', 85, 0.25, 'PRD Seed');
    insertEo.run('EO-012', 'Longitudinal Human-AI Coevolution', 'Continuous mutual adaptation of human reasoning and machine context.', 'Systems', 75, 0.4, 'PRD Seed');

    // Also map any existing ota_assets
    try {
      const otaRows = db.prepare('SELECT * FROM ota_assets').all() as any[];
      for (const ota of otaRows) {
        if (!ota.id) continue;
        const eoId = ota.id.toUpperCase().replace('OTA_', 'EO-').replace('OTA-', 'EO-');
        insertEo.run(
          eoId,
          ota.title || 'Original Thought Asset',
          ota.summary || ota.thesis || '',
          ota.category || 'Epistemology',
          ota.maturity_score || 65,
          0.35,
          'Mapped from OTA Bank'
        );
      }
    } catch {
      // ota_assets table might not exist in some environments
    }
  } catch (err) {
    console.warn('EO seeding warning:', err);
  }

  // 3. Seed initial questions if empty
  const qCount = db.prepare('SELECT count(*) as count FROM questions').get() as { count: number };
  if (qCount && qCount.count === 0) {
    const insertQ = db.prepare(`
      INSERT OR IGNORE INTO questions (id, eo_id, text, status, priority, provenance)
      VALUES (?, ?, ?, ?, ?, ?)
    `);
    insertQ.run('Q-001', 'EO-001', 'How does persistent AI interaction alter human hypothesis formulation?', 'investigating', 'high', 'PhD Thesis RQ1');
    insertQ.run('Q-004', 'EO-004', 'What distinguishes active epistemic work from passive document consumption?', 'open', 'high', 'Epistemic PRD');
    insertQ.run('Q-010', 'EO-010', 'Can an AI disagree effectively without destroying conversational flow?', 'investigating', 'medium', 'Sparring Harness');
    insertQ.run('Q-012', 'EO-012', 'What metrics quantify cognitive independence versus cognitive atrophy under AI pairing?', 'investigating', 'high', 'PhD Thesis RQ3');
  }

  // 4. Seed initial beliefs if empty
  const bCount = db.prepare('SELECT count(*) as count FROM beliefs').get() as { count: number };
  if (bCount && bCount.count === 0) {
    const insertB = db.prepare(`
      INSERT OR IGNORE INTO beliefs (id, eo_id, proposition, holder, status, confidence, supporting_evidence, counter_evidence, falsifier)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);
    insertB.run(
      'B-001',
      'EO-001',
      'Questions compound exponentially in intellectual value while factual answers decay.',
      'human',
      'working_belief',
      0.88,
      'Longitudinal tracking in My-Os shows persistent inquiry anchors produce 4x higher draft density.',
      'Factual lookups are commoditized by frontier search models.',
      'Demonstrating that users with high answer turnover generate equal high-level output.'
    );
    insertB.run(
      'B-004',
      'EO-004',
      'Context retrieval based purely on semantic vector distance creates cognitive echo chambers.',
      'joint',
      'supported',
      0.92,
      'Cosine similarity repeatedly retrieves redundant synonyms instead of orthogonal conceptual analogies.',
      'Rerankers slightly mitigate synonym loops.',
      'A purely dense vector space outperforming hybrid graph-directed retrieval on thesis generation.'
    );
    insertB.run(
      'B-010',
      'EO-010',
      'Passive AI agreement degrades human critical calibration over 6+ month horizons.',
      'ai',
      'challenged',
      0.68,
      'Recent study on sycophantic LLMs reinforcing false user assumptions.',
      'Users often find friction irritating and abandon critical agents.',
      'Longitudinal user cohorts maintaining equal critical sharpness with sycophantic assistants.'
    );
  }

  // 5. Seed initial discoveries if empty
  const dCount = db.prepare('SELECT count(*) as count FROM discoveries').get() as { count: number };
  if (dCount && dCount.count === 0) {
    const insertD = db.prepare(`
      INSERT OR IGNORE INTO discoveries (id, type, title, description, objects_involved, reasoning, confidence, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
    insertD.run(
      'DISC-001',
      'unexpected_connection',
      'Biological Memory Reconsolidation ↔ Epistemic State Updating',
      'Discovered that neurobiological reconsolidation (Nader et al.) maps 1:1 onto your non-destructive belief revision architecture in EO-001.',
      JSON.stringify(['EO-001', 'EO-004', 'Q-001']),
      'Both processes require an active reactivation state before mutation, preventing retroactive catastrophic forgetting.',
      0.91,
      'candidate'
    );
    insertD.run(
      'DISC-002',
      'contradiction',
      'Local-First Sovereignty vs Continuous Multi-Device Sparring',
      'Your desire for offline SQLite permanence conflicts with instantaneous mobile Telegram capture syncing during network dropouts.',
      JSON.stringify(['EO-012', 'Q-010']),
      'A conflict-free append-only log is required to reconcile mobile telegram queue with desktop SQLite state without data loss.',
      0.84,
      'investigating'
    );
    insertD.run(
      'DISC-003',
      'forgotten_idea',
      'Falsification Thresholds for AI Hypotheses (from June 2026)',
      'You logged a note on requiring an explicit falsifier before any AI-generated hypothesis is accepted into the thesis graph, but haven\'t tested it.',
      JSON.stringify(['EO-010', 'B-010']),
      'Unresolved for 74 days despite accumulating 12 supporting capture fragments.',
      0.88,
      'candidate'
    );
  }

  // 6. Seed initial challenges if empty
  const chCount = db.prepare('SELECT count(*) as count FROM challenges').get() as { count: number };
  if (chCount && chCount.count === 0) {
    const insertCh = db.prepare(`
      INSERT OR IGNORE INTO challenges (id, belief_id, claim, challenge_thesis, counter_evidence, potential_falsifier)
      VALUES (?, ?, ?, ?, ?, ?)
    `);
    insertCh.run(
      'CHAL-001',
      'B-010',
      'Passive AI agreement degrades human critical calibration over 6+ month horizons.',
      'Nirixa challenges this: Could structured sycophancy actually lower friction for divergent ideation, with calibration managed by downstream external verification?',
      'Brainstorming literature demonstrates that early non-critical affirmation increases total novel conceptual variance by 37%.',
      'If Monish generates more original thesis hooks during uncritical flow sessions than during adversarial sparring.'
    );
    insertCh.run(
      'CHAL-002',
      'B-004',
      'Context retrieval based purely on semantic vector distance creates cognitive echo chambers.',
      'Is semantic distance genuinely the culprit, or is it the lack of dynamic temporal decay and attention budget weighting?',
      'New hyperbolic embedding spaces capture hierarchical taxonomic leaps that flat Euclidean cosine spaces miss.',
      'Testing an experiment comparing graph-directed retrieval with hyperbolic vector embeddings on your 48 OTAs.'
    );
  }

  // 7. Seed initial coevolution events if empty
  const coCount = db.prepare('SELECT count(*) as count FROM coevolution_events').get() as { count: number };
  if (coCount && coCount.count === 0) {
    const insertCo = db.prepare(`
      INSERT OR IGNORE INTO coevolution_events (id, timestamp, human_state_change, ai_state_change, interaction_summary, downstream_effect)
      VALUES (?, ?, ?, ?, ?, ?)
    `);
    insertCo.run(
      'COEV-001',
      '2026-09-01 10:30:00',
      'Shifted from viewing AI as a rapid copywriter to an ontological research partner.',
      'Adapted retrieval from raw keyword matching to multi-hop question lineage traversal.',
      'Monish challenged the auto-generated summary; AI pushed back with empirical scar citation.',
      'Resulted in Chapter 2 draft "The Coevolution of Thought" reaching 74% maturity.'
    );
  }
}
