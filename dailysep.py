#dailySEP bot


import urllib2
import random
import datetime

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


def tweet(entry, url):
        #generates the tweet message. takes an entry name and corresponding url, and returns a string to be tweeted
        #would be cool to be able to add a few sentences copied from the web page.

        msg = "{0}!\nLearn more about it here: {1}".format(entry, url)

        #l = len(msg)

        #add_info = get_entry_info(url, l)        

        
        return msg


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
        if time_since_tweet >= 6.0:
                         
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

