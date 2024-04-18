<?php


$servername = "localhost";
$username = "root";
$password = "";
$database = "ir_job";


$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


$stmt = $conn->prepare("INSERT INTO jobs SET job_id=?, company_id=?, jd_url=?, skills=?, job_description=?, extra_data=?, title=?, company_name=?, posted_on=?, platform=?");

$curl = curl_init();
$perPage = 100;
$locations = array("mumbai","delhi","pune","banglore");
$labels = array("Software Developer","Web Developer","Data Analyst","Systems Analyst","Network Engineer","Database Administrator","Quality Assurance (QA) Engineer","IT Support Engineer","Cybersecurity Analyst","Machine Learning Engineer","Cloud Engineer","DevOps Engineer","IT Project Manager","UI/UX Designer","Mobile App Developer");
$location_str = http_build_query($locations, '', ',');
$labels_str = http_build_query($labels, '', ',');
$lat = 28.547766647372917;
$Long = 77.27393141153699;
$pageNo = 1;
$yesterdayDate = date("Y-m-d", strtotime("yesterday"));
$yesterdayStamp = strtotime($yesterdayDate);


while(true){
    $allJobs = array();


    curl_setopt_array($curl, array(
        CURLOPT_URL => "https://www.naukri.com/jobapi/v3/search?noOfResults={$perPage}&urlType=search_by_key_loc&searchType=adv&location={$location_str}&keyword={$labels_str}&sort=f&pageNo={$pageNo}&k={$labels_str}&l={$location_str}&nignbevent_src=jobsearchDeskGNB&src=jobsearchDesk&latLong={$lat}_{$Long}",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 0,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => 'GET',
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_HTTPHEADER => array(
          'systemid: Naukri',
          'appid: 108'
        ),
    ));
    
    $response = curl_exec($curl);
    if(curl_errno($curl)){
        echo 'Curl error: ' . curl_error($curl);
        exit();
    }
    curl_close($curl);
    $data = json_decode($response,true);
    $noOfJobs = $data["noOfJobs"];
    $jobDetails = $data["jobDetails"];
    $isExit = false;
    $totalRetrived = $perPage * $pageNo;
    if($jobDetails){
        foreach($jobDetails as $jobDetail){
            $timestamp = $jobDetail["createdDate"];
            $created_on = strtotime(date("Y-m-d", intval($timestamp / 1000)));
            if ($yesterdayStamp <= $created_on) {
                $allJobs[] = $jobDetail;
            }else{
                $isExit = true;
                break;
            }
        }
    }
    if($allJobs){
        
        foreach ($allJobs as $job) {
            $job_id = $job["jobId"];
            $company_id = $job["companyId"];
            $jd_url = "https://www.naukri.com".$job["jdURL"];
            $skills = $job["tagsAndSkills"];
            $job_description = $job["jobDescription"];
            $extra_data = "";
            $extra_data_arr=array();

            if($job["placeholders"]){
                foreach($job["placeholders"] as $jobph){
                    $row = $jobph["type"].": ".$jobph["label"];
                    array_push($extra_data_arr,$row);
                }
                if($extra_data_arr){
                    $extra_data = implode(", ", $extra_data_arr);
                }
            }

            $title = $job["title"];
            $company_name = $job["companyName"];
            
            $timestamp = $job["createdDate"];
            $posted_on = date("Y-m-d H:i:s", intval($timestamp / 1000));

            $skills = $conn->real_escape_string($skills);
            $job_description = $conn->real_escape_string($job_description);
            $extra_data = $conn->real_escape_string($extra_data);
            $title = $conn->real_escape_string($title);
            $company_name = $conn->real_escape_string($company_name);
            $platform = "naukri";
            $stmt->bind_param("ssssssssss", $job_id, $company_id, $jd_url, $skills, $job_description, $extra_data, $title, $company_name, $posted_on, $platform);

            try {
                $result = $stmt->execute();
                if ($result === false) {
                    die("Error executing statement: " . $stmt->error);
                }
            } catch (mysqli_sql_exception $e) {
                if ($e->getCode() == 1062) { 
               //     echo "Error: Duplicate entry. The record already exists.";
                } else {
                    echo "Error executing statement: " . $e->getMessage();
                    exit();
                }
            }
        }
    }
    if($totalRetrived >= $noOfJobs || $isExit){
        break;
    }
    $pageNo++;
//    echo " Page No: ".$pageNo." ";
}
$stmt->close();
$conn->close();

