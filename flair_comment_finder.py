import praw
import config
import time

# Name of the subreddit
SUBREDDIT_NAME = "EpicCommentFinderBot"
# The word the bot looks for in the comment's flair
AUTHOR_FLAIR = "Epic Games"
# Bot's username
BOT_USERNAME = "EpicCommentFinder"


# Loggin in the bot
def bot_login():
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    password=config.password,
                    username=config.username,
                    user_agent=config.user_agent)
    return r


def bot_run(reddit, subreddit):
    for new_comment in subreddit.stream.comments():
        if AUTHOR_FLAIR.lower() in str(new_comment.author_flair_text).lower():
            comment_reply = ""
            bot_comment_id = 0
            counter = 0
            new_comment.submission.comments.replace_more(limit=None)
            for s_comment in new_comment.submission.comments.list():
                if s_comment.author.name == BOT_USERNAME:
                    bot_comment_id = s_comment.id
                if AUTHOR_FLAIR.lower() in str(s_comment.
                                               author_flair_text).lower():
                    counter += 1
                    comment_reply += "[EPIC COMMENT #" + str(counter)\
                        + " - " + s_comment.author.name + "]"\
                        + "(https://www.reddit.com" + s_comment.permalink\
                        + ")\n\n"
            if bot_comment_id == 0:
                bot_comment = new_comment.submission.reply(comment_reply)
                bot_comment.mod.distinguish(sticky=True)
                print("Creating bot's sticky comment: ",
                      new_comment.submission.title)
            else:
                reddit.comment(bot_comment_id).edit(comment_reply)
                print("Editing bot's sticky comment: ",
                      new_comment.submission.title)

reddit = bot_login()
subreddit = reddit.subreddit(SUBREDDIT_NAME)
bot_run(reddit, subreddit)
