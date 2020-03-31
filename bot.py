import praw

reddit = praw.Reddit('bot', config_interpolation='basic')

monitor_subreddits = reddit.config.custom['monitor_subreddits'].split(',')
monitor_subreddits = '+'.join(monitor_subreddits)

restricted_origins = reddit.config.custom['restricted_origins'].split(',')

def prepare_message(author, subreddit):
	message = reddit.config.custom['message_to_user']
	message = message.replace('{user}', author)
	message = message.replace('{subreddit}', subreddit)
	message = message.replace('"', '')
	return message

subreddit = reddit.subreddit(monitor_subreddits)
#for submission in subreddit.stream.submissions(skip_existing=True):
for submission in subreddit.stream.submissions():
	print('***')
	print(submission.title + ' by ' + submission.author.name)
	for duplicate in submission.duplicates():
		if duplicate.subreddit in restricted_origins:
			print('#> Restricted origin "' + duplicate.subreddit.display_name + '"')
			if duplicate.author.name == submission.author.name:
				print('#> Author matches, no problem')
			else:
				print('#> Author does not match, deleting post!')
				submission.mod.remove()
				message = prepare_message(submission.author.name, submission.subreddit.display_name)
				submission.author.message(reddit.config.custom['subject_to_user'], message, submission.subreddit.display_name)
		else:
			print('#> Duplicate found, but not restricted origin "' + duplicate.subreddit.display_name + '"')
