import pandas as pd

def read_file(path):
    f = open(path, 'r')
    string = f.read()
    f.close()
    return string

def write_file(path, string):
    f = open(path, 'w')
    f.write( string )
    f.close()
    return string

# 1. Load Submissions
df_submissions = pd.read_csv( 'submissions.csv' ) 

# 2. Populate submissions_template
submission_template = read_file( './templates/submission.html' ) 
submission = ''
keys = [ 'project_name', 'github', 'youtube', 'company']

ind = 0
submission += '<table>\n'
while ind < len(df_submissions):
    submission += '<tr>\n'

    for _ in range(4):
        kwargs = { key: df_submissions.loc[ind,key] for key in keys }
        submission += '<td>\n' + submission_template.format( **kwargs ) + '\n</td>\n'
        ind += 1

    submission += '</tr>\n'
submission += '</table>\n'


# 3. Populate submissions template
submissions_template = read_file( './templates/submissions.md' ) 
submissions = submissions_template.format( submission=submission )

# 4. Populate README.md
readme = read_file('README.md')
readme_lines = readme.split('\n')

prompt_line = readme_lines.index( '# Hackathon Prompt' )
try:
    submissions_line = readme_lines.index( '# Submissions' )
except ValueError :
    submissions_line = None

# if submissions already exist, delete them and restart
if submissions_line != None:
    del readme_lines[ submissions_line : prompt_line ]
    prompt_line = submissions_line

# add all the submissions to the file
submissions_lines = submissions.split('\n')
submissions_lines.reverse()
for line in submissions_lines:
    readme_lines.insert( prompt_line, line )

write_file( 'README.md', '\n'.join(readme_lines) )