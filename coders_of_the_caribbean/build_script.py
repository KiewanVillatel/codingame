import os


def handle_file(file, outfile):
  with open(file, 'r') as in_file:
    for line in in_file:
      if 'from ' in line:
        continue
      else:
        outfile.write(line)
    outfile.write('\n')


with open('./script.py', 'w') as outfile:
  handle_file('./global_vars.py', outfile)
  for dir in ['model', 'services', 'actions']:
    for subdir, dirs, files in os.walk(dir):
      for file in files:
        if file != '__init__.py':
          handle_file(os.path.join(subdir, file), outfile)
  handle_file('./coders_of_the_caribbean.py', outfile)
