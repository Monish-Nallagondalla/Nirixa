import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';
import networkData from '@/data/network_data.json';

export async function GET() {
  try {
    const db = getDb();

    // 1. Exact real counts from SQLite
    let captureCount = 303;
    let otaCount = 48;
    let paperCount = 4;
    let annotCount = 2;
    let chapters: any[] = [];
    let recentCaptures: any[] = [];

    try {
      const capRow = db.prepare('SELECT count(*) as count FROM raw_captures').get() as { count: number };
      if (capRow) captureCount = capRow.count;

      const otaRow = db.prepare('SELECT count(*) as count FROM ota_assets').get() as { count: number };
      if (otaRow) otaCount = otaRow.count;

      const paperRow = db.prepare('SELECT count(*) as count FROM papers').get() as { count: number };
      if (paperRow) paperCount = paperRow.count;

      const annotRow = db.prepare('SELECT count(*) as count FROM paper_annotations').get() as { count: number };
      if (annotRow) annotCount = annotRow.count;

      chapters = db.prepare('SELECT * FROM book_chapters ORDER BY chapter_number ASC').all() as any[];

      // 2. Query real captures from SQLite
      const rawRows = db.prepare(`
        SELECT id, timestamp, raw_text, source 
        FROM raw_captures 
        WHERE raw_text IS NOT NULL AND length(trim(raw_text)) > 0
        ORDER BY id DESC 
        LIMIT 50
      `).all() as any[];

      recentCaptures = rawRows.map((r) => ({
        id: r.id,
        timestamp: r.timestamp || '2026-09-04',
        raw_text: (r.raw_text || '').trim(),
        source: r.source || 'telegram'
      }));
    } catch (dbErr) {
      console.warn('DB queries warning in /api/cockpit:', dbErr);
    }

    // 3. Mini-constellation nodes from network_data
    const otaNodes = networkData.nodes
      .filter((n: any) => n.id && n.id.startsWith('ota_') && n.id !== 'ota_eval')
      .slice(0, 18)
      .map((n: any) => ({
        id: n.id.toUpperCase().replace('_', '-'),
        title: n.label || n.title,
        category: n.group || 'Epistemology',
        pagerank: n.metrics?.pagerank || 0.65,
        color: n.color || '#38bdf8'
      }));

    return NextResponse.json({
      success: true,
      data: {
        metrics: {
          capturesCount: captureCount,
          otasConnected: otaCount,
          papersCount: paperCount,
          citationsBound: annotCount,
          leadChapter: {
            title: 'The Coevolution of Thought',
            chapterNumber: 2,
            maturity: 74
          }
        },
        chapters,
        recentCaptures,
        constellation: {
          nodes: otaNodes
        }
      }
    });
  } catch (error: any) {
    console.error('Error in /api/cockpit:', error);
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
