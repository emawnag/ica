import re
import requests

# Step 1: Download the RSS feed
url = "https://chenling3.blogspot.com/feeds/posts/default"
response = requests.get(url)
rss_feed = response.text

# Step 2: Extract URLs using regex
pattern = r"https://andythebreaker\.github\.io/InClassTestPaper/#[^&]+"
urls = re.findall(pattern, rss_feed)

print(f"Number of URLs found: {len(urls)}")

# Step 2.1: Extract titles using regex
#title_pattern = r"title='(\d+) 個意見'"
#titles = re.findall(title_pattern, rss_feed)

#print(f"Number of titles found: {len(titles)}")

#print(titles)

# Step 2.2: Extract comment counts using regex
comment_pattern = r"href='(https://chenling3\.blogspot\.com/[^<>]+\.html)#comment-form' title='(\d+) 個意見'/>"
comments = re.findall(comment_pattern, rss_feed)

print(f"Number of comments found: {len(comments)}")
#print(comments[0][0])

# Step 2.5: Extract updated dates using regex
updated_pattern = r"<updated>([^<>]+)</updated>"
updated_dates = re.findall(updated_pattern, rss_feed)

print(f"Number of updated dates found: {len(updated_dates)}")
#print(updated_dates)

# Step 3: Generate HTML with Semantic-UI structure
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InClassTestPaper Viewer</title>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"
    />
    <style>
        body {{
            display: flex;
            height: 100vh;
            margin: 0;
        }}
        #menu {{
            width: 250px;
            flex-shrink: 0;
            background-color: #f9f9f9;
            border-right: 1px solid #ddd;
            overflow-y: auto;
        }}
        #iframe-container {{
            flex-grow: 1;
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
</head>
<body>
    <div id="menu">
        <div class="ui vertical menu">
"""

# Add menu items for each URL
var_j = 0
for i, url in enumerate(urls):
    if i > 0 and url == urls[i - 1]:
        continue
    var_j=var_j+1
    html_template += f"""
            <a class="item" onclick="loadIframe('{url}','{updated_dates[var_j]}','{comments[var_j-1][0]}',{comments[var_j-1][1]})">
                Link {i + 1}
            </a>
    """

# Add remaining HTML
html_template += """
        </div>
    </div>
    <div id="iframe-container">
        <iframe id="iframe" src=""></iframe>
    </div>
    <script>
        function loadIframe(url,j,comment_url,comment_count) {
            document.getElementById('iframe-container').innerHTML = `
            <iframe id="iframe" src="${url}"></iframe>   
            <div class="ui floating visible message" style="position: absolute; left: 48vw; top: 0;">
                <p>${j}</p><a href="${comment_url}">${comment_count} comments</a>
            </div>
            `;
        }
    </script>
</body>
</html>
"""

# Step 4: Save HTML file
output_file = "output.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_template)

print(f"HTML file '{output_file}' generated successfully!")
