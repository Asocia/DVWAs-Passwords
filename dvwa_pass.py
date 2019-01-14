import bs4
import requests
import re

print("password: 0 means student didn't implement this feature.\n"
      "password: -1 means the password is not found. (i.e. kind of strong password)")
# students = {}

url = 'https://web.itu.edu.tr/djduff/2018/blg101/assignment2_student_links.html'
page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, 'html.parser')


for a_tag in soup.find_all('a'):
    student_name = a_tag.text.split("https://github.com/ituis18/a2-")[1]
    student_url = a_tag.text + '/master/bottle_app.py'
    student_url = student_url.replace('github.com', 'raw.githubusercontent.com')
    # print(student_url)

    bottle_page = requests.get(student_url)
    bottle_soup = bs4.BeautifulSoup(bottle_page.content, 'html.parser')
    # print(bottle_soup.text)

    hashed_pass = re.search(r"(?:.* ?= ?['\"])([a-f0-9]{64})(?:['\"])", bottle_soup.text, flags=re.IGNORECASE)
    if hashed_pass:
        hashed_pass = hashed_pass.group(1)
        hash_type = 'sha256'
        email = 'fakeaddress@mail-2-you.com'
        code = '2efdf3ddc6f839c1'
        query = 'https://md5decrypt.net/en/Api/api.php?hash={}&hash_type={}&email={}&code={}'.format(hashed_pass, hash_type,
                                                                                                 email, code)
        password = requests.get(query)
        password = password.content.decode('utf-8')
        if not password:
            password = -1

    else:
        password = 0

    print("url: {}, password: {}".format(a_tag.text, repr(password)))

    # students[student_name] = {"url": a_tag.text, "password": password}

# print(students)
