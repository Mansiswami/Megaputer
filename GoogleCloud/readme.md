This is the series of codes to scrape blog text from Google Cloud's website for text analysis.
Step 1 - The console_code.js is the javascript code to extract all the blog URLs from Google Cloud's official blog page. All the extracted URLs are stored in filtered_links_google.json.
Step 2 - The scrape google blog content.py is the python code developed to scrape the complete blog content from all URLs and save it as a text file in your working directory.
Step 3 - The final code google blogs.py is the Python code to scrape all the text files and fetch the top 100 most used keywords. It also saves all those keywords in an Excel sheet for every blog and finally, a consolidated Excel sheet is created with all the top 100 most used keywords across all the blogs and their frequency of usage.
Step 4 - consolidated keywords top100.xlsx is the final output which shows the top 100 most used keywords across all the Google cloud blogs and their frequency of usage.
