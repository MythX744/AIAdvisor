function advisor(allData) {
    var extractedDataArray = [[], [], [], [], [], []];

    allData.forEach(function(item) {
        if ('spending' in item) {
            extractedDataArray[0].push(item['spending']);
        }
        if ('expectations' in item) {
            extractedDataArray[1].push(item['expectations']);
        }
        if ('field' in item) {
            extractedDataArray[2].push(item['field']);
        }
        if ('tasks' in item) {
            extractedDataArray[3].push(item['tasks']);
        }
        if ('rating' in item) {
            extractedDataArray[4].push(item['rating']);
        }
        if ('rating_star' in item) {
            extractedDataArray[5].push(item['rating_star']);
        }
    });

    console.log(extractedDataArray);

    // Send the extractedDataArray to the Flask route using AJAX
    $.ajax({
        url: '/get_advisor_data',
        type: 'POST',  // Use POST or GET based on your Flask route
        contentType: 'application/json',
        data: JSON.stringify({ extractedDataArray: extractedDataArray }),
        success: function(response) {
            console.log('Data sent successfully:', response);
            console.log('Response:', response);
            // Extracted data from the response
            var results = response.results;
            var message = response.message;
            // Display the results in your HTML or do further processing
            console.log('Results:', results);
            // Display the message in your HTML or do further processing
            console.log('Message:', message);

            // Display the results in the "resultsDiv" div
            var resultsDiv = document.getElementById('your-aitools-container');
            var messageDiv = document.getElementById('message');
            resultsDiv.innerHTML = '';
            if (results.length > 0) {
                if(message === 'false')
                    messageDiv.innerHTML = 'We could not find exactly what you are looking for. Here are some suggestions that are close to your demands :';
                results.forEach(function(result) {
                    resultsDiv.innerHTML += '<p>Name: ' + result.name + ', Description: ' + result.description + '</p>';
                });
            } else {
                resultsDiv.innerHTML = 'No results found.';
            }
        },
        error: function(error) {
            console.error('Error sending data:', error);
        }
    });
}