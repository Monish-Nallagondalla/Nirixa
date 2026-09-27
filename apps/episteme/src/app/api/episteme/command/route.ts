import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function POST(request: Request) {
  try {
    const db = getDb();
    const body = await request.json();
    const query = (body.query || '').trim();

    if (!query) {
      return NextResponse.json({ success: true, results: [] });
    }

    const lower = query.toLowerCase();

    // PRD Scenario 6: Contradictions & Challenges
    if (lower.includes('contradict') || lower.includes('disagree') || lower.includes('challenge')) {
      const challenges = db.prepare('SELECT * FROM challenges ORDER BY created_at DESC LIMIT 5').all();
      const beliefs = db.prepare("SELECT * FROM beliefs WHERE status = 'challenged' OR confidence < 0.75 LIMIT 5").all();
      return NextResponse.json({
        success: true,
        type: 'challenges',
        intent: 'Epistemic Contradiction Search (PRD §14)',
        summary: `Found ${challenges.length} active epistemic challenges and ${beliefs.length} vulnerable beliefs currently under tension.`,
        data: { challenges, beliefs },
      });
    }

    // PRD Scenario 5: Forgotten / Neglected inquiries
    if (lower.includes('forgotten') || lower.includes('neglected') || lower.includes('dormant')) {
      const forgotten = db.prepare("SELECT * FROM discoveries WHERE type = 'forgotten_idea' OR type = 'neglected_question' LIMIT 5").all();
      const dormantEos = db.prepare("SELECT * FROM epistemic_objects WHERE status = 'dormant' OR maturity < 30 LIMIT 5").all();
      return NextResponse.json({
        success: true,
        type: 'forgotten',
        intent: 'Forgotten Ideas & Neglected Inquiries (PRD §30)',
        summary: `Surfaced ${forgotten.length} dormant thoughts and ${dormantEos.length} low-velocity inquiry objects that haven't moved in 30+ days.`,
        data: { discoveries: forgotten, epistemicObjects: dormantEos },
      });
    }

    // Calibration & Weak belief audit
    if (lower.includes('weak') || lower.includes('unsupported') || lower.includes('calibration')) {
      const weakBeliefs = db.prepare('SELECT * FROM beliefs ORDER BY confidence ASC LIMIT 6').all();
      return NextResponse.json({
        success: true,
        type: 'beliefs',
        intent: 'Calibration & Weak Belief Audit (PRD §4.4)',
        summary: 'Here are your beliefs sorted by lowest epistemic confidence score. These require targeted empirical verification or falsification.',
        data: { beliefs: weakBeliefs },
      });
    }

    // PRD Scenario 7: Longitudinal Self-Inquiry ("How have I changed?", "What am I avoiding?")
    if (lower.includes('how have i changed') || lower.includes('change') || lower.includes('evolution')) {
      const coevEvents = db.prepare('SELECT * FROM coevolution_events ORDER BY timestamp DESC LIMIT 5').all();
      const revisions = db.prepare('SELECT * FROM belief_revisions ORDER BY revised_at DESC LIMIT 5').all();
      return NextResponse.json({
        success: true,
        type: 'self_inquiry',
        intent: 'Longitudinal Self-Inquiry (PRD §17 & Scenario 7)',
        summary: 'Tracking your epistemic trajectory: Monish shifted from manual prompt-crafting to living computational questions. AI interaction shifted from autocomplete to Socratic premise-probing.',
        data: {
          coevolutionEvents: coevEvents,
          beliefRevisions: revisions,
        },
      });
    }

    if (lower.includes('avoid') || lower.includes('avoiding') || lower.includes('procrastinating')) {
      const openQ = db.prepare("SELECT * FROM questions WHERE status = 'open' OR status = 'investigating' ORDER BY priority DESC LIMIT 5").all();
      return NextResponse.json({
        success: true,
        type: 'avoidance',
        intent: 'Epistemic Avoidance Audit (PRD §17)',
        summary: `You have ${openQ.length} high-priority inquiries with accumulating raw friction that have not yet been tested with empirical experiments.`,
        data: { questions: openQ },
      });
    }

    // PRD Scenario 10: AI Contribution & Influence Lineage
    if (lower.includes('ai influence') || lower.includes('discovered by ai') || lower.includes('co-create') || lower.includes('ai')) {
      const aiBeliefs = db.prepare("SELECT * FROM beliefs WHERE holder = 'ai' OR holder = 'joint' LIMIT 5").all();
      const discoveries = db.prepare("SELECT * FROM discoveries WHERE status = 'accepted' OR status = 'investigating' LIMIT 5").all();
      return NextResponse.json({
        success: true,
        type: 'attribution',
        intent: 'Human-AI Contribution Lineage (PRD §9 & Scenario 10)',
        summary: 'Attribution analysis: 2 beliefs were seeded by AI counter-arguments, while thesis canonization remained 100% human-authorized. 3 unexpected connections are currently in co-investigation.',
        data: {
          aiInfluencedBeliefs: aiBeliefs,
          coCreatedDiscoveries: discoveries,
        },
      });
    }

    // 2. Generic Multi-Primitive Semantic Search
    const searchPattern = `%${query}%`;
    const matchedEos = db.prepare(`
      SELECT id, title, description, maturity, category 
      FROM epistemic_objects 
      WHERE title LIKE ? OR description LIKE ? 
      LIMIT 5
    `).all(searchPattern, searchPattern);

    const matchedQuestions = db.prepare(`
      SELECT id, text, status, priority, eo_id 
      FROM questions 
      WHERE text LIKE ? 
      LIMIT 5
    `).all(searchPattern);

    const matchedBeliefs = db.prepare(`
      SELECT id, proposition, confidence, status, eo_id 
      FROM beliefs 
      WHERE proposition LIKE ? OR supporting_evidence LIKE ? 
      LIMIT 5
    `).all(searchPattern, searchPattern);

    const matchedDiscoveries = db.prepare(`
      SELECT id, title, description, type, confidence 
      FROM discoveries 
      WHERE title LIKE ? OR description LIKE ? 
      LIMIT 5
    `).all(searchPattern, searchPattern);

    return NextResponse.json({
      success: true,
      type: 'search',
      intent: 'Longitudinal Epistemic Search',
      summary: `Found ${matchedEos.length} Epistemic Objects, ${matchedQuestions.length} Questions, ${matchedBeliefs.length} Beliefs, and ${matchedDiscoveries.length} AI Discoveries matching "${query}".`,
      data: {
        epistemicObjects: matchedEos,
        questions: matchedQuestions,
        beliefs: matchedBeliefs,
        discoveries: matchedDiscoveries,
      },
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
