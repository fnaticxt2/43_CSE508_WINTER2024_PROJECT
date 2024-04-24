<?php


$servername = "localhost";
$username = "root";
$password = "";
$database = "ir_job";


$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


$stmt = $conn->prepare("INSERT INTO jobs SET job_id=?, company_id=?, jd_url=?, skills=?, job_description=?, extra_data=?, title=?, company_name=?, posted_on=?, platform=?, processed_text=?");

$perPage = 100;
$locations = array("mumbai","delhi","pune","banglore","indore","chennai","nagpur","bhopal");
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

    $url = "https://www.naukri.com/jobapi/v3/search?noOfResults={$perPage}&urlType=search_by_key_loc&searchType=adv&location={$location_str}&keyword={$labels_str}&sort=f&src=sortby&pageNo={$pageNo}&k={$labels_str}&l={$location_str}&nignbevent_src=jobsearchDeskGNB&jobAge=1&latLong={$lat}_{$Long}";

    $curl = curl_init();
    curl_setopt_array($curl, array(
        CURLOPT_URL => $url,
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

            $processed_text = preprocessText($skills." ".$job_description." ".$extra_data);


            $platform = "naukri";
            $stmt->bind_param("sssssssssss", $job_id, $company_id, $jd_url, $skills, $job_description, $extra_data, $title, $company_name, $posted_on, $platform, $processed_text);

            try {
                $result = $stmt->execute();
                if ($result === false) {
                }
            } catch (mysqli_sql_exception $e) {
                
                $error_code = $stmt->errno;
                if ($error_code == 1062) { 
                    continue;
                } else {
                    echo "Error during executing statement: " . $e->getMessage()." Code: ".$stmt->errno;
                    exit();
                }
            }
        }
    }
    if($totalRetrived >= $noOfJobs || $isExit){
        break;
    }
    echo " Page No: ".$pageNo.", TotalRetrived: ".$totalRetrived.", NoOfJobs: ".$noOfJobs."<br>";
    $pageNo++;
    sleep(2);
}
$stmt->close();
$conn->close();





function preprocessText($text) {
    // Define stopwords, punctuation characters, and specified characters
    $stopWords = array("i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now");
    $punctuationChars = array(".", ",", ";", ":", "-", "!", "?", "\"", "'", "(", ")", "[", "]", "{", "}", "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "_", "+", "=", "~", "`");
    $specifiedChars = array(".", ";", ":", "-", " ");

    // Remove stopwords, punctuations, and specified characters
    $processedText = "";
    $words = explode(" ", $text);
    foreach ($words as $word) {
        $word = strtolower($word);
        if (!in_array($word, $stopWords) && !in_array($word, $punctuationChars) && !in_array($word, $specifiedChars)) {
            $processedText .= trim($word) . " ";
        }
    }
    $processedText = trim($processedText);
    $processedText = strip_tags($processedText);
    $processedText = preg_replace('/<br\s*\/?>/', ' ', $processedText);
    return $processedText;
}

