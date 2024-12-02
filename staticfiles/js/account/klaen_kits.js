$(document).ready(function () {

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
    // Fetch data from the server
    $.ajax({
        url: '/klaen/api/get-all-kits',  // Ensure this matches your Django URL
        type: 'GET',
        success: function (data) {
            // Hide the loading cube
            toggleLoading(false);

            // showLoading("Load data su"); // Hide loading message
            var tableBody = $('#data-table tbody');
            tableBody.empty(); // Clear existing rows

            data.forEach(function (item) {
                // Format data (you can customize this)
                var status = item.active ? 'Active' : 'Inactive';
                var lastUpdated = new Date(item.last_time).toLocaleString();
                var startDate = new Date(item.timestamp).toLocaleString();

                // Create a row
                var row = `
                    <tr>
                        <td>${item.serial_number}</td>
                        <td>${status}</td>
                        <td>${lastUpdated}</td>
                        <td><a href="/klaen/chart-sn?serial_number=${item.serial_number}" class="btn btn-success btn-sm">View Chart</a></td>
                        <td><button class="btn btn-primary btn-sm">View</button></td>
                    </tr>
                `;

                // Append the row to the table
                tableBody.append(row);
            });
            // Safely initialize or reinitialize DataTable
            if ($.fn.DataTable) {
                if ($.fn.DataTable.isDataTable('#data-table')) {
                    dataTable.destroy();
                }
                dataTable = $('#data-table').DataTable();
            } else {
                console.error('DataTables plugin is not loaded or initialized.');
            }
        
            
        },
        error: function (error) {
            console.error('Error fetching data:', error);
            alert('Failed to load data.');
        }
    });

    
});