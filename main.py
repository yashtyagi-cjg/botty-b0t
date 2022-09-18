import praw
import os
import re
import json
import time
from dotenv import dotenv_values


def read_a_post(reddit, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.hot(limit=5):
        print("Title: ", submission.title)
        print("Text: ", submission.selftext)
        print("Score: ", submission.score)


# Will work on it or include it later after completing the mention module
def reply_to_post(reddit, subreddit_name):
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", 'r') as file:
            posts_replied_to = file.read()
            posts_replied_to = posts_replied_to.split('\n')
            posts_replied_to = list(filter(None, posts_replied_to))

    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.hot(limit=5):
        if submission.id not in posts_replied_to:
            if re.search('Lounge', submission.title, re.IGNORECASE):
                submission.reply('Me Too')
                posts_replied_to.append(submission.id)
                print("Replied To: ")
                print("Title: ", submission.title)
                print("Text: ", submission.selftext)


# This works for mention in comment but doesn't work for mention in post description
# A reply to u/botty-bot message with reference to username is not considered as a mention but as reply of a comment
def check_if_mentioned(reddit):
    # Should limit the reiteration of the previous mention using a set of length 5 or so
    # Checks for presence fo a file mentioned_posts.txt and Opens the file mentioned_posts.txt to read the contents
    # and get 10 last mentions which have been replied to. Then we check for mentions in the inbox and if the id matches
    # with those in .txt file they are not processed rest are processed

    mentioned = []
    if os.path.isfile('mentioned_posts.txt'):
        with open('mentioned_posts.txt', 'r') as f:
            mentioned = f.read()
            mentioned = mentioned.split('\n')
            mentioned = list(filter(None, mentioned[:10]))

    for mention in reddit.inbox.mentions(limit=10):
        if mention.id in mentioned:
            continue
        mentioned.append(mention.id)
        mention.reply('Dekh Chutiye Kam kar raha h na? 1227')

        # reply_to_mention(reddit)

        '''
        print("Author: ", mention.author)
        # Removing the call to u/botty-b0t so that the rest of the arguments can be easily processed
        mention_body = mention.body
        mention_body = re.sub('u/botty-b0t ', '', mention_body)
        print("Body: ", mention.body)
        print("Processed Body: ", mention_body)
        mention.reply("Read it -- {}".format(time.ctime()))
        '''
    # Writes the 10 last comments which have been replied to
    with open('mentioned_posts.txt', 'w') as f:
        f.writelines('\n'.join(mentioned))
        '''
        Need to split mention_body to correlate any words that can be altered in the context of words transaltion.
        Subsequently post a reply.
        
        Also a file to log the comments replied to has to be created. 
        '''

# def reply_to_mention(reddit):


def main():
    reddit = praw.Reddit(client_id=config['client_id'],
                         client_secret=config['client_secret'],
                         username=config['username'],
                         password=config['password'],
                         user_agent=config['user_agent'])
    # read_a_post(reddit, 'tryingout_bottesting')
    # for submission in reddit.front.hot(limit=5):
    #     print(submission.id, submission)
    # reply_to_post(reddit, 'tryingout_bottesting')
    check_if_mentioned(reddit)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = dotenv_values(".env")
    main()


