import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

let dbInstance: Database.Database | null = null;

export function getDb(): Database.Database {
  if (dbInstance) {
    return dbInstance;
  }

  const primaryPath = path.resolve(/*turbopackIgnore: true*/ process.cwd(), process.env.DATABASE_PATH || '../../system/data/nirixa.db');
  const fallbackPath = path.resolve(/*turbopackIgnore: true*/ process.cwd(), 'system/data/nirixa.db');

  let dbPath = primaryPath;
  if (!fs.existsSync(primaryPath) && fs.existsSync(fallbackPath)) {
    dbPath = fallbackPath;
  }

  dbInstance = new Database(dbPath, {
    // verbose: console.log,
  });

  // Enable WAL mode for high concurrency and sub-millisecond reads
  dbInstance.pragma('journal_mode = WAL');
  dbInstance.pragma('synchronous = NORMAL');

  // Initialize PRD Epistemic tables & seeds
  try {
    const { initializeEpistemicSchema } = require('./schema');
    initializeEpistemicSchema(dbInstance);
  } catch (schemaErr) {
    console.warn('Epistemic schema init warning:', schemaErr);
  }

  return dbInstance;
}

export default getDb;
