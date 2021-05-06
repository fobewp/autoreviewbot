from mwclient import Site
import sys
import time
from datetime import datetime

ua = 'Reviewer bot using mwclient framework (https://github.com/mwclient/mwclient)'
site = Site('hu.wikipedia.org', clients_useragent=ua)
input = open('my.credentials', 'r')
password = input.readline().split('\n')[0]
input.close()
site.login('FoBeBot', password)

filename = sys.argv[1];
stream = open(filename, 'r')
lines = stream.readlines();
success = 0;
for line in lines:
	try:
		contents = line.strip().split(',');
		title = ''
		for i in range(0,len(contents)-1):
			title += contents[i]
			if i < len(contents)-2:
				title += ','
		title = title.strip('\"').replace('_',' ');
		revid = int(contents[len(contents)-1]);
		print('Reviewing revision '+str(revid)+' of page '+title+'...', end=' ');
		
		page = site.pages[title]
		text = page.text()
		if not page.can('review'):
			raise mwclient.errors.InsufficientPermission(page)
		if not page.site.writeapi:
			raise mwclient.errors.NoWriteApi(page)
		comment = 'Bot: megerősített szerkesztők szerkesztéseinek automatikus ellenőrzése'
		result = page.site.post('review', revid=revid, comment=comment, token=page.get_token('review'))
		print(result['review']['result']);
		if result['review']['result'] == 'Success':
			success += 1;
		time.sleep(3)
	except ValueError:
		print(line)
log = open('run.log', 'a')
log.write(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")+" "+str(success)+" revisions marked as reviewed\n")
log.close()
