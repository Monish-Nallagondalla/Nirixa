import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET() {
  try {
    const db = getDb();
    const captures = db.prepare(`
      SELECT id, capture_type, title, raw_text, source, tags, created_at 
      FROM raw_captures 
      ORDER BY created_at DESC 
      LIMIT 20
    `).all() as any[];

    return NextResponse.json({
      success: true,
      data: captures
    });
  } catch (error: any) {
    console.error('Error in /api/friction:', error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
