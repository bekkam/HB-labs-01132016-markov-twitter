import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    new_string = " ".join(words)
    if len(new_string) < 140:
        return new_string
    else:
        return new_string[:140]

def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    #print most recent tweet to terminal, before posting new tweet
    statuses = api.GetUserTimeLine(id = 4754349372)
    # home_timeline = api.GetHomeTimeLine()
    # print [s.text for s in home_timeline]
    print[s.text for s in statuses]

    status = api.PostUpdate(chains)
    print status.text
    # pass

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]
# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)
string = make_text(chains)
# make_text(chains)

# Your task is to write a new function tweet, that will take chains as input
tweet(string)

def retweet():
    tweet_again = True 
    while tweet_again == True:
        userinput = raw_input("Enter to tweet again [q to quit] > ")
        if userinput == "":
            print "you pressed enter"
            string = make_text(chains)
            tweet(string)
        elif userinput == "q":
            print "Thanks for tweeting; bye now!"
            tweet_again = False
        else:
            print "Sorry, that is not a valid option."
retweet()