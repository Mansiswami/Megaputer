import re
import requests

# URL of the webpage
url = "https://aws.amazon.com/blogs/?awsf.blog-master-category=category%23analytics&awsf.blog-master-learning-levels=*all&awsf.blog-master-industry=*all&awsf.blog-master-analytics-products=*all&awsf.blog-master-artificial-intelligence=*all&awsf.blog-master-aws-cloud-financial-management=*all&awsf.blog-master-blockchain=*all&awsf.blog-master-business-applications=*all&awsf.blog-master-compute=*all&awsf.blog-master-customer-enablement=*all&awsf.blog-master-customer-engagement=*all&awsf.blog-master-database=*all&awsf.blog-master-developer-tools=*all&awsf.blog-master-devops=*all&awsf.blog-master-end-user-computing=*all&awsf.blog-master-mobile=*all&awsf.blog-master-iot=*all&awsf.blog-master-management-governance=*all&awsf.blog-master-media-services=*all&awsf.blog-master-migration-transfer=*all&awsf.blog-master-migration-solutions=*all&awsf.blog-master-networking-content-delivery=*all&awsf.blog-master-programming-language=*all&awsf.blog-master-sector=*all&awsf.blog-master-security=*all&awsf.blog-master-storage=*all"

# Send a GET request to the URL
response = requests.get(url)

# Extract text from the response
html_content = response.text

# Use regular expressions to find all URLs in the HTML content
urls = re.findall(r'<a href="(https?://.*?)"', html_content)

# Print the first 100 URLs
for i, url in enumerate(urls[:100], 1):
    print(f"{i}. {url}")

# Save URLs to a text file
with open("blog_urls.txt", "w") as f:
    for url in urls:
        f.write(url + "\n")

print("Scraped URLs:")
print("Top 100 blog URLs saved to 'blog_urls.txt' file.")
