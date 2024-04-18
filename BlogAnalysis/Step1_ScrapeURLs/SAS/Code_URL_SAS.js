#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 22:39:46 2024

@author: shubhisri0809
"""

var allLinks = document.querySelectorAll('a[itemprop="url"]');

// Convert the NodeList to an array (optional, for convenience)
var linksArray = Array.from(allLinks);

// Initialize a counter and an array to store the filtered links
var counter = 0;
var filteredLinksArray = [];

// Filter links that match the specified SAS Enterprise blog structure and limit to the top 100
for (var i = 0; i < linksArray.length; i++) {
    // Check if the link belongs to the specified SAS Enterprise blog structure
    var regexResult = linksArray[i].href.match(/^https:\/\/blogs\.sas\.com\/content\/subconsciousmusings\/.+\/$/);
    if (regexResult && regexResult.length === 1) {
        // Store the matched portion in the array
        filteredLinksArray.push(linksArray[i].href);

        // Increment the counter
        counter++;

        // Check if the counter reaches 100, and break the loop if it does
        if (counter === 100) {
            break;
        }
    }
}

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

// Now, save the filtered links to a file
console.save(filteredLinksArray, 'filtered_links_sas_top100.json');
