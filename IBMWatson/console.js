var allLinks = document.querySelectorAll('a');

// Convert the NodeList to an array for convenience
var linksArray = Array.from(allLinks);

// Initialize an array to store the filtered links
var filteredLinksArray = [];

// Filter links that match the specified pattern for IBM blog articles
linksArray.forEach(function(link) {
    // Adjust the regex pattern to match the blog article URLs on IBM's website
    if (/^https:\/\/www\.ibm\.com\/blog\/.+/.test(link.href)) {
        filteredLinksArray.push(link.href);
    }
});

// Define the console.save function to save the filtered links
console.save = function (data, filename) {
    if (!data) {
        console.error('Console.save: No data');
        return;
    }

    if (!filename) filename = 'filtered_links_ibm_blogs.json';

    if (typeof data === 'object') {
        data = JSON.stringify(data, undefined, 4);
    }

    var blob = new Blob([data], { type: 'text/json' }),
        e = document.createEvent('MouseEvents'),
        a = document.createElement('a');

    a.download = filename;
    a.href = window.URL.createObjectURL(blob);
    a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    a.dispatchEvent(e);
};

// Now, save the filtered links to a file
console.save(filteredLinksArray, 'filtered_links_ibm_blogs.json');
