import sys
import numpy as np
import random
import subprocess
import pdfkit
from datetime import datetime
import schedule
import time

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

def create_file(template):
  # copy template to 
  # subprocess.run(["cp", "html_template/" + template, "temp/."])

  # template HTML file
  fin = open("html_template/" + template, "rt")

  # Output HTML file
  fout = open("temp/out.html", "wt")

  # For each line in the input file
  for line in fin:
    # write lines in output file
    if "#day#" in line:
      current_day = get_current_day()
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

def send_new_exercise():
  # create PDF file
  file = create_file("template.html")

  # send file to printer
  print("Sending new activity to the printer " + datetime.now().strftime("(%d/%m/%Y)") + "!")
  # SEND

def main():

  schedule.every().day.at("10:00").do(send_new_exercise)
  # schedule.every(1).minutes.do(send_new_exercise)

  while 1:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
  main()