CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL,
  sso_subject text UNIQUE NOT NULL,
  email text NOT NULL,
  display_name text NOT NULL,
  role text NOT NULL DEFAULT 'repartidor' CHECK (role IN ('admin','supervisor','analyst','auditor','repartidor')),
  password_hash text,
  password_salt text,
  active boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS guides (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), organization_id uuid NOT NULL, code varchar(12) NOT NULL,
  address text, zone text, price numeric(14,2) NOT NULL DEFAULT 0, status text NOT NULL DEFAULT 'available',
  UNIQUE (organization_id, code)
);
CREATE TABLE IF NOT EXISTS visits (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), organization_id uuid NOT NULL, guide_id uuid NOT NULL REFERENCES guides(id),
  user_id uuid REFERENCES users(id), status text NOT NULL, description text, zone text, price numeric(14,2) NOT NULL DEFAULT 0,
  visited_at timestamptz NOT NULL DEFAULT now(), location geography(Point,4326), gps_accuracy_m numeric, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS visits_location_gix ON visits USING GIST(location);
CREATE INDEX IF NOT EXISTS guides_org_code_idx ON guides(organization_id, code);
CREATE TABLE IF NOT EXISTS telemetry_events (
  id bigserial PRIMARY KEY, organization_id uuid NOT NULL, user_subject text, event_name text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb, created_at timestamptz NOT NULL DEFAULT now()
);
