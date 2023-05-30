from bs4 import BeautifulSoup
import json
import re
file = open("AN 100-114.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
QUESTION_TITTLE = "Short Answer Type Questions-"
titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)
next_all = soup.find_all(id="preview-content")
css_styles = """
.start-question {
    color: red;
    font-weight: bold;
}
.start-answer {
    color: green;
    font-weight: bold;
}
"""
style_tag = soup.new_tag('style')
style_tag.string = css_styles
soup.head.append(style_tag)

# Pre-Process For Question
for child in next_all[0].children:
    if "Q. " in child.text:
        if not child.text.startswith("Q. "):
            div_split = str(child).split("Q. ")
            insert_stringOne =  f"{div_split[0]}</div><br><div>Q. {div_split[1]}"
            new_soup = BeautifulSoup(insert_stringOne, 'html.parser')
            child.replace_with(new_soup)
            
for each in next_all[0].children:
    if each.text.startswith('Q.') or each.text.startswith('Q. '):
        each['class'] = each.get('class', []) + ['start-question']

# Pre-Process For Answer
for ans_child in next_all[0].children:
    if "Ans." in ans_child.text:
        if not ans_child.text.startswith("Ans."):
            div_split = str(ans_child).split("Ans.")
            # ["<div asdasdasd ", "asdasdasd ></div>"]
            insert_ans_stringOne =  f"{div_split[0]}</div><br><div>Ans. {div_split[1]}"
            ans_new_soup = BeautifulSoup(insert_ans_stringOne, 'html.parser')
            ans_child.replace_with(ans_new_soup)

for ans_each in next_all[0].children:
    if ans_each.text.startswith('Ans.') or ans_each.text.startswith('Ans. '):
        ans_each['class'] = ans_each.get('class', []) + ['start-answer']

# Collecting Questions
next_all_tags = soup.find_all('div', class_=["start-question"])
Total_Que_list = []
for each_Que_ans in next_all_tags:
    Questions = []
    Question_list = []
    Answer_list = []
    Question_list.append(each_Que_ans)
    find_next = each_Que_ans.find_next_sibling()
    count = 0
    is_answer_mode = False
    while find_next is not None:
        if "start-answer" in find_next.get('class', []):
            is_answer_mode = True
        elif "start-question" in find_next.get('class', []):
            break
        if is_answer_mode:
            Answer_list.append(find_next)
        else:
            Question_list.append(find_next)
        find_next = find_next.find_next_sibling()
    Total_Que_list.append([Question_list, Answer_list])
        #
        # if "start-question" not in find_next.get('class', []) and "start-answer" not in find_next.get('class', []):
        #     Question_list.append(find_next)
        #     find_next = find_next.find_next_sibling()
        # elif "start-answer" in find_next.get('class', []):
        #     Answer_list.append(find_next)
        #     find_next = find_next.find_next_sibling()
        #     while find_next is not None:
        #         if "start-question" not in find_next.get('class', []) and "start-answer" not in find_next.get('class', []):
        #             Answer_list.append(find_next)
        #             find_next = find_next.find_next_sibling()
        #         else:
        #
        #             count = count + 1
        #             break
        #     Questions.append(Question_list)
        #     Questions.append(Answer_list)
        #     break
        # else:
        #     break
    # if count == 0:
    #     Questions.append(Question_list)
    #     Questions.append(Answer_list)
    # Total_Que_list.append(Questions)

print(len(Total_Que_list))
All_question = []
for Que_no in range(2,3):#len(Total_Que_list)):
    print(f"Question {Que_no}")
    print(Total_Que_list[Que_no][0])
    print(f"Answer {Que_no}")
    print(Total_Que_list[Que_no][1])










    
#     parsed_question = []
#     Dict = {}
#     Dict['Question'] = Total_Que_list[Que_no][0]
#     Dict['Answer'] = Total_Que_list[Que_no][1]
#     All_question.append(Dict)
#
# out_File = open("OswalQuetions.json", "w")
# json.dump(All_question, out_File, indent=6)
# print(out_File)









# Total_Que_list = []
# Answer = []
# count = 0
# next_all_tags = soup.find_all('div', {"class":"start-question"})
# print(len(next_all_tags))
# for each_Que_ans in next_all_tags:
#     Questions = []
#     Question_list = []
#     Answer_list = []
#     Question_list.append(each_Que_ans)
#     find_next = each_Que_ans.find_next_sibling()
#     while True:
#         if "start-question" not in find_next.get('class', []) and "start-answer" not in find_next.get('class', []):
#             Question_list.append(each_Que_ans)
#             each_Que_ans = each_Que_ans.find_next_sibling()
#         elif "start-answer" in each_Que_ans.get('class', []):
#             Answer_list.append(each_Que_ans)
#             while True:
#                 each_Que_ans = each_Que_ans.find_next_sibling()
#                 if "start-question" not in each_Que_ans.get('class', []) and "start-answer" not in each_Que_ans.get('class', []):
#                     Answer_list.append(each_Que_ans)
#                 else:
#                     Questions.append(Question_list)
#                     Questions.append(Answer_list)
#                     Question_list = []
#                     Question_list.append()
#                     break
#         else:
#             Questions.append(Question_list)
#             Total_Que_list.append(Questions)
#             break
#     Total_Que_list.append(Questions)
#
#
#
# print(len(Questions))
# print(count)
#
