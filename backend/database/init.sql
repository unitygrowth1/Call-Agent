# PostgreSQL Database Initialization

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector"; -- For pgvector if using

-- Create schema for application
CREATE SCHEMA IF NOT EXISTS public;

-- Set search path
SET search_path TO public;

-- Create initial indexes
CREATE COLLATION IF NOT EXISTS "und-x-icu" (provider = icu, locale = 'und');

-- Grant privileges
GRANT USAGE ON SCHEMA public TO postgres;
GRANT CREATE ON SCHEMA public TO postgres;

-- Note: All table definitions are in migrations (alembic)
-- This file just ensures the database is ready
