CREATE SCHEMA IF NOT EXISTS atomic;

CREATE TABLE atomic.events (
    app_id TEXT,
    platform TEXT,
    etl_tstamp TIMESTAMP,
    collector_tstamp TIMESTAMP,
    dvce_created_tstamp TIMESTAMP,
    event TEXT,
    event_id UUID,
    txn_id UUID,
    name_tracker TEXT,
    v_tracker TEXT,
    v_collector TEXT,
    v_etl TEXT,
    user_fingerprint TEXT,
    user_ipaddress TEXT,
    domain_userid TEXT,
    domain_sessionidx CHARACTER VARYING,
    network_userid TEXT,
    geo_country TEXT,
    geo_region TEXT,
    geo_city TEXT,
    geo_zipcode TEXT,
    geo_latitude FLOAT,
    geo_longitude FLOAT,
    geo_region_name TEXT,
    ip_isp TEXT,
    ip_organization TEXT,
    ip_domain TEXT,
    ip_netspeed TEXT,
    page_url TEXT,
    page_title TEXT,
    page_referrer TEXT,
    page_urlscheme TEXT,
    page_urlhost TEXT,
    page_urlport INT,
    page_urlpath TEXT,
    page_urlquery TEXT,
    page_urlfragment TEXT,
    refr_urlscheme TEXT,
    refr_urlhost TEXT,
    refr_urlport INT,
    refr_urlpath TEXT,
    refr_urlquery TEXT,
    refr_urlfragment TEXT,
    refr_medium TEXT,
    refr_source TEXT,
    refr_term TEXT,
    mkt_medium TEXT,
    mkt_source TEXT,
    mkt_term TEXT,
    mkt_content TEXT,
    mkt_campaign TEXT,
    contexts TEXT,
    se_category TEXT,
    se_action TEXT,
    se_label TEXT,
    se_property TEXT,
    se_value FLOAT,
    unstruct_event TEXT,
    tr_orderid TEXT,
    tr_affiliation TEXT,
    tr_total FLOAT,
    tr_tax FLOAT,
    tr_shipping FLOAT,
    tr_city TEXT,
    tr_state TEXT,
    tr_country TEXT,
    ti_orderid TEXT,
    ti_sku TEXT,
    ti_name TEXT,
    ti_category TEXT,
    ti_price FLOAT,
    ti_quantity INT,
    pp_xoffset_min FLOAT,
    pp_xoffset_max FLOAT,
    pp_yoffset_min FLOAT,
    pp_yoffset_max FLOAT,
    useragent TEXT,
    br_name TEXT,
    br_family TEXT,
    br_version TEXT,
    br_type TEXT,
    br_renderengine TEXT,
    br_lang TEXT,
    br_features_pdf CHARACTER VARYING,
    br_features_flash BOOLEAN,
    br_features_java BOOLEAN,
    br_features_director BOOLEAN,
    br_features_quicktime BOOLEAN,
    br_features_realplayer BOOLEAN,
    br_features_windowsmedia BOOLEAN,
    br_features_gears BOOLEAN,
    br_features_silverlight BOOLEAN,
    br_cookies BOOLEAN,
    br_colordepth TEXT,
    br_viewwidth CHARACTER VARYING,
    br_viewheight INT,
    os_name TEXT,
    os_family TEXT,
    os_manufacturer TEXT,
    os_timezone TEXT,
    dvce_type TEXT,
    dvce_ismobile BOOLEAN,
    dvce_screenwidth INT,
    dvce_screenheight INT,
    doc_charset TEXT,
    doc_width CHARACTER VARYING,
    doc_height INT,
    tr_currency TEXT,
    tr_total_base FLOAT,
    tr_tax_base FLOAT,
    tr_shipping_base FLOAT,
    ti_currency TEXT,
    ti_price_base FLOAT,
    base_currency TEXT,
    geo_timezone TEXT,
    mkt_clickid TEXT,
    mkt_network TEXT,
    etl_tags TEXT,
    dvce_sent_tstamp TIMESTAMP,
    refr_domain_userid TEXT,
    refr_device_tstamp TIMESTAMP,
    domain_sessionid TEXT,
    derived_tstamp TIMESTAMP WITHOUT TIME ZONE,
    event_vendor TEXT,
    event_name TEXT,
    event_format TEXT,
    event_version TEXT,
    event_fingerprint TEXT,
    true_tstamp TIMESTAMP WITHOUT TIME ZONE,
    -- Additional fields to make up to 130 columns
    custom_field1 TEXT,
    custom_field2 TEXT,
    custom_field3 TEXT,
    custom_field4 TEXT,
    custom_field5 TEXT,
    custom_field6 TEXT,
    custom_field7 TEXT,
    custom_field8 TEXT,
    custom_field9 TEXT,
    custom_field10 TEXT,
    custom_field11 TEXT,
    custom_field12 TEXT,
    custom_field13 TEXT,
    custom_field14 TEXT,
    custom_field15 TEXT,
    custom_field16 TEXT,
    custom_field17 TEXT,
    custom_field18 TEXT,
    custom_field19 TEXT,
    custom_field20 TEXT
);
