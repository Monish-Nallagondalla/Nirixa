import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const db = getDb();
    const { searchParams } = new URL(request.url);
    const status = searchParams.get('status');

    let query = 'SELECT * FROM discoveries';
    const params: any[] = [];

    if (status) {
      query += ' WHERE status = ?';
      params.push(status);
    }
    query += ' ORDER BY confidence DESC, created_at DESC';

    const discoveries = db.prepare(query).all(...params) as any[];

    // Parse objects_involved
    const formatted = discoveries.map((d) => ({
      ...d,
      objectsInvolved: d.objects_involved ? JSON.parse(d.objects_involved) : [],
    }));

    return NextResponse.json({ success: true, data: formatted });
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
      UPDATE discoveries 
      SET status = ?
      WHERE id = ?
    `).run(status, id);

    return NextResponse.json({ success: true });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
