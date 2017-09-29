from __future__ import with_statement  #imports stuff from python 3.x
import hashlib
import re
import sys
import argparse
import os

#takes in stuff from command line. 
parser = argparse.ArgumentParser()
parser.add_argument("srcfile", help="Name of the source file to be hashed")
parser.add_argument("-email_column", type=int, default=0, help="Column that contains the email. Defailt is the first column")
parser.add_argument("-hashed_suffix", default="_hashed.csv", help="Suffix for the hashed file. Default is '_hashed'")
parser.add_argument("-delimiter", default=",", help="Column delimiter for the file. Default is comma")
args = parser.parse_args()


def normalize(s, is_name=False):
  ret = s.strip().lower().replace(' ', '')
  if is_name:
    # strip all non a-z letters
    ret = re.sub(r'[^a-zA-Z]', '', ret)
  return ret

#sets up variables for arguments
source_file = args.srcfile
delimiter = args.delimiter
source_filename_without_extension = os.path.splitext(args.srcfile)[0]
hashed_filename_suffix = args.hashed_suffix
hashed_filename = source_filename_without_extension + hashed_filename_suffix
email_column = args.email_column

#files
in_handler = open(source_file, 'r')
out_handler = open(hashed_filename, 'w')

#hashes each line in the file and writes it to the new file. 
for line in in_handler:
  fields = line.split(delimiter)
  email = normalize(fields[email_column])
  hashed_email = hashlib.sha256(email.encode("UTF-8")).hexdigest()
  fields[email_column] = hashed_email
  output_line = delimiter.join(fields)
  out_handler.write(output_line + '\n')
in_handler.close()
out_handler.close()
