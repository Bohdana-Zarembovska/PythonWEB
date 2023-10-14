import cgi
import html
import http.cookies
import os

form = cgi.FieldStorage()

username = html.escape( form.getfirst("name", "Not specified") )
age = html.escape(form.getfirst("age", "Not specified"))
author = form.getvalue("author", "Not specified")

directions = ["painting", "architecture", "sculpture", "music", "performing", "literature", "cinema"]
checkedDirection = []

for direction in directions:
    if direction in form:
        checkedDirection.append(direction)


cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
counterCookie = int(cookie.get("counter").value) + 1 if "counter" in cookie else 1

print(f"Set-cookie: counter={counterCookie};")
print("Content-type:text/html\r\n\r\n")

template_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form</title>
</head>
<body>
    <p>Your name: {username}</p>
    <p>Your age: {age}</p>
    <p>Your favourite author of horror films: - {author}</p>
    <p>Your favorite direction in art: {", ".join(checkedDirection)}</p>
    
    <p>Counter: {counterCookie}</p>

</body>
</html>
"""
print(template_html)