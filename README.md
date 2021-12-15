# About
> google translation api와 jira api을 사용하여 자동으로 브랜치 이름을 만들어주는 스크립트

# Setup
환경변수에 다음 3가지를 등록해야 한다.
- `JIRA_USER` : JIRA email (ex: `username@domain.com`)
- `JIRA_PASSWORD` : JIRA API Token ([토큰 발급 방법](https://www.resolution.de/create-or-generate-api-tokens-in-jira/?utm_campaign=C%3Agoad%7CA%3Atext%7CR%3AreW%3Aapit%7CP%3Ajira-software%7CV%3Agoogle%7CG%3Aall%7CL%3Aen%7CF%3Aaware%7C&utm_term=create%20api%20token%20jira&utm_medium=cpc&utm_source=google&utm_content=create%20api%20token%20jira&gclid=Cj0KCQiAnuGNBhCPARIsACbnLzr3r1WWYLr0ho2xQAhv4VgO2ppc7Jc7Dqfveb7w-y4rg8LLBDB0wQIaAmeyEALw_wcB)
- `JIRA_BASE` : JIRA base url (ex: `https://domain.atlassian.net`)

# Installation
## required
- python3
## install
```bash
pip install require -r requirements
```
Done.

# Usage
## Single ticket
```bash
python main.py {ticket_no}
```
## Muliple ticket
```bash
python main.py {ticket_no1} {ticket_no2} ...
```

# Notice
- 구글 번역기 API, JIRA API 기반이라 네트워크 필수
- 구글 번역기라서 종종 번역 불가능한 부분이 한글로 나올 수 있음
- 특수 문자의 경우 직접 바꿔줘야 할 때도 있음
