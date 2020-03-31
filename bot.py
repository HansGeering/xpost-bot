import praw

reddit = praw.Reddit('bot', config_interpolation='basic')

monitor_subreddits = reddit.config.custom['monitor_subreddits'].split(',')
monitor_subreddits = '+'.join(monitor_subreddits)

restricted_origins = reddit.config.custom['restricted_origins'].split(',')

DEBUG = True if reddit.config.custom['debug'] == '1' else False

def prepare_message(author, subreddit):
	message = reddit.config.custom['message_to_user']
	message = message.replace('{user}', author)
	message = message.replace('{subreddit}', subreddit)
	message = message.replace('"', '')
	return message

subreddit = reddit.subreddit(monitor_subreddits)
for submission in subreddit.stream.submissions(skip_existing=True):
	if DEBUG: print('Checking new post >=' + submission.title + ' by ' + submission.author.name + '=<')
	for duplicate in submission.duplicates():
		if duplicate.subreddit in restricted_origins:
			if DEBUG: print('#> Restricted origin "' + duplicate.subreddit.display_name + '"')
			if duplicate.author.name == submission.author.name:
				if DEBUG: print('#> Author matches, no problem')
			else:
				if DEBUG: print('#> Author does not match, deleting post!')
				submission.mod.remove()
				message = prepare_message(submission.author.name, submission.subreddit.display_name)
				submission.author.message(reddit.config.custom['subject_to_user'], message, submission.subreddit.display_name)
		else:
			if DEBUG: print('#> Duplicate found, but not restricted origin "' + duplicate.subreddit.display_name + '"')
