import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');
    const status = searchParams.get('status');

    let query = 'SELECT * FROM epistemic_objects';
    const params: any[] = [];
    const conditions: string[] = [];

    if (category) {
      conditions.push('category = ?');
      params.push(category);
    }
    if (status) {
      conditions.push('status = ?');
      params.push(status);
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    query += ' ORDER BY maturity DESC';

    const eos = db.prepare(query).all(...params) as any[];

    // Enrich with attached counts
    const enrichedEos = eos.map((eo) => {
      const qCount = db.prepare('SELECT count(*) as count FROM questions WHERE eo_id = ?').get(eo.id) as any;
      const bCount = db.prepare('SELECT count(*) as count FROM beliefs WHERE eo_id = ?').get(eo.id) as any;
      const eCount = db.prepare('SELECT count(*) as count FROM evidence WHERE eo_id = ?').get(eo.id) as any;

      return {
        ...eo,
        questionsCount: qCount ? qCount.count : 0,
        beliefsCount: bCount ? bCount.count : 0,
        evidenceCount: eCount ? eCount.count : 0,
      };
    });

    return NextResponse.json({ success: true, data: enrichedEos });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const db = getDb();
    const body = await request.json();
    const { id, title, description, category, maturity, provenance } = body;

    const newId = id || `EO-${Math.floor(100 + Math.random() * 900)}`;
    db.prepare(`
      INSERT INTO epistemic_objects (id, title, description, category, maturity, provenance)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(newId, title, description || '', category || 'Epistemology', maturity || 50, provenance || 'Manual Creation');

    return NextResponse.json({ success: true, id: newId });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
