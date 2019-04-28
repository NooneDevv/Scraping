import requests
import string
import threading
from random import choice
from ytScanner import DbUtils
from ytScanner import StopWatch as s

DB_PASS = ""
DB_USERNAME = ""
DB_IP = ""
DB_NAME = ""
MISSES_TABLE = "misses"
VERIFY = '<meta itemprop="unlisted" content="True">'
BASE_URL = "https://www.youtube.com/watch?v="
POSSIBLE_CHARS = string.digits + string.ascii_letters

thread_count = int(input("How many threads would you like to run?\n"))
running = True

miss_count = 0
hit_count = 0
misses = []

db = DbUtils.DbUtils(DB_USERNAME, DB_PASS, DB_IP, DB_NAME)
sw = s.StopWatch()


def run():
    """Checks randomly generated links"""
    global miss_count, hit_count, misses
    while running:
        gen = generate_url()
        content = requests.get(BASE_URL + gen).text

        if VERIFY in content:
            print("HIT! {}".format(gen))
            hit_count += 1
            db.append_hit(gen)
        else:
            misses.append(gen)
            miss_count += 1


def send_misses():
    """Sends the misses array to the db"""
    global misses
    while running:
        if len(misses) >= thread_count * 5:
            db.insert_many(MISSES_TABLE, misses)
            misses = []
            print("Elapsed time: " + sw.get_elapsed_time() +
                  "\nChecks per hour: " +
                  str(int((hit_count+miss_count)/int(sw.get_elapsed_time_seconds()) * 3600)) +
                  "\nMiss count: " + str(miss_count) +
                  "\nHit count: " + str(hit_count))


def generate_url():
    """Generates a random ending of a link"""
    return "".join(choice(POSSIBLE_CHARS) for i in range(11))


def start_threads():
    """Starts the threads"""
    threading.Thread(target=send_misses).start()
    for x in range(0, thread_count-1):
        print("Starting threads")
        t = threading.Thread(target=run)
        t.start()


start_threads()
