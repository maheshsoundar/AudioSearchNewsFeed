from TalkAudio import TalkAudio
from ListenAudio import ListenAudio
from NewsFeed import NewsFeed

'''
Runs the program to pick the search term from user (via mic) and reads out the required no of top news entries.
Set n_entries to required number of top headlines needed and extensive to true or false depending on the need
for a complete article read out or the summary. 

Note: extensive=False option can lead to a little load time before the articles are read out. Depends on the system.
'''
if __name__== '__main__':
	search_term = ''
	stop = False
	while stop==False:
	    while search_term == '':
	    	try:
		        print('Listening...\n')
		        TalkAudio().talk('Listening')
		        search_term = ListenAudio().take_command()
		        if(search_term != ''):
		            print(search_term)
		            newsarticles = NewsFeed(search_term,n_entries=5,extensive=False) #set the conditions here before running
		            newsarticles.read_out()
		            print('Do you want to make another search')
		            TalkAudio().talk('Do you want to make another search')
		            reply = ListenAudio().take_command()
		            print(reply)
		            if(reply.lower()!='yes' and reply.lower()!='continue'):
		                stop=True
		            else:
		                search_term = ''
		            print('Ok')
		            TalkAudio().talk('Ok')
		        else:
		            print('Try again!!!!!\n')
		    except:
		    	print('Error!!. Try again please!\n')
		    	exit()
	    if(stop==True):
	        break
	print('Done')