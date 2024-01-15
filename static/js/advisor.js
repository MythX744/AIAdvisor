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

}