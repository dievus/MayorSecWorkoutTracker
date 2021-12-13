import csv
import os
import os.path
from prettytable import from_csv
from datetime import date
import argparse
import textwrap
import sys
import pandas as pd


def banner():
    print("          _                                       _")
    print("    _  _ | |                                     | | _  _")
    print("   | || || |       MayorSec Exercise Tracker     | || || |")
    print(" =H| || || |========nnnn=============nnnn========| || || |H=")
    print("   |_||_|| |        |  |             |  |        | ||_||_|")
    print("         |_|        /  |     v1.0    |  \        |_|")
    print("                   |   |             |   |")
    print("                   \   (_   /~~~\   _)   /")
    print("                    \    \ ( '_' ) /    /")
    print("                     \    )\  =  /(    /")
    print("                      \   (_)   (_)   /")
    print("                       \ /   ~~~   \ /")
    print("                       (             )")
    print("                        \           /")
    print("                         \         /")
    print("                          )==(O)==(")
    print("                         /         \ ")
    print("                        /____/ \____\ ")
    print("                        /   /   \   \ ")
    print("                       /   /     \   \ ")
    print("                      (   )      (   )")
    print("                      |   |      |   |")
    print("                      |   |      |   |")
    print("                      |___|      |___|")
    print("                      (___)      (___)\n")


def options():
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''Example: python3 workouttracker.py -e
Example: python3 workouttracker.py -r
Example: python3 workouttracker.py -w
'''))
    opt_parser.add_argument(
        '-e', '--enter', help='Enter a workout into the log.', action='store_true')
    opt_parser.add_argument(
        '-r', '--read', help="Reads all lines from the log.", action='store_true')
    opt_parser.add_argument(
        '-w', '--web', help="Read logs from the web.", action='store_true')

    global args
    args = opt_parser.parse_args()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()


def main():
    if args.enter:
        file = 'workouttracker.csv'
        file_exists = os.path.isfile(file)
        if file_exists == False:
            print('\n[!] No log file found. Creating. [!]\n')
            with open(file, 'a+') as csvfile:
                headers = ['Date', 'Exercise',
                           'Time (minutes)', 'Distance', 'kCal Burned' ,'Avg HR', 'Comments']
                writer = csv.DictWriter(
                    csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
                writer.writeheader()
        exercise = input("Enter the exercise you did here: ")
        print(f"\nGreat! You did {exercise} today.\n")
        workout_time = input("How long did you work out for (in minutes)? ")
        print(f"\nGreat! You worked out for {workout_time} minutes today.\n")
        distance = input("If there was a distance, how far did you go? ")
        if distance is not None:
            print(f"\nGreat work! you made it {distance} today.\n")
        elif distance is None:
            distance = 0
        kcal_burned = input("How many calories did you burn? ")
        print(f"\nGreat! You burned {kcal_burned} calories today.\n")
        avg_hr = input("What was your average heartrate during exercise?")
        print(f"\nGreat! Your average heartrate was {avg_hr} beats per minute.\n")
        comments = input("Any comments for today's workout? ")
        print(f"Comment logged - {comments}")
        today = date.today()
        with open(file, 'a+') as file:
            results = (
                f"{today}, {exercise}, {workout_time}, {distance}, {kcal_burned}, {avg_hr}, {comments}\n")
            file.write(results)
        with open("workouttracker.csv", "r") as fp:
            current_workout = from_csv(fp)[0:1]
        print("Workout entered into the log.\n")
        print(current_workout)

    elif args.read:
        file = 'workouttracker.csv'
        file_exists = os.path.isfile(file)
        if file_exists == False:
            print("No log found.")
        if file_exists == True:
            with open(file, 'r') as file:
                z = from_csv(file)
            print("\nPrinting full log results.")
            print(z)

    elif args.web:
        file = 'workouttracker.csv'
        file_exists = os.path.isfile(file)
        if file_exists == False:
            print("No log found. Exiting")
            sys.exit()
        a = pd.read_csv(file)
        pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
        html_string = '''
        <html>
        <head><title>MayorSec Workout Tracker</title></head>
        <link rel="stylesheet" type="text/css" href="df_style.css"/>
        <body>
        <p>MayorSec Workout Tracker</p>
        {table}
        </body>
        </html>
       '''
        with open('workouttracker.html', 'w') as f:
            f.write(html_string.format(table=a.to_html(classes='mystyle')))
            print("\nOutputting log named workouttracker.html to current directory.\n")
            print("Opening log in browser. Goodbye.\n")
        os.system("start workouttracker.html")
        sys.exit()


if __name__ == "__main__":
    try:
        banner()
        options()
        main()
    except KeyboardInterrupt:
        quit()
