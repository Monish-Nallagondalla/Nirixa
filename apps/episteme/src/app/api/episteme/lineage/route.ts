import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);
    const eoId = searchParams.get('eoId') || 'EO-001';

    // 1. Fetch EO
    const eo = db.prepare('SELECT * FROM epistemic_objects WHERE id = ?').get(eoId) as any;

    if (!eo) {
      return NextResponse.json({ success: false, error: 'Epistemic Object not found' }, { status: 404 });
    }

    // 2. Fetch associated Questions
    const questions = db.prepare('SELECT * FROM questions WHERE eo_id = ? ORDER BY priority DESC').all(eoId);

    // 3. Fetch associated Beliefs
    const beliefs = db.prepare('SELECT * FROM beliefs WHERE eo_id = ? ORDER BY confidence DESC').all(eoId);

    // 4. Fetch associated Evidence
    const evidence = db.prepare('SELECT * FROM evidence WHERE eo_id = ? ORDER BY strength DESC').all(eoId);

    // 5. Fetch associated Connections
    const connections = db.prepare(`
      SELECT * FROM connections 
      WHERE source_id = ? OR target_id = ?
    `).all(eoId, eoId);

    // 6. Fetch linked book chapters or outputs
    const chapters = db.prepare(`
      SELECT * FROM book_chapters 
      WHERE synopsis LIKE ? OR title LIKE ?
    `).all(`%${eoId}%`, `%${eo.title}%`);

    return NextResponse.json({
      success: true,
      data: {
        eo,
        questions,
        beliefs,
        evidence,
        connections,
        chapters,
        lineageSummary: `${eo.id} → ${questions.length} Questions → ${evidence.length} Evidence Anchors → ${beliefs.length} Beliefs`,
      },
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
