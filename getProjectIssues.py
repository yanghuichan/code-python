import argparse

import gitlab
import pdb
import csv
import os
import json

import requests




def downloadjson(url):
    jsondata = []
    try:
        res = requests.get(url)
        jsondata = json.loads(res.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return jsondata

def writecsvhead(csvfilepath):
    csv_filed = ['id', 'title', 'web_url', 'description', 'model', 'issue_Level', 'fixed','labels04','other_labels', 'state', 'created_at',
                 'updated_at','author', 'assigneer']
    with open(csvfilepath, 'w', newline='' ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_filed)

def writecsvdata(csvfilepath,issues_data):
    try:
        json_filed = ['iid', 'title', 'web_url', 'description', 'labels', 'state', 'created_at', 'updated_at', 'author',
                      'assignee']
        # csv_filed = ['id', 'title', 'web_url', 'description', 'labels01', 'labels02', 'labels03', 'state', 'created_at','updated_at', 'assigneer']
        labels01 = ['UZFS', 'UZL', 'Journal', 'CLI']
        labels02 = ['Level-Blocker', 'Level-Critical', 'Level-Major', 'Level-Minor']
        labels03 = ['Stat-Fixed']
        labels04 = ['Type-Bug', 'Not-Bug']
        labels05 = []
        issues = []
        print("yhc 22len:", len(issues_data), type(issues_data))
        for data in issues_data:
            data_value = []
            for col in json_filed:
                if col == 'labels':
                    csv_lables01, csv_lables02, csv_lables03, csv_lables04, csv_lables05 = [], [], [], [], []
                    for label in data[col]:
                        if label in labels01:
                            csv_lables01.append(label)
                        elif label in labels02:
                            csv_lables02.append(label)
                        elif label in labels03:
                            csv_lables03.append(label)
                        elif label in labels04:
                            csv_lables04.append(label)
                        else:
                            csv_lables05.append(label)
                    csv_lables01 = (",").join(str(i) for i in csv_lables01)
                    data_value.append( csv_lables01)
                    csv_lables02 = (",").join(str(i) for i in csv_lables02)
                    data_value.append( csv_lables02)
                    csv_lables03 = (",").join(str(i) for i in csv_lables03)
                    data_value.append(csv_lables03)
                    csv_lables04 = (",").join(str(i) for i in csv_lables04)
                    data_value.append(csv_lables04)
                    csv_lables05 = (",").join( str( i ) for i in csv_lables05)
                    data_value.append(csv_lables05)
                    continue
                elif col == 'assignee':
                    if data[col]:
                        assigneer = data[col]['name']
                        data_value.append(assigneer)
                    else:
                        data_value.append('')
                    continue
                elif col == 'author':
                    author_name = data[col]['name']
                    data_value.append(author_name)
                    continue
                elif col in ['created_at', 'updated_at']:
                    data[col] = (data[col])[0:(data[col]).rfind('T', 1)]
                    data_value.append(data[col])
                    continue
                data_value.append(data[col])
            issues.append(data_value)
        write2csv(csvfilepath, issues)
    except Exception as e:
        raise SystemExit( e )



def write2csv(csvfilepath, issues):
    with open(csvfilepath, 'a+', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(issues)

def get_project_issues (project_url, token,csvfilepath ):
    per_page = 100
    writecsvhead(csvfilepath)
    try:
        issues_list = []
        index = 1
        while True:
            issues_url = project_url + "issues?private_token={}&state=all&order_by=created_at&per_page={}&page={}".format(token,per_page, index)
            print("issues_url:%s", issues_url)
            res = requests.get(issues_url)
            print("res.status_code", res.status_code,requests.codes.ok)
            if res.status_code == requests.codes.ok:
                issues_data = json.loads(res.text)
                if len(issues_data) > 0 and index < 5:
                    #issues_list.append(issues_data)
                    writecsvdata(csvfilepath, issues_data)
                    print("Got 100 issues from page {}".format(index))
                    index = index + 1
                else:
                    print("Get all issues successfully")
                    break
            else:
                print("Stop to get issues due to {}".format(res.text))
                break

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def writeToCvs(issues_list,csvFilePath):
    headers = ["Id", "IssueId", "Title", "Description", "State", "web_url", 'author', 'assignee', 'created_at',
               'updated_at']
    with open(csvFilePath, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # pdb.set_trace()
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(issues_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('-p', '--id', help="gitlab project id")
    # parser.add_argument('-t', '--token', help="gitlab personal access token")
    # parser.add_argument('-o', '--dir', help="out put dir")

    args = parser.parse_args()

    args.id = 83
    args.token = "ubTajrFtjpH_go1Cyh5r"
    args.dir = "out"
    per_page = 100

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    base = "http://172.20.8.46/api/v4/"
    # 当然你也可以自建gitlab
    filePath = 'C:\\workspace\\code\\GetIssues\\yhc\\BCStore.csv'
    gurl = base + "projects/{}/".format(args.id)
    #gurl = base + "software-bugzilla/bcstore/".format(args.id)
    get_project_issues(gurl, args.token, filePath)


