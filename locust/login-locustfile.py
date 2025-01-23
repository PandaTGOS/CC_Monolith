from locust import task, run_single_user
from locust import FastHttpUser


class login(FastHttpUser):
    host = "http://127.0.0.1:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        with self.client.request(
            "POST",
            "/login",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                "Content-Length": "33",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "127.0.0.1:5000",
                "Origin": "http://127.0.0.1:5000",
                "Priority": "u=0, i",
                "Referer": "http://127.0.0.1:5000/login",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            data="username=test123&password=test123",
            catch_response=True,
        ) as resp:
            pass
        
if __name__ == "__main__":
    run_single_user(login)
