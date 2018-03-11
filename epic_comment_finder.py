import praw
import config
import time

SUBREDDIT_NAME = "FortNiteBR"
#LINK_FLAIR = "epic comment"
AUTHOR_FLAIR = "epic games"

def bot_login():
    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    password=config.password,
                    username=config.username,
                    user_agent=config.user_agent)
    return r

def bot_run(reddit, subreddit):
    submission_visited = []
    for new_comment in subreddit.comments(limit=25):
        if AUTHOR_FLAIR in str(new_comment.author_flair_text).lower():
            comment_reply = ""
            bot_comment_id = 0
            counter = 0
            if new_comment.submission.id not in submission_visited:
                submission_visited.append(new_comment.submission.id)
                new_comment.submission.comments.replace_more(limit=None)
                for s_comment in new_comment.submission.comments.list():
                    if s_comment.author.name == "EpicCommentFinder":
                        bot_comment_id = s_comment.id
                    if AUTHOR_FLAIR in str(s_comment.author_flair_text).lower():
                        counter += 1
                        comment_reply += "[EPIC COMMENT #" + str(counter) + " - " + s_comment.author.name + "]" + "(https://www.reddit.com" + s_comment.permalink + ")\n\n"
                if bot_comment_id == 0:
                    bot_comment = new_comment.submission.reply(comment_reply)
                    bot_comment.mod.distinguish(sticky=True)
                    print("Creating sticky comment: ", new_comment.submission.title)
                else:
                    reddit.comment(bot_comment_id).edit(comment_reply)
                    print("Editing sticky comment: ", new_comment.submission.title)
    print("Bot in rest for 10 seconds")
    time.sleep(10)

while True:
    reddit = bot_login()
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    bot_run(reddit, subreddit)
