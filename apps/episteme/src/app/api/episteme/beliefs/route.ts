import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);
    const eoId = searchParams.get('eoId');
    const status = searchParams.get('status');
    const holder = searchParams.get('holder');

    let query = 'SELECT * FROM beliefs';
    const params: any[] = [];
    const conditions: string[] = [];

    if (eoId) {
      conditions.push('eo_id = ?');
      params.push(eoId);
    }
    if (status) {
      conditions.push('status = ?');
      params.push(status);
    }
    if (holder) {
      conditions.push('holder = ?');
      params.push(holder);
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    query += ' ORDER BY confidence DESC, updated_at DESC';

    const beliefs = db.prepare(query).all(...params) as any[];

    // Enrich with revisions history
    const enriched = beliefs.map((b) => {
      const revisions = db.prepare('SELECT * FROM belief_revisions WHERE belief_id = ? ORDER BY revised_at DESC').all(b.id);
      return {
        ...b,
        revisions,
      };
    });

    return NextResponse.json({ success: true, data: enriched });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const db = getDb();
    const body = await request.json();
    const { id, eo_id, proposition, holder, status, confidence, supporting_evidence, counter_evidence, falsifier } = body;

    const newId = id || `B-${Math.floor(100 + Math.random() * 900)}`;
    db.prepare(`
      INSERT INTO beliefs (id, eo_id, proposition, holder, status, confidence, supporting_evidence, counter_evidence, falsifier)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      newId,
      eo_id || null,
      proposition,
      holder || 'human',
      status || 'working_belief',
      confidence !== undefined ? confidence : 0.75,
      supporting_evidence || '',
      counter_evidence || '',
      falsifier || ''
    );

    return NextResponse.json({ success: true, id: newId });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

// PRD Scenario 4: Non-destructive Belief Revision
export async function PATCH(request: Request) {
  try {
    const db = getDb();
    const body = await request.json();
    const { id, newProposition, newStatus, newConfidence, reasonForChange, workId } = body;

    if (!id) {
      return NextResponse.json({ success: false, error: 'Belief ID is required' }, { status: 400 });
    }

    // 1. Fetch current belief state
    const current = db.prepare('SELECT * FROM beliefs WHERE id = ?').get(id) as any;
    if (!current) {
      return NextResponse.json({ success: false, error: 'Belief not found' }, { status: 404 });
    }

    // 2. Insert immutable revision record
    const revId = `BREV-${Date.now()}`;
    db.prepare(`
      INSERT INTO belief_revisions (
        id, belief_id, previous_proposition, new_proposition, 
        previous_status, new_status, previous_confidence, new_confidence, 
        reason_for_change, work_id
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      revId,
      id,
      current.proposition,
      newProposition || current.proposition,
      current.status,
      newStatus || current.status,
      current.confidence,
      newConfidence !== undefined ? newConfidence : current.confidence,
      reasonForChange || 'Refined during epistemic sparring',
      workId || null
    );

    // 3. Update belief current state with updated_at timestamp
    db.prepare(`
      UPDATE beliefs
      SET proposition = ?, status = ?, confidence = ?, updated_at = datetime('now')
      WHERE id = ?
    `).run(
      newProposition || current.proposition,
      newStatus || current.status,
      newConfidence !== undefined ? newConfidence : current.confidence,
      id
    );

    return NextResponse.json({
      success: true,
      revisionId: revId,
      message: 'Belief revised non-destructively; historical state preserved.',
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
