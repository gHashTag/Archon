# Vercel Database Setup Instructions

## Problem

The Vercel deployment is failing with 500 errors because the Supabase database hasn't been initialized with the required schema.

## Solution

Run the complete database setup script in Supabase SQL Editor.

## Steps

### 1. Open Supabase Dashboard

Navigate to: https://supabase.com/dashboard/project/yuukfqcsdhkyxegfwlcb

### 2. Open SQL Editor

- Click "SQL Editor" in the left sidebar
- Or go directly to: https://supabase.com/dashboard/project/yuukfqcsdhkyxegfwlcb/sql/new

### 3. Run Complete Setup Script

1. Open the file `/Users/playra/archon/migration/complete_setup.sql` in your local editor
2. Copy all contents (1375 lines)
3. Paste into Supabase SQL Editor
4. Click "Run" button (or press Cmd+Enter)

This script will create:
- ✅ All required extensions (vector, pgcrypto, pg_trgm)
- ✅ `archon_settings` table with configuration
- ✅ Knowledge base tables (`archon_sources`, `archon_crawled_pages`, `archon_code_examples`)
- ✅ Projects tables (`archon_projects`, `archon_tasks`, etc.)
- ✅ Search functions for RAG operations
- ✅ RLS policies for security

### 4. Verify Schema

After running the migration, verify it worked:

```sql
-- Check that archon_settings table exists and has data
SELECT COUNT(*) FROM archon_settings;
-- Should return 30+ rows

-- Check all main tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name LIKE 'archon_%'
ORDER BY table_name;
-- Should return: archon_code_examples, archon_crawled_pages, archon_migrations,
-- archon_page_metadata, archon_project_sources, archon_projects, archon_prompts,
-- archon_settings, archon_sources, archon_tasks, archon_document_versions
```

### 5. Test Vercel Deployment

Once the database is initialized, test the Vercel deployment:

```bash
# Check health endpoint
curl https://archon-fraj8878h-ghashtag.vercel.app/api/health

# Expected response:
{
  "status": "healthy",
  "service": "archon-backend",
  "timestamp": "2025-01-18T...",
  "ready": true,
  "credentials_loaded": true,
  "schema_valid": true
}
```

## Why This Approach?

1. **Safer**: Supabase SQL Editor handles large migrations better than API calls
2. **Transactional**: If any part fails, you'll see exactly which line
3. **Recommended**: This is Supabase's official way to run migrations
4. **Interactive**: You can see results immediately

## Alternative: Run via Supabase CLI

If you prefer command line:

```bash
# Install Supabase CLI if needed
brew install supabase/tap/supabase

# Link to your project
supabase link --project-ref yuukfqcsdhkyxegfwlcb

# Run migration
supabase db push --include-all
```

## After Database Setup

Once the database is initialized, the Vercel deployment should work properly:

- ✅ Backend will initialize without errors
- ✅ All API endpoints will return proper responses
- ✅ Frontend will connect successfully

## Environment Variables Already Set

These are already configured in Vercel (no action needed):

- `SUPABASE_URL`: https://yuukfqcsdhkyxegfwlcb.supabase.co
- `SUPABASE_SERVICE_KEY`: (encrypted in Vercel)
- `OPENAI_API_KEY`: (encrypted in Vercel)

## Next Steps

After database setup:
1. Test health endpoint: `curl https://archon-fraj8878h-ghashtag.vercel.app/api/health`
2. Test frontend: https://archon-fraj8878h-ghashtag.vercel.app
3. Check API docs: https://archon-fraj8878h-ghashtag.vercel.app/api/docs

---

**TL;DR**: Copy `migration/complete_setup.sql` → Paste in Supabase SQL Editor → Click Run
