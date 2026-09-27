import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);
    const eoId = searchParams.get('eoId');
    const status = searchParams.get('status');

    let query = 'SELECT * FROM questions';
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

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    query += ' ORDER BY updated_at DESC';

    const questions = db.prepare(query).all(...params);
    return NextResponse.json({ success: true, data: questions });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const db = getDb();
    const body = await request.json();
    const { id, eo_id, text, priority, provenance } = body;

    const newId = id || `Q-${Math.floor(100 + Math.random() * 900)}`;
    db.prepare(`
      INSERT OR REPLACE INTO questions (id, eo_id, text, priority, provenance)
      VALUES (?, ?, ?, ?, ?)
    `).run(newId, eo_id || null, text, priority || 'high', provenance || 'User Input');

    return NextResponse.json({ success: true, id: newId });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  try {
    const db = getDb();
    const body = await request.json();
    const { id, status } = body;

    db.prepare(`
      UPDATE questions 
      SET status = ?, updated_at = datetime('now')
      WHERE id = ?
    `).run(status, id);

    return NextResponse.json({ success: true });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
