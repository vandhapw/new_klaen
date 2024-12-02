document.addEventListener("DOMContentLoaded", () => {
    function toggleLoading(show) {
        const loading_cube = document.getElementById("cube-loading");
        if (show) {
            loading_cube.style.display = "flex"; // Show loading cube
        } else {
            loading_cube.style.display = "none"; // Hide loading cube
        }
    }

    // Show the loading cube before starting the AJAX request
    toggleLoading(true);
    async function fetchData() {
      try {
        // Fetch data from the API
        const response = await fetch('/klaen/api/get-chart-sn'); // Replace with your API URL
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json(); // Parse the JSON response

        toggleLoading(false); // Hide the loading cube
        

        // Extract necessary fields for the chart
        const timestamps = data.map(item => item.timestamp);
        
        console.log(typeof(timestamps[timestamps.length - 1]), timestamps[0]);
        const last_time = data.map(item => item.last_time);
        const vocData = data.map(item => item.voc);
        const co2Data = data.map(item => item.co2);
        const dustData = data.map(item => item.dust);
        const tempData = data.map(item => item.temperature);
        const ozoneData = data.map(item => item.ozone);
        const humidityData = data.map(item => item.humidity);

        // Render chart with the fetched data
        new ApexCharts(document.querySelector("#reportsChart"), {
          series: [
            { name: 'VOC', data: vocData },
            { name: 'CO2', data: co2Data },
            { name: 'Dust', data: dustData },
            { name: 'Temperature', data: tempData },
            { name: 'Ozone', data: ozoneData },
            { name: 'Humidity', data: humidityData },
          ],
          chart: {
            height: 350,
            type: 'area',
            toolbar: {
              show: false
            },
          },
          markers: {
            size: 4
          },
          colors: ['#FF5733', '#33FF57', '#3357FF', '#FF33B5', '#FFBD33', '#5733FF'],
          fill: {
            type: "gradient",
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.3,
              opacityTo: 0.4,
              stops: [0, 90, 100]
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth',
            width: 2
          },
          xaxis: {
            type: 'string',
            categories: timestamps,
            min: timestamps[0],
            max: timestamps[timestamps.length - 1],
          },
          tooltip: {
            x: {
              format: 'dd/MM HH:mm'
            },
          }
        }).render();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please try again later.");
      }
    }

    // Call fetchData to initialize the chart
    fetchData();
  });