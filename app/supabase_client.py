import os
import logging
import reflex as rx
from supabase import create_client, Client

"""
This file initializes the Supabase client for storage operations.
Database operations are handled by the Reflex ORM.

-- Supabase Setup required for this app:
-- 1. Create a public bucket named 'media' in Supabase Storage.
-- 2. The 'posts' table is managed by the Reflex ORM (see app/models.py).
"""
try:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        print("Supabase credentials not found. Running in offline mode.")
        db: Client | None = None
    else:
        db: Client | None = create_client(supabase_url, supabase_key)
except Exception as e:
    logging.exception(f"Error: {e}")
    print(f"Error initializing Supabase client: {e}")
    db: Client | None = None