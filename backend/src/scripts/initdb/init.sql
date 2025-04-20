\c app
CREATE EXTENSION postgis;

DROP FUNCTION IF EXISTS public.get_dataset_tile(text,integer,integer,integer);
CREATE OR REPLACE FUNCTION public.get_dataset_tile(
    relation text,
    z integer,
    x integer,
    y integer
) RETURNS bytea
LANGUAGE plpgsql
AS $$
DECLARE
    tile bytea;
BEGIN
    EXECUTE format(
        $f$
        WITH mvtgeom AS (
            SELECT ST_AsMVTGeom(
                       ST_Transform(geom, 3857),
                       ST_TileEnvelope(%s, %s, %s),
                       4096,
                       0,
                       true
                   ) AS geom
			,ogc_fid AS id
			,*
            FROM %s
            WHERE ST_Intersects(
                ST_Transform(geom, 3857),
                ST_TileEnvelope(%s, %s, %s)
            )
        )
        SELECT ST_AsMVT(mvtgeom, 'dataset', 4096, 'geom', 'id') FROM mvtgeom
        $f$,
        z, x, y,
        quote_ident(relation),
        z, x, y
    ) INTO tile;

    IF tile IS NULL OR length(tile) = 0 THEN
        RETURN NULL;
    END IF;

    RETURN tile;
END;
$$;

CREATE DATABASE data;
\c data
CREATE EXTENSION postgis;