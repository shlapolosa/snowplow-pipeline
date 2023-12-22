# Kafka to Postgres simple scala storage loader

## Getting Started

This Code is ready to use Storage loader which save atmoic data. for custom events or custom dimension you need to add to this code and you know how !

# Notel! Make sure you're using Java 8

### Build 

```
mvn clean install 
```

### To Run from command line after making changes

```
java -cp target/scala-maven-0.1-SNAPSHOT-jar-with-dependencies.jar com.digikala.Kafka2Storage
```

### To create stand-alone image

```
docker build -t scala-maven-app .  
```
followed by
```
docker run -it --rm --name my-running-app scala-maven-app   
```

## Note

the command above will fail when ran as stand alone since it wont be able to connect to kafka. current config assumes running in with a cluster available


### Configuration

In the config.conf file you can adjust your Ne04j storage loader with cofiguration that you want.

Firstly, Set you Kafka connection information in below. It is better to set specific consumer id in order to Kafka manages offsets. you can seperate yor brokers just by comma !

```
kafka{
  brokers = "broker1,broker2"
  topic = "someTopic"
  consumerGroupId = "someConsumerGroupID"
}
```

Secondly, You should set you Postgres Connection information. In numberOfThread field you should mention that how many thread you need to start.

```
postgres{
  driver = "org.postgresql.Driver"
  url = "jdbc:postgresql://ip:port/databaseName"
  username = "########"
  password = "#########"
  groupid = "GroupID"
  numberOfThreads = 1
}

```

## Contributing

This Program is Coded by [Digikala](https://Digikala.com) Data Science Team.

## RoadMap

we decided to refactor our code and design in ib actor model and implement by akka, but at this time it is not reqired.

## Prep

run the sql queries against the database defined in the conf file before starting the process, otherwise it will fail when trying to process the records with messages like 

'relation events does not exist'

this will try to write to iglu-postgres:5432/igludb?currentSchema=atomic

---
```
create table atomic.events
(
    app_id                   varchar(255),
    platform                 varchar(255),
    etl_tstamp               timestamp,
    collector_tstamp         timestamp    not null,
    dvce_created_tstamp      timestamp,
    event                    varchar(128),
    event_id                 varchar(50),
    txn_id                   integer,
    name_tracker             varchar(128),
    v_tracker                varchar(100),
    v_collector              varchar(100) not null,
    v_etl                    varchar(100) not null,
    user_id                  varchar(255),
    user_ipaddress           varchar(128),
    user_fingerprint         varchar(50),
    domain_userid            varchar(128),
    domain_sessionidx        integer,
    network_userid           varchar(128),
    geo_country              char(2),
    geo_region               char(3),
    geo_city                 varchar(75),
    geo_zipcode              varchar(15),
    geo_latitude             double precision,
    geo_longitude            double precision,
    geo_region_name          varchar(100),
    ip_isp                   varchar(100),
    ip_organization          varchar(100),
    ip_domain                varchar(100),
    ip_netspeed              varchar(100),
    page_url                 varchar(4096),
    page_title               varchar(2000),
    page_referrer            varchar(4096),
    page_urlscheme           varchar(16),
    page_urlhost             varchar(255),
    page_urlport             integer,
    page_urlpath             varchar(3000),
    page_urlquery            varchar(6000),
    page_urlfragment         varchar(3000),
    refr_urlscheme           varchar(16),
    refr_urlhost             varchar(255),
    refr_urlport             integer,
    refr_urlpath             varchar(6000),
    refr_urlquery            varchar(6000),
    refr_urlfragment         varchar(3000),
    refr_medium              varchar(25),
    refr_source              varchar(50),
    refr_term                varchar(255),
    mkt_medium               varchar(255),
    mkt_source               varchar(255),
    mkt_term                 varchar(255),
    mkt_content              varchar(500),
    mkt_campaign             varchar(255),
    se_category              varchar(1000),
    se_action                varchar(1000),
    se_label                 varchar(1000),
    se_property              varchar(1000),
    se_value                 double precision,
    tr_orderid               varchar(255),
    tr_affiliation           varchar(255),
    tr_total                 double precision,
    tr_tax                   double precision,
    tr_shipping              double precision,
    tr_city                  varchar(255),
    tr_state                 varchar(255),
    tr_country               varchar(255),
    ti_orderid               varchar(255),
    ti_sku                   varchar(255),
    ti_name                  varchar(255),
    ti_category              varchar(255),
    ti_price                 double precision,
    ti_quantity              integer,
    pp_xoffset_min           integer,
    pp_xoffset_max           integer,
    pp_yoffset_min           integer,
    pp_yoffset_max           integer,
    useragent                varchar(1000),
    br_name                  varchar(50),
    br_family                varchar(50),
    br_version               varchar(50),
    br_type                  varchar(50),
    br_renderengine          varchar(50),
    br_lang                  varchar(255),
    br_features_pdf          boolean,
    br_features_flash        boolean,
    br_features_java         boolean,
    br_features_director     boolean,
    br_features_quicktime    boolean,
    br_features_realplayer   boolean,
    br_features_windowsmedia boolean,
    br_features_gears        boolean,
    br_features_silverlight  boolean,
    br_cookies               boolean,
    br_colordepth            varchar(12),
    br_viewwidth             integer,
    br_viewheight            integer,
    os_name                  varchar(50),
    os_family                varchar(50),
    os_manufacturer          varchar(50),
    os_timezone              varchar(50),
    dvce_type                varchar(50),
    dvce_ismobile            boolean,
    dvce_screenwidth         integer,
    dvce_screenheight        integer,
    doc_charset              varchar(128),
    doc_width                integer,
    doc_height               integer,
    tr_currency              char(3),
    tr_total_base            double precision,
    tr_tax_base              double precision,
    tr_shipping_base         double precision,
    ti_currency              char(3),
    ti_price_base            double precision,
    base_currency            char(3),
    geo_timezone             varchar(64),
    mkt_clickid              varchar(128),
    mkt_network              varchar(64),
    etl_tags                 varchar(500),
    dvce_sent_tstamp         timestamp,
    refr_domain_userid       varchar(128),
    refr_dvce_tstamp         timestamp,
    domain_sessionid         varchar(128),
    derived_tstamp           timestamp,
    event_vendor             varchar(1000),
    event_name               varchar(1000),
    event_format             varchar(128),
    event_version            varchar(128),
    event_fingerprint        varchar(128),
    true_tstamp              timestamp
);


create table atomic.com_snowplowanalytics_snowplow_ua_parser_context_1
(
    schema_vendor     varchar(128),
    schema_name       varchar(128),
    schema_format     varchar(128),
    schema_version    varchar(128),
    root_id           uuid,
    root_tstamp       timestamp,
    device_family     varchar(4096) not null,
    os_family         varchar(4096) not null,
    useragent_family  varchar(4096) not null,
    os_major          varchar(4096),
    os_minor          varchar(4096),
    os_patch          varchar(4096),
    os_patch_minor    varchar(4096),
    os_version        varchar(4096),
    useragent_major   varchar(4096),
    useragent_minor   varchar(4096),
    useragent_patch   varchar(4096),
    useragent_version varchar(4096)
);


create table atomic.org_w3_performance_timing_1
(
    schema_vendor                  varchar(128),
    schema_name                    varchar(128),
    schema_format                  varchar(128),
    schema_version                 varchar(128),
    root_id                        uuid,
    root_tstamp                    timestamp,
    chrome_first_paint             bigint,
    connect_end                    bigint,
    connect_start                  bigint,
    dom_complete                   bigint,
    dom_content_loaded_event_end   bigint,
    dom_content_loaded_event_start bigint,
    dom_interactive                bigint,
    dom_loading                    bigint,
    domain_lookup_end              bigint,
    domain_lookup_start            bigint,
    fetch_start                    bigint,
    load_event_end                 bigint,
    load_event_start               bigint,
    ms_first_paint                 bigint,
    navigation_start               bigint,
    proxy_end                      bigint,
    proxy_start                    bigint,
    redirect_end                   bigint,
    redirect_start                 bigint,
    request_end                    bigint,
    request_start                  bigint,
    response_end                   bigint,
    response_start                 bigint,
    secure_connection_start        bigint,
    unload_event_end               bigint,
    unload_event_start             bigint
);


create table atomic.com_snowplowanalytics_snowplow_link_click_1
(
    schema_vendor   varchar(128),
    schema_name     varchar(128),
    schema_format   varchar(128),
    schema_version  varchar(128),
    root_id         uuid,
    root_tstamp     timestamp,
    target_url      varchar(4096) not null,
    element_classes jsonb,
    element_id      varchar(4096),
    element_target  varchar(4096),
    element_content varchar(4096)
);


create table atomic.nl_basjes_yauaa_context_1
(
    schema_vendor                        varchar(128),
    schema_name                          varchar(128),
    schema_format                        varchar(128),
    schema_version                       varchar(128),
    root_id                              uuid,
    root_tstamp                          timestamp,
    device_class                         varchar(21) not null,
    agent_build                          varchar(100),
    agent_class                          varchar(17),
    agent_information_email              varchar(4096),
    agent_information_url                varchar(4096),
    agent_language                       varchar(50),
    agent_language_code                  varchar(20),
    agent_name                           varchar(100),
    agent_name_version                   varchar(200),
    agent_name_version_major             varchar(120),
    agent_security                       varchar(15),
    agent_uuid                           varchar(4096),
    agent_version                        varchar(100),
    agent_version_major                  varchar(20),
    anonymized                           varchar(4096),
    carrier                              varchar(4096),
    device_brand                         varchar(50),
    device_cpu                           varchar(50),
    device_cpu_bits                      varchar(20),
    device_firmware_version              varchar(100),
    device_name                          varchar(100),
    device_version                       varchar(100),
    facebook_carrier                     varchar(4096),
    facebook_device_class                varchar(1024),
    facebook_device_name                 varchar(1024),
    facebook_device_version              varchar(4096),
    facebook_fbop                        varchar(4096),
    facebook_fbss                        varchar(4096),
    facebook_operating_system_name       varchar(4096),
    facebook_operating_system_version    varchar(4096),
    g_sa_installation_id                 varchar(4096),
    hacker_attack_vector                 varchar(4096),
    hacker_toolkit                       varchar(4096),
    i_e_compatibility_name_version       varchar(50),
    i_e_compatibility_name_version_major varchar(70),
    i_e_compatibility_version            varchar(100),
    i_e_compatibility_version_major      varchar(50),
    kobo_affiliate                       varchar(4096),
    kobo_platform_id                     varchar(4096),
    layout_engine_build                  varchar(100),
    layout_engine_class                  varchar(10),
    layout_engine_name                   varchar(100),
    layout_engine_name_version           varchar(150),
    layout_engine_name_version_major     varchar(120),
    layout_engine_version                varchar(50),
    layout_engine_version_major          varchar(20),
    network_type                         varchar(4096),
    operating_system_class               varchar(12),
    operating_system_name                varchar(100),
    operating_system_name_version        varchar(150),
    operating_system_version             varchar(50),
    operating_system_version_build       varchar(100),
    webview_app_name                     varchar(4096),
    webview_app_name_version_major       varchar(50),
    webview_app_version                  varchar(4096),
    webview_app_version_major            varchar(50),
    operating_system_name_version_major  varchar(4096),
    operating_system_version_major       varchar(4096)
);


create table atomic.com_snowplowanalytics_snowplow_web_page_1
(
    schema_vendor  varchar(128),
    schema_name    varchar(128),
    schema_format  varchar(128),
    schema_version varchar(128),
    root_id        uuid,
    root_tstamp    timestamp,
    id             varchar(4096) not null
);


```