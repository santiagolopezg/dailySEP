#dailySEP bot


import urllib2
import random
import datetime
from HTMLParser import HTMLParser
import re


def html_to_string(url):
        
        html_content = urllib2.urlopen(url).read()

        # now I have the web page in HTML format, I need to extract info of interest

        #print html_content

        '''
        try and extract this info -
        <li> <a href="https://plato.stanford.edu/entries/logic-dependence/"><strong>Dependence Logic</strong></a> [<em>February 23, 2017</em>]</li>
        3 things: Label, URL and Date
        '''

        start_index = html_content.find('<li> <a href="https://plato.stanford.edu/entries/logic-dependence/"><strong>Dependence Logic</strong></a> [<em>February 23, 2017</em>]')
        #print start_index

        end_index = html_content.find('</ul>    </div> <!-- End content --><!--DO NOT MODIFY THIS LINE AND BELOW-->')
        #print end_index


        new_html_content = html_content[start_index:end_index]
        #print new_html_content, len(new_html_content)

        '''
        so now, new_html_content is a string containing our info, in the form:
        <li> <a href="_url_"><strong>_entry_</strong></a>[<em>_date_</em>]</li>
        and this, for each particular entry.
        '''

        cuttin_it = new_html_content.split("</li>")

        #print cuttin_it

        return cuttin_it


        '''
        now, cuttin_it is a list of strings, where each string is basically this:
        '\n<li> <a href="https://plato.stanford.edu/entries/frege/"><strong>Gottlob Frege</strong></a> [<em>September 14, 1995</em>]', '\n'
        all that's left to do is to remove the superfluous html formatting and make the desired dicts.
        '''

def mkdict_url(entry, dict_entry_url):

        # remember, this is what it looks like: '\n<li> <a href="https://plato.stanford.edu/entries/frege/"><strong>Gottlob Frege</strong></a> [<em>September 14, 1995</em>]', '\n'

        b = entry.strip('\n<li> a href=')
        b = b.split('[')[0] #split into a new list: [url-name, date]
        try:
                ent, ur = b.split('><strong>')[1], b.split('><strong>')[0]
                ent = ent.split('</')[0]
                try:
                        ent= ent.replace('<em>', '')
                        ent=ent.replace('</em>', '')
                except:
                        pass

                
                ur = ur.strip('"')

                #print ent,ur

                dict_entry_url[ent] = ur
        except:
                pass

        return dict_entry_url


def mkdict_date(entry, dict_entry_date):

        # remember, this is what it looks like:
        #'\n<li> <a href="https://plato.stanford.edu/entries/frege/"><strong>Gottlob Frege</strong></a>
        #[<em>September 14, 1995</em>]', '\n'

        #print entry
 
        try:
                b = entry.split('<strong>')[1]
                #print b
                ent, date = b.split('</strong>')[0], b.split('[<em>')[1]
                date = date.strip('</em>]')
                try:
                        ent= ent.replace('<em>', '')
                        ent=ent.replace('</em>', '')
                except:
                        pass

                #print ent, date

                dict_entry_date[ent] = date
        except:
                pass

        return dict_entry_date

def make_dicts(update_dict_cp = True):
        #function to make dicts. Takes the table of contents url;
        #returns dicts, other stuff
        
        #instantiate dicts 

        dict_entry_url={}

        dict_entry_date={}

        #first, make entry -> url dict

        cuttin_it = html_to_string('https://plato.stanford.edu/published.html')

        for entry in cuttin_it:
                #generates the dicts needed to tweet random entries

                dict_entry_url = mkdict_url(entry, dict_entry_url)
                dict_entry_date = mkdict_date(entry, dict_entry_date)

        #print dict_entry_url, '{0} entries currently stored'.format(len(dict_entry_url.keys()))
        #print dict_entry_date, '{0} entries currently stored'.format(len(dict_entry_date.keys()))

        print '{0} entries currently stored'.format(len(dict_entry_date.keys()))

        save_to_txt(filename='savedicts.txt', dict_entry_url=dict_entry_url, dict_entry_date=dict_entry_date)


        #create a copy of my original entry -> url dict. Will use to select random entries.

        if update_dict_cp:
                
                dict_cp = dict_entry_url
                print 'updated dict cp'
                return dict_entry_url, dict_entry_date, dict_cp
        else:
                print 'not updating dict cp'
                return dict_entry_url, dict_entry_date

def save_to_txt(filename, dict_entry_url, dict_entry_date):
        with open(filename, 'w') as f:
                f.write(str(dict_entry_url))
                f.write('\n\n\n\n')
                f.write(str(dict_entry_date))

        print 'txt file saved.'


def random_entry(dict_cp):
        #takes the dict of entry -> url and returns a random entry, its url and the dict copy updated
        assert len(dict_cp)>0, "I've run out of entries to post about!"

        if len(dict_cp)==0:
                print 'updating dict... please wait'
                dict_entry_url, dict_entry_date, dict_cp = make_dicts(update_dict_cp = True)

        entry = random.choice(dict_cp.keys())
        url = dict_cp[entry]
        del dict_cp[entry]
        
        print '{0} entries left in dict'.format(len(dict_cp))
        
        return entry, url, dict_cp


def update_dict(last_update, dict_entry_url):
        time = datetime.datetime.now()
        time_since_update = time - last_update
        time_since_update = time_since_update.days
        #print time_since_update
        if time_since_update > 7:
                print 'dict needs updating'
                dict_entry_url, dict_entry_date = make_dicts(update_dict_cp = False)
        else:
                pass

        return dict_entry_url


def get_entry_info(url, entry, l): # returns additional info to complete the 280 character limit (or less) 
							# if it reaches a period after the limit. 
		html_content = urllib2.urlopen(url).read()

   		start_index = html_content.find('<p>')
   		#print start_index

   		end_index = html_content.find('</p>', start_index)
   		#print end_index
   		
		#print url #smth like https://plato.stanford.edu/entries/antiochus-ascalon/
   		
   		new_html_content = html_content[start_index+3:end_index]
   		
   		#print len(new_html_content)
   		
   		#print new_html_content

   		new_html_content = new_html_content.split('\n')
   		
   		text = ''
   		for sentence in new_html_content:
   			if len(sentence)>0:
   				text+=' '+sentence
   		text = text[1:]
   		
   		print text
   		
		#text = check_text(text)
		text = ez_html(text)
		
		#print text

		return text
		


def check_text(text):
		new_text = ''
		text = text.split(' ')
		#print text
		for word in text:
			flag = 0
		
		## first check if word is only text without format. if it is, leave as is;
			list_of_forbidden_items = ['&', '<', '>']
			for letter in word:
				if letter in list_of_forbidden_items:
			
					## is only text, no format:
					flag = 0
					break
				else:
					flag = 1
			if flag == 1:
				new_text += word+' '
				
			if flag == 0 : ## or else, remove formating and make plain text
				#print 'go'
				
				if '&ldquo;' in word: #eg.: &ldquo;have
					nword = word.split('&ldquo;')[1].split('&rdquo;')[0]
								
				if '<em>' in word: # eg.: <em>ceteris
			
					nword1 = word.split('<em>')[0]+word.split('<em>')[1]
					if '</em>' in nword1:
						nword = nword1.split('</em>')[0]
					else:
						nword = nword1
					#print nword
				
				if '</em>' in word:
					nword = word.split('</em>')[0]+word.split('</em>')[1]
				
				if 'href' in word:
					nword = ''
				
				if '<sup>' in word or '</sup>' in word: # eg.: #<sup>[<a href="notes.html#1" name="note-1">1</a>]</sup>
					nword = ''		
						
				if '&ndash;' in word: # eg.: 1075&ndash;1141)
					nword = word.split('&ndash;')[0]+'-'+word.split('&ndash;')[1]
					#print nword, 'dashed'
				
				if '&mdash;' in word: # Hume&mdash;had
					nword = word.split('&mdash;')[0]+'-'+word.split('&mdash;')[1]

				if '&lsquo;' in word:
					nword = word.split('&lsquo;')[1]+"'"+word.split('&lsquo;')[1].split('&rsquo;')[0]
				
				if '&rsquo;' in word:
					nword = word.split('&rsquo;')[0]+"'"+word.split('&rsquo;')[1]
			
				if 'oslash' in word:	#S&oslash;ren
					nword = word.split('&oslash;')[0]+'o'+word.split('&oslash;')[1]			
	
				if 'eacute' in word: #Dieudonn&eacute
					nword = word.split('&eacute;')[0]+'e'+word.split('&eacute;')[1]
			
				if '&#351;' in word: # Ku&#351;adas&#305;
					nword = word.split('&#351;')[0]+'s'+word.split('&#351;')[1]
				
				if '&#257;' in word: # upam&#257;
					nword = word.split('&#257;')[0]+'s'+word.split('&#257;')[1]
				
				if '&#305;' in word:	
					nword = word.split('&#305;')[0]+'i'+word.split('&#305;')[1]
				
				if '(' in word and '(' not in nword:	
					nword = '('+nword
				
				if ')' in word and ')' not in nword:
					nword = nword+')'
				
				if ':' in word and ':' not in nword:
					if 'here' in word or 'https' in word:
						nword = word
					else:
						nword = nword+':'	
			
				try:
					#print nword 
					new_text += nword+' '
				except:
					print word
				#print new_text
			
   		print new_text
   		   		
   		return new_text

   		
def ez_html(text):

	parser = HTMLParser()
	
	ntext = parser.unescape(text)
	
	ntext = ntext.replace('<em>', '').replace('</em>', '').replace('<sup>', '').replace('</sup>', '').replace('C.E.', 'CE').replace('B.CE', 'BCE').replace('etc.', 'etc').replace('e.g.', 'eg').replace('J.J.', 'JJ').replace('G.W.F.', 'GWF')
	
	#remove hrefs, multiple spaces, etc.
	ntext = re.sub("[[].*?[]]", "", ntext)
	ntext = re.sub("<a.*?a>", "", ntext)
	ntext = re.sub(' +',' ', ntext)
	
	return ntext

def tweet(entry, url):
        #generates the tweet message. takes an entry name and corresponding url, and returns a string to be tweeted
        #would be cool to be able to add a few sentences copied from the web page.

        msg = "Learn more about {0} here: {1}".format(entry, url)
         
        #print 'foo'       
        
        msg = ez_html(msg)
        
		#exit()
        
        #msg = check_text(msg)

        #print msg, 'gooboo'
				
    	new_text = get_entry_info(url, entry, len(msg))
    	
    	print new_text
    	
        available_char = 280 - len(msg)

        #print available_char
   		
        add_info = new_text[:available_char]

		#print add_info

		#keep only the complete sentences up to that point.
  		
        for letter in add_info[::-1]:
        	if letter == '.': #and the next letter isn't a c:
        		break
        	else:
        		add_info = add_info[:len(add_info)-1]
				
		#print add_info

		tweet = add_info + ' ' + msg

        return tweet


def schedule_tweet(last_tweet_time, dict_cp, dict_entry_url, last_update):
        #checks time of day, and decides whether to post or not -
        #could loop this indefinitely 
        #print 'this works'

        #before tweeting, check if dict needs updating
        dict_entry_url = update_dict(last_update, dict_entry_url)
        
        check_time = datetime.datetime.now()
        time_since_tweet = check_time - last_tweet_time
        time_since_tweet = time_since_tweet.seconds / 3600.0
        print str(time_since_tweet) + 'hours since last tweet'
        #if time_since_tweet >= 6.0:
        if time_since_tweet >= 0.0: ##debugging

                         
                print 'time to post'
                #this updates last_tweet_time
                last_tweet_time = check_time
                print 'updating last post time to {0}'.format(last_tweet_time)
                #now, time to post
                entry, url, dict_cp = random_entry(dict_cp)
                message = tweet(entry, url)
                        
                return message, dict_cp, last_tweet_time        
        else:
                print 'not time yet'

