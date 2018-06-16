<?php
$connect=mysqli_connect("localhost","root","","sdp");
$query="SELECT City, Count from python";
$result=mysqli_query($connect,$query);

?>

<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data=google.visualization.arrayToDataTable([
			['City','Count'],
			<?php
			while($row=mysqli_fetch_array($result))
			{
				echo "['".$row["City"]."',".$row["Count"]."],";
				
			}
			?>
			
		]);

        var options = {
          title: 'Pictorial',
		  is3D:true,
		  'animation':{duration:1000,easing:'in'}
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
		var chart1 = new google.visualization.BarChart(document.getElementById('barchart'));

        
		chart.draw(data, options);
		chart1.draw(data, options);
      }
    </script>
  </head>
  <body>
	<div id="container">
    <div id="piechart" style="width: 900px; height: 500px; float:left; margin-top:10px; margin-left:10px"></div>
	<div id="barchart" style="width: 900px; height: 500px; float:left; margin-top:10px; margin-left:30px"></div>
	</div>
  </body>
</html>