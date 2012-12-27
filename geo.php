<?php
  function cidrconv($net) { 
    $start=strtok($net,"/"); 
    $n=3-substr_count($net, "."); 
    if ($n>0) { for ($i=$n;$i>0;$i--) $start.=".0"; } 
    $bits1=str_pad(decbin(ip2long($start)),32,"0",STR_PAD_LEFT); 
    $net=pow(2,(32-substr(strstr($net,"/"),1)))-1; 
    $bits2=str_pad(decbin($net),32,"0",STR_PAD_LEFT); 
    $final="";
    for ($i=0;$i<32;$i++) { 
      if ($bits1[$i]==$bits2[$i]) $final.=$bits1[$i]; 
      if ($bits1[$i]==1 and $bits2[$i]==0) $final.=$bits1[$i]; 
      if ($bits1[$i]==0 and $bits2[$i]==1) $final.=$bits2[$i]; 
    } 
    return long2ip(bindec($final)); 
  }
  
  include 'Spyc.php';

  //detect real IP address
  if (!empty($_SERVER['HTTP_CLIENT_IP']))
  //check ip from share internet
  {
    $ip=$_SERVER['HTTP_CLIENT_IP'];
  }
  elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))
  //to check ip addr is passed from proxy
  {
    $ip=$_SERVER['HTTP_X_FORWARDED_FOR'];
  }
  else
  {
    $ip=$_SERVER['REMOTE_ADDR'];
  }

  function get_page_content($url){
    $resource = curl_init();
 
    curl_setopt($resource, CURLOPT_URL, $url);
    curl_setopt($resource, CURLOPT_HEADER, false);
    curl_setopt($resource, CURLOPT_RETURNTRANSFER, true);
 
    $content = curl_exec($resource);
 
    curl_close($resource);
 
    return $content;
  }

  function get_country_by_ip($ip) {
    $hostip_raw = get_page_content("http://api.hostip.info/get_html.php?ip=".$ip);
    $hostip_data = explode("\n", $hostip_raw);
    $country_parts = explode(" ", $hostip_data[0]);
    return strtolower($country_parts[1]);
  }

  //finally, this is the IP address
  $userIP = $ip;

  //$userIP = "178.165.58.116";

  $geo_country = get_country_by_ip($userIP);

  //print "userip = $userIP <br />";
  list($w, $x, $y, $z) = explode('.', $userIP);

  $config = Spyc::YAMLLoad('geo.db');

  $results = array();
  $results[0] = array();
  $results[1] = array();
  $results[2] = array();
  $results[3] = array();
  $results[4] = array();
  $results[5] = array();
  
  foreach ($config["countries"] as &$country)
  {
    $keys = array_keys ($country);
    $config_country = strtolower($keys[0]);
    $values = $country[$keys[0]];

    if (!array_key_exists("url", $values))
    {
      print "ConfigurationError:$url not configured for $config_country";
      exit;
    }
    $url = $values["url"];
 
    if ($config_country=="default")
    {
      array_push($results[5], $url);
    } 
    if (array_key_exists("hostip_service", $values) && true == $values["hostip_service"])
    {
      array_push($results[4], $url);
    }   

    if (array_key_exists("IP", $values))
    {
      $ip_list = $values["IP"];

      foreach ($ip_list as &$full_ip)
      {
        $cidr = cidrconv($full_ip);
        list($w1, $x1, $y1, $z1) = explode(".", $cidr);
        if ($w == $w1)
        {
           if ($x == $x1)
           {
             if ($y == $y1)
             {
               if ($z == $z1)
               {
                 array_push($results[0], $url);
               }
               elseif ($z1 == '255')
               {
                 array_push($results[1], $url);
               }
             }
             elseif ($y1 == '255')
             {
               array_push($results[2], $url);
             }
           }
           elseif ($x1 == '255')
           {
             array_push($results[3], $url);
           }
        }
      }
    }
  }
  
  $target_url = "";
  foreach($results as $r)
  {
    if(count($r) > 0)
    {
      //print "$r[0] <br />";
      $target_url = $r[0];
      break;
    }
  }

  if(NULL != $target_url and strlen($target_url) > 0 and "none" != strtolower($target_url) and "null" != strtolower($target_url))
  {
    print '<meta http-equiv="refresh" content="0;url='.$target_url.'"/>';
    exit;
  }
?>
