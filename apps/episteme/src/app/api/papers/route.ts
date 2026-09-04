import { NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export async function GET() {
  try {
    const db = getDb();

    let papers = db.prepare('SELECT * FROM papers ORDER BY year DESC, title ASC').all() as any[];

    // If no papers yet in database, seed foundational PhD literature benchmarks
    if (papers.length === 0) {
      const samplePapers = [
        {
          id: 'paper-licklider-1960',
          title: 'Man-Computer Symbiosis',
          authors: 'J. C. R. Licklider',
          year: 1960,
          venue: 'IRE Transactions on Human Factors in Electronics',
          doi: '10.1109/THFE2.1960.4503259',
          abstract: 'Man-computer symbiosis is an expected development in cooperative interaction between men and electronic computers. It involves very close coupling among human and electronic members of the partnership.',
          file_path: 'data/papers/licklider_1960.pdf',
          file_hash: 'hash-licklider-1960',
          total_pages: 8,
          phd_rq_id: 'RQ-2'
        },
        {
          id: 'paper-engelbart-1962',
          title: 'Augmenting Human Intellect: A Conceptual Framework',
          authors: 'Douglas C. Engelbart',
          year: 1962,
          venue: 'Stanford Research Institute Summary Report',
          doi: '10.21236/AD0299834',
          abstract: 'By augmenting human intellect we mean increasing the capability of a man to approach a complex problem situation, to gain comprehension to suit his particular needs, and to derive solutions.',
          file_path: 'data/papers/engelbart_1962.pdf',
          file_hash: 'hash-engelbart-1962',
          total_pages: 134,
          phd_rq_id: 'RQ-1'
        },
        {
          id: 'paper-shannon-1948',
          title: 'A Mathematical Theory of Communication',
          authors: 'Claude E. Shannon',
          year: 1948,
          venue: 'The Bell System Technical Journal',
          doi: '10.1002/j.1538-7305.1948.tb01338.x',
          abstract: 'The fundamental problem of communication is that of reproducing at one point either exactly or approximately a message selected at another point.',
          file_path: 'data/papers/shannon_1948.pdf',
          file_hash: 'hash-shannon-1948',
          total_pages: 55,
          phd_rq_id: 'RQ-4'
        }
      ];

      const insertStmt = db.prepare(`
        INSERT OR IGNORE INTO papers (id, title, authors, year, venue, doi, abstract, file_path, file_hash, total_pages, phd_rq_id)
        VALUES (@id, @title, @authors, @year, @venue, @doi, @abstract, @file_path, @file_hash, @total_pages, @phd_rq_id)
      `);

      for (const p of samplePapers) {
        insertStmt.run(p);
      }

      // Also seed sample annotations
      const sampleAnnotations = [
        {
          id: 'annot-1',
          paper_id: 'paper-licklider-1960',
          page_number: 4,
          highlighted_text: 'human brains and computing machines will be coupled together very tightly, and that the resulting partnership will think as no human brain has ever thought.',
          note: 'Direct empirical anchor for OTA-014 (Cognitive Morphology) and PhD RQ-2.',
          annotation_type: 'ota_anchor',
          linked_ota_id: 'OTA-014'
        },
        {
          id: 'annot-2',
          paper_id: 'paper-engelbart-1962',
          page_number: 18,
          highlighted_text: 'we mean augmenting the total cognitive capacity of the human system through structured artifact scaffolding.',
          note: 'Supports Socratic agent debate hypothesis (OTA-010).',
          annotation_type: 'ota_anchor',
          linked_ota_id: 'OTA-010'
        }
      ];

      const insertAnnot = db.prepare(`
        INSERT OR IGNORE INTO paper_annotations (id, paper_id, page_number, highlighted_text, note, annotation_type, linked_ota_id)
        VALUES (@id, @paper_id, @page_number, @highlighted_text, @note, @annotation_type, @linked_ota_id)
      `);

      for (const a of sampleAnnotations) {
        insertAnnot.run(a);
      }

      papers = db.prepare('SELECT * FROM papers ORDER BY year DESC, title ASC').all() as any[];
    }

    const annotations = db.prepare('SELECT * FROM paper_annotations ORDER BY created_at DESC').all() as any[];

    return NextResponse.json({
      success: true,
      data: {
        papers,
        annotations
      }
    });
  } catch (error: any) {
    console.error('Error in /api/papers:', error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const db = getDb();

    if (body.action === 'add_annotation') {
      const { paperId, pageNumber, highlightedText, note, annotationType, linkedOtaId } = body;
      const id = 'annot-' + Date.now();

      db.prepare(`
        INSERT INTO paper_annotations (id, paper_id, page_number, highlighted_text, note, annotation_type, linked_ota_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `).run(id, paperId, pageNumber || 1, highlightedText, note || '', annotationType || 'note', linkedOtaId || null);

      return NextResponse.json({ success: true, id });
    }

    return NextResponse.json({ success: false, error: 'Unknown action' }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
