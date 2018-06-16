<?php
	//if(!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest')
if($_SERVER["REQUEST_METHOD"]=="GET"){
$j=$_GET['j'];
$c=$_GET['c'];
$l=$_GET['l'];
$t=$_GET['t'];
require 'start_db.php';
$add=$j.$c.$l.$t;
$query="SELECT * FROM Job_URL_List WHERE Unique_Job_Value='$add'";
$query_run=mysqli_query($con,$query);
$i=0;
$result=[];
while($query_row=mysqli_fetch_assoc($query_run)){
	$job=$query_row['Job_URL'];
	$i=$i+1;
	$result[]=$job;
}

//echo $result[1];

if($i==2)
{
	$job1=$result[0];
	$job2=$result[1];
	$response=array(
	'count'=>$i,
    'Job1'=>$job1,
	'Job2'=>$job2
   );
   echo json_encode($response);
}
else{
	$job1=$result[0];
	$response=array(
	'count'=>$i,
    'Job1'=>$job1
   );
   echo json_encode($response);
}
}

?>