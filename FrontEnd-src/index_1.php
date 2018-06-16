<?php
session_start();



	
if($_SERVER["REQUEST_METHOD"]=="POST"){
	
$tech=$_POST["tech"];
$loc=$_POST["city"];
require 'start_db.php';
$query="SELECT * FROM Job_List WHERE Technology LIKE '%$tech%' AND Job_Location LIKE '%$loc%'";
$query_run=mysqli_query($con,$query);
if($query_run==null){
echo 'Unabe to display records';
}
else{
	?>
<html>
	<head>
		
		<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
	</head>
	<body style="background-color:cyan">
		<header>
			<div align="center" style="height:70px;">
				<h3 style="font-size:25px;color:black;position:relative;top:25px"> <?php echo $tech;?> jobs in <?php echo $loc;?></h3>
			</div>
		</header>
		<section>
			<div align="left" style="margin-top:100px;">
			<div id="Navigation" style="margin-left:635px;min-width:150px;min-height:75px;max-height:200px;max-width:400px;position:relative;top:0px;display:none;">
				<h3>EXPLORE FROM <a id="Monster1" target="_blank" align="Center">Monster</a> OR <a id="Stepstone1" target="_blank">Stepstone</a></h3>
			</div>
			<hr>
			<?php
			$i=0;
			while($query_row=mysqli_fetch_assoc($query_run)){
				
				$job_name=$query_row['Job_Title'];
				$company_name=$query_row['Company_Name'];
				$location=$query_row['Job_Location'];
				$technology=$query_row['Technology'];
			?>
			
			<div>
			<!--<div style="margin-left:500px;width:auto;height:auto;background-color:cyan">-->
				<p id="JobName<?php echo $i;?>"><?php echo $job_name;?></p> 
			    <p id="CompanyName<?php echo $i;?>"><?php echo $company_name;?></p>
				<p id="Location<?php echo $i;?>"><?php echo $location;?></p>
				<p id="Technology<?php echo $i;?>"><?php echo $technology;?></p>	
				<button name='submit<?php echo $i;?>' onclick="getJob(<?php echo $i;?>)" style="color:Red;border-radius:12px;" onMouseOver="this.style.color='White'" onMouseOut="this.style.color='Red'">Click Here for more information</button>
				
			</div>
			<hr>
			<?php
			$i=$i+1;
			}
			?>
			</div>
		</section>
		<script>
			function getJob(x){
				var job_name=document.getElementById('JobName'+x.toString()).innerHTML;
				var company_name=document.getElementById('CompanyName'+x.toString()).innerHTML;
				var Location=document.getElementById('Location'+x.toString()).innerHTML;
				var Technology=document.getElementById('Technology'+x.toString()).innerHTML;
				
				$.ajax({
				type: "GET",
				url: 'index1.php',
				data: {j:job_name,c:company_name,l:Location,t:Technology},
				success: function(data){
				var res=jQuery.parseJSON(data);
				count=res.count;
				if(count==1){
				job=res.Job1;
				//Navigate to the url
				window.open(job,'_blank');
				}
				else{
					job1=res.Job1;
					job2=res.Job2;
					get_job_url(job1,job2);
				}
				
				
				}
				});
				//document.write("Request sent successfully");
			
			}
			
			function get_job_url(job1,job2){
			//alert(job1);
			//alert(job2);
			var n=job1.includes("monster");
			if(n==true){
			document.getElementById('Monster1').href=job1;
			document.getElementById('Stepstone1').href=job2;
			document.getElementById('Navigation').style.display="block";
			}
			else{
				document.getElementById('Monster1').href=job2;
				document.getElementById('Stepstone1').href=job1;
				document.getElementById('Navigation').style.display="block";
			}
			
			}
			
		
		</script>
		
		
		
	</body>
</html>	
	
	
	
	
	<?php
}


}


?>