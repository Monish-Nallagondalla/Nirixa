import { NextResponse } from 'next/server';
import networkData from '@/data/network_data.json';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('q')?.toLowerCase() || '';
    const category = searchParams.get('category')?.toLowerCase() || '';

    // Filter only OTAs from the 76 nodes
    let otaNodes = networkData.nodes
      .filter((n: any) => n.type === 'ota')
      .map((n: any) => ({
        id: n.ota_num || n.id,
        nodeId: n.id,
        title: n.label,
        description: n.properties?.description || n.label,
        thesis: n.properties?.description || n.label,
        category: n.group?.replace(/^Pillar \d+:\s*/, '') || 'Epistemology',
        pillar: n.group,
        color: n.color,
        pagerank: n.metrics?.pagerank || 0.5,
        authority_score: n.metrics?.authority_score || 25,
        degree: n.degree || 3
      }));

    if (search) {
      otaNodes = otaNodes.filter(o =>
        o.id.toLowerCase().includes(search) ||
        o.title.toLowerCase().includes(search) ||
        o.description.toLowerCase().includes(search)
      );
    }

    if (category && category !== 'all') {
      otaNodes = otaNodes.filter(o =>
        o.category.toLowerCase().includes(category) ||
        o.pillar.toLowerCase().includes(category)
      );
    }

    // Sort by PageRank descending
    otaNodes.sort((a, b) => b.pagerank - a.pagerank);

    return NextResponse.json({
      success: true,
      total: otaNodes.length,
      data: {
        otas: otaNodes,
        edges: networkData.links
      }
    });
  } catch (error: any) {
    console.error('Error in /api/otas:', error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
