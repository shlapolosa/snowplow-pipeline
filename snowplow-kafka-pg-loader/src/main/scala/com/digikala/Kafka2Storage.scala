package com.digikala

import java.io.File
import java.text.SimpleDateFormat
import java.util
import java.util.Properties
import com.snowplowanalytics.snowplow.analytics.scalasdk.json.EventTransformer
import com.typesafe.config.ConfigFactory
import net.liftweb.json._
import org.apache.kafka.clients.consumer.KafkaConsumer
import scalikejdbc._
import scala.collection.JavaConverters._
import org.apache.logging.log4j.scala.Logging


class PostgresLoader {

    val config = ConfigFactory.parseFile(new File("config.conf"))
    Class.forName(config.getString("postgres.driver"))
    ConnectionPool.singleton(config.getString("postgres.url"),config.getString("postgres.username"), config.getString("postgres.password"))
    implicit val session = AutoSession
    var timing : Boolean = false
    var performanceMap : Map[String,Any] = null


  def  save(jsonMap : Map[String,Any])={

    if(jsonMap.contains("contexts_org_w3_performance_timing_1"))
      {
         performanceMap =jsonMap.getOrElse("contexts_org_w3_performance_timing_1",null).asInstanceOf[List[Map[String,Any]]](0)
         timing = true
      }
    val dateFormat : SimpleDateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSS");
    var parsedDate_etl_tstamp : java.util.Date = dateFormat.parse(jsonMap.getOrElse("etl_tstamp", null).asInstanceOf[String].dropRight(1).replace('T', ' '))
    var timestamp_etl_tstamp :java.sql.Timestamp  = new java.sql.Timestamp(parsedDate_etl_tstamp.getTime())
    var parsedDate_collector_tstamp : java.util.Date = dateFormat.parse(jsonMap.getOrElse("collector_tstamp", null).asInstanceOf[String].dropRight(1).replace('T', ' '))
    var timestamp_collector_tstamp :java.sql.Timestamp  = new java.sql.Timestamp(parsedDate_collector_tstamp.getTime())
    var parsedDate_dvce_created_tstamp : java.util.Date = dateFormat.parse(jsonMap.getOrElse("dvce_created_tstamp", null).asInstanceOf[String].dropRight(1).replace('T', ' '))
    var timestamp_dvce_created_tstamp :java.sql.Timestamp  = new java.sql.Timestamp(parsedDate_dvce_created_tstamp.getTime())
    var parsedDate_dvce_sent_tstamp : java.util.Date = dateFormat.parse(jsonMap.getOrElse("dvce_sent_tstamp", null).asInstanceOf[String].dropRight(1).replace('T', ' '))
    var timestamp_dvce_sent_tstamp :java.sql.Timestamp  = new java.sql.Timestamp(parsedDate_dvce_sent_tstamp.getTime())
    var parsedDate_derived_tstamp : java.util.Date = dateFormat.parse(jsonMap.getOrElse("derived_tstamp", null).asInstanceOf[String].dropRight(1).replace('T', ' '))
    var timestamp_derived_tstamp :java.sql.Timestamp  = new java.sql.Timestamp(parsedDate_derived_tstamp.getTime())
    try{
        sql"insert into events values (${jsonMap.getOrElse("app_id",null)},${jsonMap.getOrElse("platform",null)},${timestamp_etl_tstamp},${timestamp_collector_tstamp},${timestamp_dvce_created_tstamp},${jsonMap.getOrElse("event",null)},${jsonMap.getOrElse("event_id",null)},${jsonMap.getOrElse("tnx_id",null)},${jsonMap.getOrElse("name_tracker",null)},${jsonMap.getOrElse("v_tracker",null)},${jsonMap.getOrElse("v_collector",null)},${jsonMap.getOrElse("v_etl",null)},${jsonMap.getOrElse("user_id",null)},${jsonMap.getOrElse("user_ipaddress",null)},${jsonMap.getOrElse("user_fingerprint",null)},${jsonMap.getOrElse("domain_userid",null)},${jsonMap.getOrElse("domain_sessionidx",null)},${jsonMap.getOrElse("network_userid",null)},${jsonMap.getOrElse("geo_country",null)},${jsonMap.getOrElse("geo_region",null)},${jsonMap.getOrElse("geo_city",null)},${jsonMap.getOrElse("geo_zipcode",null)},${jsonMap.getOrElse("geo_latitude",null)},${jsonMap.getOrElse("geo_longitude",null)},${jsonMap.getOrElse("geo_region_name",null)},${jsonMap.getOrElse("ip_isp",null)},${jsonMap.getOrElse("ip_organization",null)},${jsonMap.getOrElse("ip_domain",null)},${jsonMap.getOrElse("ip_netspeed",null)},${jsonMap.getOrElse("page_url",null)},${jsonMap.getOrElse("page_title",null)},${jsonMap.getOrElse("page_referrer",null)},${jsonMap.getOrElse("page_urlscheme",null)},${jsonMap.getOrElse("page_urlhost",null)},${jsonMap.getOrElse("page_urlport",null)},${jsonMap.getOrElse("page_urlpath",null)},${jsonMap.getOrElse("page_urlquery",null)},${jsonMap.getOrElse("page_urlfragment",null)},${jsonMap.getOrElse("refr_urlscheme",null)},${jsonMap.getOrElse("refr_urlhost",null)},${jsonMap.getOrElse("refr_urlport",null)},${jsonMap.getOrElse("refr_urlpath",null)},${jsonMap.getOrElse("refr_urlquery",null)},${jsonMap.getOrElse("refr_urlfragment",null)},${jsonMap.getOrElse("refr_medium",null)},${jsonMap.getOrElse("refr_source",null)},${jsonMap.getOrElse("refr_term",null)},${jsonMap.getOrElse("mkt_medium",null)},${jsonMap.getOrElse("mkt_source",null)},${jsonMap.getOrElse("mkt_term",null)},${jsonMap.getOrElse("mkt_content",null)},${jsonMap.getOrElse("mkt_campaign",null)},${jsonMap.getOrElse("se_category",null)},${jsonMap.getOrElse("se_action",null)},${jsonMap.getOrElse("se_label",null)},${jsonMap.getOrElse("se_property",null)},${jsonMap.getOrElse("se_value",null)},${jsonMap.getOrElse("tr_orderid",null)},${jsonMap.getOrElse("tr_affiliation",null)},${jsonMap.getOrElse("tr_total",null)},${jsonMap.getOrElse("tr_tax",null)},${jsonMap.getOrElse("tr_shipping",null)},${jsonMap.getOrElse("tr_city",null)},${jsonMap.getOrElse("tr_state",null)},${jsonMap.getOrElse("tr_country",null)},${jsonMap.getOrElse("ti_orderid",null)},${jsonMap.getOrElse("ti_sku",null)},${jsonMap.getOrElse("ti_name",null)},${jsonMap.getOrElse("ti_category",null)},${jsonMap.getOrElse("ti_price",null)},${jsonMap.getOrElse("ti_quantity",null)},${jsonMap.getOrElse("pp_xoffset_min",null)},${jsonMap.getOrElse("pp_xoffset_max",null)},${jsonMap.getOrElse("pp_yoffset_min",null)},${jsonMap.getOrElse("pp_yoffset_max",null)},${jsonMap.getOrElse("useragent",null)},${jsonMap.getOrElse("br_name",null)},${jsonMap.getOrElse("br_family",null)},${jsonMap.getOrElse("br_version",null)},${jsonMap.getOrElse("br_type",null)},${jsonMap.getOrElse("br_renderengine",null)},${jsonMap.getOrElse("br_lang",null)},${jsonMap.getOrElse("br_features_pdf",null)},${jsonMap.getOrElse("br_features_flash",null)},${jsonMap.getOrElse("br_features_java",null)},${jsonMap.getOrElse("br_features_director",null)},${jsonMap.getOrElse("br_features_quicktime",null)},${jsonMap.getOrElse("br_features_realplayer",null)},${jsonMap.getOrElse("br_features_windowsmedia",null)},${jsonMap.getOrElse("br_features_gears",null)},${jsonMap.getOrElse("br_features_silverlight",null)},${jsonMap.getOrElse("br_cookies",null)},${jsonMap.getOrElse("br_colordepth",null)},${jsonMap.getOrElse("br_viewwidth",null)},${jsonMap.getOrElse("br_viewheight",null)},${jsonMap.getOrElse("os_name",null)},${jsonMap.getOrElse("os_family",null)},${jsonMap.getOrElse("os_manufacturer",null)},${jsonMap.getOrElse("os_timezone",null)},${jsonMap.getOrElse("dvce_type",null)},${jsonMap.getOrElse("dvce_ismobile",null)},${jsonMap.getOrElse("dvce_screenwidth",null)},${jsonMap.getOrElse("dvce_screenheight",null)},${jsonMap.getOrElse("doc_charset",null)},${jsonMap.getOrElse("doc_width",null)},${jsonMap.getOrElse("doc_height",null)},${jsonMap.getOrElse("tr_currency",null)},${jsonMap.getOrElse("tr_total_base",null)},${jsonMap.getOrElse("tr_tax_base",null)},${jsonMap.getOrElse("tr_shipping_base",null)},${jsonMap.getOrElse("ti_currency",null)},${jsonMap.getOrElse("ti_price_base",null)},${jsonMap.getOrElse("base_currency",null)},${jsonMap.getOrElse("geo_timezone",null)},${jsonMap.getOrElse("mkt_clickid",null)},${jsonMap.getOrElse("mkt_network",null)},${jsonMap.getOrElse("etl_tags",null)},${timestamp_dvce_sent_tstamp},${jsonMap.getOrElse("refr_domain_userid",null)},${jsonMap.getOrElse("refr_dvce_tstamp", null)},${jsonMap.getOrElse("domain_sessionid",null)},${timestamp_derived_tstamp},${jsonMap.getOrElse("event_vendor",null)},${jsonMap.getOrElse("event_name",null)},${jsonMap.getOrElse("event_format",null)},${jsonMap.getOrElse("event_version",null)},${jsonMap.getOrElse("event_fingerprint",null)},${jsonMap.getOrElse("true_tstamp", null)})".update.apply()
        if(timing == true) sql"insert into performance values (${jsonMap.getOrElse("app_id",null)},${jsonMap.getOrElse("platform",null)},${jsonMap.getOrElse("user_ipaddress",null)},${jsonMap.getOrElse("event_fingerprint",null)},${jsonMap.getOrElse("page_urlpath",null)},${jsonMap.getOrElse("page_urlhost",null)},${jsonMap.getOrElse("br_name",null)},${jsonMap.getOrElse("br_version",null)},${performanceMap.getOrElse("requestStart",null)},${performanceMap.getOrElse("chromeFirstPaint",null)},${performanceMap.getOrElse("domContentLoadedEventStart",null)},${performanceMap.getOrElse("navigationStart",null)},${performanceMap.getOrElse("unloadEventStart",null)},${performanceMap.getOrElse("fetchStart",null)},${performanceMap.getOrElse("domainLookupStart",null)},${performanceMap.getOrElse("responseStart",null)},${performanceMap.getOrElse("connectStart",null)},${performanceMap.getOrElse("domContentLoadedEventEnd",null)},${performanceMap.getOrElse("loadEventEnd",null)},${performanceMap.getOrElse("responseEnd",null)},${performanceMap.getOrElse("connectEnd",null)},${performanceMap.getOrElse("domInteractive",null)},${performanceMap.getOrElse("redirectStart",null)},${performanceMap.getOrElse("unloadEventEnd",null)},${performanceMap.getOrElse("loadEventStart",null)},${performanceMap.getOrElse("secureConnectionStart",null)},${performanceMap.getOrElse("domComplete",null)},${performanceMap.getOrElse("domainLookupEnd",null)},${performanceMap.getOrElse("domLoading",null)},${performanceMap.getOrElse("redirectEnd",null)})".update.apply()
    }
    catch {
      case e => e.printStackTrace()
    }
  }

}

class PostgresThread extends Thread{

  val configFile = new File("config.conf");
  println(configFile.getAbsolutePath);
  val config = ConfigFactory.parseFile(configFile)

  var jValue : JValue = null
  var postgres = new PostgresLoader

  def jsonParser(input : scala.Predef.String) : Map[String,Any] = {
    val event = EventTransformer.transform(input)
    event.right.foreach(
      pair=>
        jValue = parse(pair)
    )
    val jsonMap = jValue.values.asInstanceOf[Map[String, Any]]
    return jsonMap
  }

  val props = new Properties()
  println("bootstrap.servers: " + config.getString("kafka.brokers"))
  println("key.deserializer: " + "org.apache.kafka.common.serialization.StringDeserializer")
  println("value.deserializer: " + config.getString("kafka.brokers"))
  println("kgroup.id: " + config.getString("postgres.groupid"))

  props.put("bootstrap.servers", config.getString("kafka.brokers") )
  props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("group.id", config.getString("postgres.groupid") )
  val consumer = new KafkaConsumer[String, String](props)
  consumer.subscribe(util.Collections.singletonList(config.getString("kafka.topic")))

  override def run(){

    while (true) {
      val records = consumer.poll(100)
      for (record <- records.asScala) {
        postgres.save(jsonParser(record.value()))
      }
    }
  }

}


object Kafka2Storage extends Logging {


 def main(args: Array[String]) {
   logger.info("Starting Applicaiton")
    var postgres = new PostgresThread()
    logger.info("postgres thread is running")
    postgres.run()
  //  val config = ConfigFactory.parseFile(new File("config.conf"))
  //  for(i <- 0 until config.getInt("postgres.numberOfThreads")){
  //    var postgres = new PostgresThread()
  //    logger.info("postgres thread is running")
  //    postgres.run()
  //  }
 }
}
