from datetime import *
import datetime
import prettytable
import xlsxwriter
import urllib, json

today = datetime.date.today()

#Input member launchpad id here.
members = ["hieulq", "duonghq", "tovin07", "kiennt2609", "daidv", "namnh"]
maps = {"hieulq": "Hieu", "duonghq": "Duong", "tovin07": "Vinh", "kiennt2609": "Kien", "daidv": "Dai", "namnh": "Nam"}
#Input target
review_target = 1219
commit_target = 213

# Create a new Excel file and add a worksheet.
year = today.year
month = today.month
day = today.day
a = date(year, month, day).isocalendar()[1]
a1 = date(2017, 12, 31).isocalendar()[1]
b = date(2018, 3, 2).isocalendar()[1]
if a > b:
    week = (a1 - a) + b
else:
    week = b - a
# Cal start date and end date of a week
def _range_date_of_week(year, week):
    d = date(year,1,1)
    if(d.weekday()>3):
        d = d+timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    start = str(d + dlt)
    end = str(d + dlt + timedelta(days=4))
    return start, end

filename = 'FVL_UC_Contribution_Summarization_R-' + str(week) + '.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()
def output_xlsx (member, reviews, commits, index, sum=None):
    # Widen the first column to make the text clearer.
    worksheet.set_column('E:E', 30)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 15)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': False})
    bold.set_border()
    bold.set_font('Times New Roman')
    bold.set_font_size(13)
    bold_color = workbook.add_format({'bold': False, 'font_color': 'black'})
    bold_color.set_font('Times New Roman')
    bold_color.set_font_size(13)
    bold_color.set_border()
    bold_color.set_pattern(1)
    bold_color.set_bg_color('yellow')
    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font': 'Times New Roman',
        'font_size': 13})

    row = 13 + index*4
    # Write some simple text.
    if sum:
        worksheet.merge_range('D' + str(row - 5) + ':J'  + str(row - 5),
                              'Week (From ' + _range_date_of_week(year, a)[0] +
                              ' to ' + _range_date_of_week(year, a)[1] + ' )', merge_format)
        worksheet.merge_range('D' + str(row - 4) + ':D'  + str(row - 2), 'Team', merge_format)
        worksheet.write('E' + str(row - 4), 'R-' + str(week), bold)
        worksheet.write('E' + str(row - 3), 'Reviews (Until 2018/02/23)', bold)
        worksheet.write('E' + str(row - 2), 'Commits (Until 2018/01/26)', bold)
        worksheet.write('F' + str(row - 4), 'Target', bold)
        worksheet.write('G' + str(row - 4), 'Actual', bold)
        worksheet.write('H' + str(row - 4), 'Target remain', bold)
        worksheet.write('I' + str(row - 4), 'Actual remain', bold)
        worksheet.write('J' + str(row - 4), 'Status', bold)
        worksheet.write('F' + str(row - 3), review_target, bold)
        worksheet.write('F' + str(row - 2), commit_target, bold)
        worksheet.write('G' + str(row - 3), reviews, bold_color)
        worksheet.write('G' + str(row - 2), commits, bold_color)
        m1 = review_target - (review_target/25)*(26-week) #25 is total week of the cycle
        n1 = commit_target - (commit_target/21)*(26-week) #21 is the week of RC1
        m2 = review_target - reviews
        n2 = commit_target - commits
        worksheet.write('H' + str(row - 3), round(m1), bold)
        worksheet.write('H' + str(row - 2), round(n1), bold)
        worksheet.write('I' + str(row - 3), m2, bold)
        worksheet.write('I' + str(row - 2), n2, bold)
        worksheet.write('J' + str(row - 3), round(m1 - m2), bold_color)
        worksheet.write('J' + str(row - 2), round(n1 - n2), bold_color)
    else:
        worksheet.merge_range('D' + str(row) + ':D'  + str(row + 2), member, merge_format)
        worksheet.write('E' + str(row ), '', bold)
        worksheet.write('E' + str(row + 1), 'Reviews', bold)
        worksheet.write('E' + str(row + 2), 'Commits', bold)
        worksheet.write('F' + str(row), 'Target', bold)
        worksheet.write('G' + str(row), 'Actual', bold)
        worksheet.write('H' + str(row), 'Target remain', bold)
        worksheet.write('I' + str(row), 'Actual remain', bold)
        worksheet.write('J' + str(row), 'Status', bold)
        q = review_target / len(members)
        p = commit_target / len(members)
        q1 = q - (q/25)*(26 - week)
        p1 = p - (p/21)*(26 - week)
        q2 = q - reviews
        p2 = p - commits
        worksheet.write('F' + str(row + 1), q, bold)
        worksheet.write('F' + str(row + 2), p, bold)
        worksheet.write('G' + str(row + 1), reviews, bold_color)
        worksheet.write('G' + str(row + 2), commits, bold_color)
        worksheet.write('H' + str(row + 1), round(q1), bold)
        worksheet.write('H' + str(row + 2), round(p1), bold)
        worksheet.write('I' + str(row + 1), q2, bold)
        worksheet.write('I' + str(row + 2), p2, bold)
        worksheet.write('J' + str(row + 1), round(q1-q2), bold_color)
        worksheet.write('J' + str(row + 2), round(p1-p2), bold_color)
# Create an new Excel file and add a worksheet...End

patches = prettytable.PrettyTable(["UC team results on the community summary", str(today) + " (R-" + str(week) + ")"])
table = prettytable.PrettyTable(["Team/Members", "Reviews", "Commits"])
table.align = "l"

team_stats_patches = 0
team_stats_commits = 0
team_stats_reviews = 0
i = 0
for member in members:
    url = "http://stackalytics.com/api/1.0/contribution?release=queens&company=fujitsu&user_id=" + member
    member_url = urllib.urlopen(url)
    try:
        member_stats = json.loads(member_url.read())
    except ValueError:
        print("Something wrong with member " + member)
        continue
    member_stats_patches = member_stats['contribution']['patch_set_count']
    member_stats_commits = member_stats['contribution']['commit_count']
    member_stats_reviews = (
        member_stats['contribution']['marks']['-1'] +
        member_stats['contribution']['marks']['1'] +
        member_stats['contribution']['marks']['-2'] +
        member_stats['contribution']['marks']['2'])

    team_stats_patches += member_stats_patches
    team_stats_reviews += member_stats_reviews
    team_stats_commits += member_stats_commits

    table.add_row([maps.get(member), member_stats_reviews, member_stats_commits])

    output_xlsx(maps.get(member), member_stats_reviews, member_stats_commits, i)
    i += 1
    if i == len(members):
        output_xlsx('Team', team_stats_reviews, team_stats_commits, 0, sum=True)

workbook.close()
patches.add_row(["Total patches uploaded", team_stats_patches])
print(patches)
table.add_row(["*** Team ***", team_stats_reviews, team_stats_commits])
print(table)
