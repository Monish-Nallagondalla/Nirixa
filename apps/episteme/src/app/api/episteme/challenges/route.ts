import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);
    const status = searchParams.get('status');

    let query = `
      SELECT c.*, b.proposition as held_belief, b.confidence as belief_confidence, b.eo_id
      FROM challenges c
      LEFT JOIN beliefs b ON c.belief_id = b.id
    `;
    const params: any[] = [];

    if (status) {
      query += ' WHERE c.status = ?';
      params.push(status);
    }
    query += ' ORDER BY c.created_at DESC';

    const challenges = db.prepare(query).all(...params);
    return NextResponse.json({ success: true, data: challenges });
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
      UPDATE challenges 
      SET status = ?
      WHERE id = ?
    `).run(status, id);

    return NextResponse.json({ success: true });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
