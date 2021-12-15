import googletrans
import os
import requests
import sys
from typing import Iterable, List, Optional

from jira import JIRA, Issue, JIRAError


JIRA_USER = os.environ.get("JIRA_USER")
JIRA_PASSWORD = os.environ.get("JIRA_PASSWORD")
JIRA_OPTIONS = {"server": os.environ.get("JIRA_BASE")}

translator = googletrans.Translator()


def varify_ticket_format(ticket_no):
	if not ticket_no or ticket_no == '':
		return False
	tmp = ticket_no.split('-')
	if len(tmp) != 2:
		return False
	project, number = tmp[0], tmp[1]
	if project == '' or number == '' or not number.isnumeric() or \
		int(number) == 0 or not project.isalpha():
		return False
	return True


def branchname_maker(ticket_no, msg):
	if not msg or msg == '':
		raise Error
	change_list = [
		(' ', '-'),
		('_', '-'),
		(':', '-'),
		("'", '"'),
		('/', ''),
		('(', ''),
		(')', ''),
		('[', ''),
		(']', ''),
		('{', ''),
		('}', '')
	]
	for change_from, change_to in change_list:
		msg = msg.replace(change_from, change_to)
	return (ticket_no + '-' + msg).lower()

def get_jira_client() -> JIRA:
	return JIRA(basic_auth=(JIRA_USER, JIRA_PASSWORD), **JIRA_OPTIONS)

def get_issues(keys: Iterable[str], jira_client: Optional[JIRA] = None) -> List[Issue]:
	jira_client = jira_client or get_jira_client()
	return jira_client.search_issues(f"key in ({','.join(str(key) for key in keys)})")

def get_issue(key: str, jira_client: Optional[JIRA]=None) -> Issue:
	jira_client = jira_client or get_jira_client()
	return jira_client.issue(key)

def make_names(ticket_no_list: List[str]):
	issues = get_issues(ticket_no_list)
	for issue in issues:
		ticket_no = issue.key
		summary_origin = issue.fields.summary
		summary_trans = translator.translate(summary_origin, dest='en')
		suggested_name = branchname_maker(ticket_no, summary_trans.text)
		print(f"{ticket_no}\n\t- origin:\t\"{summary_origin}\"\n\t- result:\t\"{suggested_name}\"")

def make_name(ticket_no: str):
	issue = get_issue(ticket_no)
	summary_origin = issue.fields.summary
	summary_trans = translator.translate(summary_origin, dest='en')
	suggested_name = branchname_maker(ticket_no, summary_trans.text)

	answer = input(f"suggested name is: \"{suggested_name}\". copy this? (y/n): ")
	if answer.upper() in ('Y', 'YES', '네', '넵', '넹', 'DD', '', 'D'):
		os.system(f"echo '{suggested_name}' | pbcopy")
		print("copied!")
	else:
		print("bye")

def main(argv):
	if len(argv) == 1:
		make_name(argv[0])
	else:
		make_names(argv)

if __name__ == "__main__":
	argc = len(sys.argv)
	if argc <= 1:
		sys.stderr.write("[ERROR] At least 1 argument needed: ticket number\n")
		exit(-1)
	for i in range(1, argc):
		if not varify_ticket_format(sys.argv[i]):
			sys.stderr.write(f"[ERROR] Ticket format error : {sys.argv[i]}\n")
			exit(-1)
	main(sys.argv[1:])
