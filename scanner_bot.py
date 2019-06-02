import configparser
import praw
from prawcore.exceptions import Conflict, BadRequest
import signal
import sys
from pprint import pprint

REDDIT_URL = "https://www.reddit.com"

# a signal handler to handle shutdown of the bot
def signal_handler(sig, frame):
    print('Closing bot...')
    sys.exit(0)

def login():
    """Method used to login onto Reddit and obtain a praw.Reddit instance using the configuration within config.ini"""
    # utilizes a ConfigParser object to parse through the config.ini file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # fetches the required config options in order to ensure that the bot can function
    user_agent = config["DEFAULT"]["user_agent"]
    client_id = config["DEFAULT"]["client_id"]
    client_secret = config["DEFAULT"]["client_secret"]
    username = config["DEFAULT"]["username"]
    password = config["DEFAULT"]["password"]

    # verifies that none of the required configuration options for login were left blank
    if '' in [user_agent, client_id, client_secret, username, password]:
        raise Exception("One or more of the required configuration options were left empty")

    # returns the created Reddit instance
    return praw.Reddit(user_agent=user_agent,
                       client_id=client_id,
                       client_secret=client_secret,
                       username=username,
                       password=password)


def createMulti(reddit):
    multi = None
    feed_name = None

    while multi is None:
        feed_name = input("\nWhat would you like to name this new feed? (limit 50 characters)\n")
        # the name is not allowed to be longer than 50 characters (per Reddit custom feed name specifications)
        if len(feed_name) > 50:
            print("The maximum custom feed name length is 50 characters. The name you chose was %d characters long. Please try again" % len(feed_name))
            continue
        # and also makes sure that the custom feed created doesn't already exist for the user
        try:
            multi = reddit.multireddit.create(display_name=feed_name, subreddits=[])
            break
        except Conflict:
            print("The custom feed with that name already exists on your account. Please choose a different name")
            continue
    print("Successfully created an empty custom feed named %s\n" % feed_name)
    return multi


def getUser():
    feed_name = input("\nWhat is the name of the feed you want to mimic?\n")
    # utilizes a ConfigParser object to parse through the config.ini file to get the username
    config = configparser.ConfigParser()
    config.read("config.ini")

    return config["DEFAULT"]["username"]


def read_subreddits():
    """Method that reads in a list of subreddits from the user to be added to a custom feed"""
    # starts by asking the user for the number of subreddits they want to add
    subreddit_count = None
    while subreddit_count is None:
        try:
            subreddit_count = int(input("Please enter the number of subreddit(s) you want to add to your collection!\n"))
            break
        # if the user input is not a valid number, then it keeps re-prompting the user
        except ValueError:
            print("Please enter an integer value!\n")
            continue

    # next, reads the number of lines for each subreddit and returns the list read
    subreddit_list = []
    print("\nPlease enter", subreddit_count, "subreddits, each followed by a new line.")
    for i in range(0, subreddit_count):
        # reads in a line the user enters and stores it in an array
        subreddit_list.append(input(""))
    return subreddit_list


def create_feed(reddit):
    """Method that creates a custom feed that the user requests"""
    # starts by prompting the user for a name for the custom feed
    multi = createMulti(reddit)

    # next, the user is prompted for all the subreddits they want to add to the feed
    subreddit_list = read_subreddits()
    print("\nAdding the chosen subreddits to the custom feed\n")
    for subreddit in subreddit_list:
        # once the list of subreddits is fetched from the user, each of them is added to feed one by one
        try:
            multi.add(subreddit)
            print("Successfully added the subreddit '%s' to the feed" % subreddit)
        except BadRequest:
            # if adding the subreddit fails due to a BadRequest, it means that the subreddit provided wasn't valid
            # so the appropriate error message is printed
            print("Failed to add the subreddit '%s' to the feed because it is not a valid subreddit" % subreddit)

    # finally, the link to the custom feed is output into the console so they can readily access it
    print("\nFinished adding the given subreddits to the custom feed. In order to access it, visit:\n%s%s" % (REDDIT_URL, multi.path))

def mimic_feed(reddit):
    feed_name = input("\nWhat feed would you like to mimic?\n")

    multi = reddit.multireddit(getUser, feed_name)

    '''
    subreddit_list = multi.subreddits
    for subreddit  in subreddit_list:
        print("Successfully found '%s'" % subreddit)
    '''

    print("Functionality not yet fully implemented")
    #check if it is a valid feed name

def backup_tofeed(reddit):

    multi = createMulti(reddit)
    print("Now copying subreddits over...")

    userSubreddits = reddit.user.subreddits()
    for subreddit in userSubreddits:
        multi.add(subreddit)
        print(subreddit)

    print("\nSuccessfully backed up subreddits! In order to access the backup visit:\n%s%s" % (REDDIT_URL, multi.path))


def run_bot():
    """ Method that will run the Subreddit-Scanner bot """
    reddit = login()
    print("Logged in successfully...")
    # runs the program indefinitely
    while True:
        # fetches the command
        command = input("\nWhat would you like to do today?\n"
                        "1. (c)reate\n"
                        "2. (b)ackup\n"
                        "3. (m)imic\n"
                        "4. (q)uit\n")

        # performs the action based on the command given
        if command == "c" or command == "create":
            create_feed(reddit)
        elif command == 'b' or command == "backup":
            backup_tofeed(reddit)
        elif command == "m" or command == "mimic":
            mimic_feed(reddit)
        elif command == "q" or command == "quit":
            sys.exit(0)
        else:
            print("Invalid command given! Please choose one of the given options")


if __name__ == '__main__':
    # sets up signal to be recognized by user
    signal.signal(signal.SIGINT, signal_handler)
    print('To close the bot please press Ctrl + C')
    run_bot()
    signal.pause()  # this is currently here to show the functionality of the signal signal_handler
    # when we actually make the bot, it will run indefintely so this pause will not be necessary
