# myfxbook-calendar-scraper
a xml scraper for myfxbook that automatically downloads the requested calendar xml


Make sure you've set the config.json correctly


{
   "email": "yourmail@mail.com",
   "password": "strongestPassword123",
   "login_url": "https://www.myfxbook.com/login",
   "search_url": "https://www.myfxbook.com/calendar_statement.xml?&start=&end=&filter=",
   "output_file_name": "out.xml",

   "latest_cookies": {},
   "latest_header_cookie": {}
}

You do not need to set "latest_cookies" and "latest_header_cookie"
Just run and it will use selenium chrome webdriver to emulate the login when necessary.
