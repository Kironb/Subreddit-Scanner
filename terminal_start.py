import signal
import sys

from connectors.generic import login, create_feed, backup_tofeed, mimic_feed, save_hot, unsave
from connectors.terminal import Terminal

REDDIT_URL = "https://www.reddit.com"


# a signal handler to handle shutdown of the bot
def signal_handler(sig, frame):
    print('Closing bot...')
    sys.exit(0)


def run_bot():
    """ Method that will run the Subreddit-Scanner bot """
    reddit = login()
    print("Logged in successfully...")
    terminal_obj = Terminal()
    # runs the program indefinitely
    while True:
        # fetches the command
        command = input("\nWhat would you like to do today?\n"
                        "1. (c)reate\n"
                        "2. (b)ackup\n"
                        "3. (m)imic\n"
                        "4. (s)ave hot items\n"
                        "5. (u)nsave\n"
                        "6. (q)uit\n")

        # performs the action based on the command given
        if command == "c" or command == "create" or command == "1":
            create_feed(reddit, terminal_obj)
        elif command == 'b' or command == "backup" or command == "2":
            backup_tofeed(reddit, terminal_obj)
        elif command == "m" or command == "mimic" or command == "3":
            mimic_feed(reddit, terminal_obj)
        elif command == "s" or command == "save hot items" or command == "4":
            save_hot(reddit, terminal_obj)
        elif command == "u" or command == "unsave" or command == "5":
            unsave(reddit, terminal_obj)
        elif command == "q" or command == "quit" or command == "6":
            sys.exit(0)
        else:
            print("Invalid command given! Please choose one of the given options")


if __name__ == '__main__':
    # sets up signal to be recognized by user
    signal.signal(signal.SIGINT, signal_handler)
    print('To close the bot please press Ctrl + C')
    run_bot()
