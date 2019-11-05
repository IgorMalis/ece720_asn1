import requests
from pandas import read_csv
import numpy as np
import time

# Read in Post ID's retrieved from Stack Exchange Data Explorer
question_ids = read_csv('./data/QueryResults.csv').values[:,0]

# Split into 10 chunks with < 100 questions per array
split_num = np.array_split(question_ids, 10)
split_str = []

for i in split_num:
    split_str.append( ';'.join( str(x) for x in i ) )

# Write file headers
with open('./data/allPosts.tsv', 'w+') as output:
    output.write('question_id\tanswer_id\tuser_id\tpost_type\tlink\tscore\tcreated\tlast_activity\ttitle\tbody_markdown\tis_answered\tis_accepted\tanswer_count\tview_count\tup_vote_count\tdown_vote_count\ttags\n')
with open('./data/allPosts-metaData.tsv', 'w+') as output:
    output.write('question_id\tanswer_id\tuser_id\tpost_type\n')
with open('./data/askerAnswerer_nodes.tsv', 'w+') as output:
    output.write('id\n')
with open('./data/askerAnswerer_edges.tsv', 'w+') as output:
    output.write('from\tto\tweight\ttype\n')

users = []

# Save question data to tsv files
for chunk in split_str:
    url = 'https://api.stackexchange.com/2.2/questions/{}?pagesize=100&site=stackoverflow&filter=!0V-ZwUEu0wMhJq3YDwaaC_)*r'.format(chunk)
    r = requests.get(url = url)
    data = r.json()
    for item in data['items']:
        with open('./data/allPosts.tsv', 'a+') as output:
            output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                item['question_id'],
                '',
                item['owner']['user_id'] if item['owner']['user_type'] == 'registered' else item['owner']['display_name'],
                'question',
                item['link'],
                item['score'],
                time.ctime(item['creation_date']),
                time.ctime(item['last_activity_date']),
                item['title'],
                item['body_markdown'].replace('\r\n', '\\n').replace('\t', '\\t'),
                item['is_answered'],
                '',
                item['answer_count'],
                item['view_count'],
                item['up_vote_count'],
                item['down_vote_count'],
                ';'.join(item['tags'])
            ))
        with open('./data/allPosts-metaData.tsv', 'a+') as output:
            output.write('{}\t{}\t{}\t{}\n'.format(
                item['question_id'],
                '',
                item['owner']['user_id'] if item['owner']['user_type'] == 'registered' else item['owner']['display_name'],
                'question'
            ))

        users.append(item['owner']['user_id'] if item['owner']['user_type'] == 'registered' else item['owner']['display_name'])

        if 'answers' in item:
            for answer in item['answers']:
                with open('./data/allPosts.tsv', 'a+') as output:
                    output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                        answer['question_id'],
                        answer['answer_id'],
                        answer['owner']['user_id'] if answer['owner']['user_type'] == 'registered' else answer['owner']['display_name'],
                        'answer',
                        '',
                        answer['score'],
                        time.ctime(answer['creation_date']),
                        time.ctime(answer['last_activity_date']),
                        '',
                        answer['body_markdown'].replace('\r\n', '\\n').replace('\t', '\\t'),
                        '',
                        answer['is_accepted'],
                        '',
                        '',
                        answer['up_vote_count'],
                        answer['down_vote_count'],
                        ';'.join(item['tags'])
                    ))
                with open('./data/allPosts-metaData.tsv', 'a+') as output:
                    output.write('{}\t{}\t{}\t{}\n'.format(
                        answer['question_id'],
                        answer['answer_id'],
                        answer['owner']['user_id'] if answer['owner']['user_type'] == 'registered' else answer['owner']['display_name'],
                        'answer'
                    ))

                with open('./data/askerAnswerer_edges.tsv', 'a+') as output:
                    output.write('{}\t{}\t{}\t{}\n'.format(
                        item['owner']['user_id'] if item['owner']['user_type'] == 'registered' else item['owner']['display_name'],
                        answer['owner']['user_id'] if answer['owner']['user_type'] == 'registered' else answer['owner']['display_name'],
                        '1',
                        'askerAnswerer'
                    ))

                users.append(answer['owner']['user_id'] if answer['owner']['user_type'] == 'registered' else answer['owner']['display_name'])

# Remove duplicate users
users = list(set(users))

with open('./data/askerAnswerer_nodes.tsv', 'a+') as output:
    for user in users:
        output.write('{}\n'.format(user))
