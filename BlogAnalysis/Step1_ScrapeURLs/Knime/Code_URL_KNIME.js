var allLinks = document.querySelectorAll('a');
var linksArray = Array.from(allLinks);
var filteredLinksArray = [];
var count = 0;

// Filter links that match the specified pattern and limit to 100 links
linksArray.forEach(function(link) {
    if (link.href.startsWith('https://www.knime.com/blog/') && count < 100) {
        filteredLinksArray.push(link.href);
        count++;
    }
});

// Define the console.save function
console.save = function (data, filename) {
    if (!data) {
        console.error('Console.save: No data');
        return;
    }

    if (!filename) filename = 'console.json';

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

// Save the filtered links to a file
console.save(filteredLinksArray, 'knime_blog_links.json');
