import sys
import numpy as np
import random
import pdfkit
from datetime import datetime
import schedule
import time
import argparse
import subprocess

def generate_exercise():
  min = 100
  max = 99999

  # generate first number
  n1 = np.ceil(np.random.uniform(min, max))

  # generate operation
  operations = [" + ", " - ", " X "]
  op = random.sample(operations, 1)[0]

  # generate second number
  if op == " X ":
    n2 = np.ceil(np.random.uniform(min, np.minimum(n1, 999)))
  else:
    n2 = np.ceil(np.random.uniform(min, n1))

  return str(n1)[:-2] + op + str(n2)[:-2] + " ="

def get_current_day():
  return datetime.now().strftime("%d/%m/%Y")

def create_file(template, current_day):
  # template HTML file
  fin = open("html_template/" + template, "rt")

  # Output HTML file
  fout = open("temp/out.html", "wt")

  # For each line in the input file
  for line in fin:
    # write lines in output file
    if "#day#" in line:
      fout.write(line.replace("#day#", current_day))
    elif "#exercise#" in line:
      exercise = generate_exercise()
      fout.write(line.replace("#exercise#", exercise))
    else:
      fout.write(line)

  # Close input and output files
  fin.close()
  fout.close()

  # convert output file to pdf
  pdfkit.from_file('temp/out.html', 'temp/out.pdf') 
  
  return

def print_file(path):
  subprocess.run(["lpr", "temp/out.pdf"])

def send_new_exercise(current_day = get_current_day()):
  # create PDF file
  file = create_file("template.html", current_day)

  # send file to printer
  print("Sending new activity to the printer (" + current_day + ")!")
  # SEND
  print_file('temp/out.pdf')

def main():
  # setup parser
  parser = argparse.ArgumentParser(description = 'Creates math exercises regularly to be printed or on demand.')
  parser.add_argument('--mode', type = str, nargs = '+',
                      help = '0: prints on schedule at specified time (default: 10:00) \n1: prints immediately with specified day (default: today)')
  parser.add_argument('--time', type = str, nargs = '+',
                      help = 'time (--:--) at which a new sheet will be printed on schedule (mode 0 required)')
  parser.add_argument('--day', type = str, nargs = '+',
                      help = 'day to be displayed on sheetto be immediately printed (mode 1 required)')
  args = parser.parse_args()

  if (args.mode[0] == '0'): # print on schedule
    # get time
    if args.time is None: # if no argument was given
      time_str = "10:00"
    else:
      time_str = args.time[0]

    print("Setting Schedule: Everyday at " + time_str)
    schedule.every().day.at(time_str).do(send_new_exercise)

    while 1:
      schedule.run_pending()
      time.sleep(1)
  elif (args.mode[0] == '1'): # print immediately
    if args.day is None: # if no argument was given
      send_new_exercise()
    else:
      send_new_exercise(args.day[0])
  else:
    print("Incorrect mode.")


if __name__ == '__main__':
  main()