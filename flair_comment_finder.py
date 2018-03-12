import praw
import config
import time

# Name of the subreddit
SUBREDDIT_NAME = "FortNiteBR"
# The word the bot looks for in the comment's flair
AUTHOR_FLAIR = "Epic Games"
# Bot's username
BOT_USERNAME = "EpicCommentFinder"
# Number of new comments the bot checks
COMMENTS_LIMIT = 25
# The time the bot goes to rest after checking the new comments
BOT_SLEEP_TIME = 10

# Loggin in the bot
def bot_login():
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    password=config.password,
                    username=config.username,
                    user_agent=config.user_agent)
    return r

def bot_run(reddit, subreddit):
    submissions_visited = []
    for new_comment in subreddit.comments(limit=COMMENTS_LIMIT):
        if AUTHOR_FLAIR.lower() in str(new_comment.author_flair_text).lower():
            comment_reply = ""
            bot_comment_id = 0
            counter = 0
            if new_comment.submission.id not in submissions_visited:
                submissions_visited.append(new_comment.submission.id)
                new_comment.submission.comments.replace_more(limit=None)
                for s_comment in new_comment.submission.comments.list():
                    if s_comment.author.name == BOT_USERNAME:
                        bot_comment_id = s_comment.id
                    if AUTHOR_FLAIR.lower() in str(s_comment.author_flair_text).lower():
                        counter += 1
                        comment_reply += "[EPIC COMMENT #" + str(counter) + " - " + s_comment.author.name + "]" + "(https://www.reddit.com" + s_comment.permalink + ")\n\n"
                if bot_comment_id == 0:
                    bot_comment = new_comment.submission.reply(comment_reply)
                    bot_comment.mod.distinguish(sticky=True)
                    print("Creating bot's sticky comment: ", new_comment.submission.title)
                else:
                    reddit.comment(bot_comment_id).edit(comment_reply)
                    print("Editing bot's sticky comment: ", new_comment.submission.title)
    print("Bot in rest for " + str(BOT_SLEEP_TIME) + " seconds")
    time.sleep(BOT_SLEEP_TIME)

# Bot going to an infinite loop in order to be always on
while True:
    reddit = bot_login()
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    bot_run(reddit, subreddit)