from bs4 import BeautifulSoup
import json
import re

file = open("Bussiness studies-1-18_compressed.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
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
.start-heading {
    color: blue;
    font-weight: bold;
}
.start-explanation {
    color: yellow;
    font-weight: bold;
}
.start-obj-heading {
    color: blue;
    font-weight: bold;
}
.start-AR-heading {
    color: blue;
    font-weight: bold;
}
.start-topic{
    color: orange;
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
            insert_stringOne = f"{div_split[0]}</div><br><div>Q. {div_split[1]}"
            new_soup = BeautifulSoup(insert_stringOne, 'html.parser')
            child.replace_with(new_soup)
    elif "Q." in child.text:
        if (not child.text.startswith("Q.") or not child.text.startswith("Q. ")) and child.name == "div":
            div_split = str(child).split("Q.")
            insert_stringOne = f"{div_split[0]}</div><br><div>Q. {div_split[1]}"
            new_soup = BeautifulSoup(insert_stringOne, 'html.parser')
            child.replace_with(new_soup)
        elif (not child.text.startswith("Q.") or not child.text.startswith("Q. ")) and child.name != "div":
            stringOne = child.text
            insert_string = f"<div>{stringOne}</div>"
            new_soup = BeautifulSoup(insert_string, 'html.parser')
            child.replace_with(new_soup)
    if "Reason (R):" in child.text:
        if not child.text.startswith("Reason"):
            div_split = str(child).split("Reason (R):")
            insert_stringOne = f"{div_split[0]}</div><br><div>Reason (R): {div_split[1]}"
            new_soup = BeautifulSoup(insert_stringOne, 'html.parser')
            child.replace_with(new_soup)

for each in next_all[0].children:
    if each.text.startswith('Q.') or each.text.startswith('Q. '):
        each['class'] = each.get('class', []) + ['start-question']
    elif each.text.startswith('Explanation:'):
        each['class'] = each.get('class', []) + ['start-explanation']
# Pre-Process For Answer
for ans_child in next_all[0].children:
    if "Ans." in ans_child.text:
        if not ans_child.text.startswith("Ans."):
            div_split = str(ans_child).split("Ans.")
            insert_ans_stringOne = f"{div_split[0]}</div><br><div>Ans. {div_split[1]}"
            ans_new_soup = BeautifulSoup(insert_ans_stringOne, 'html.parser')
            ans_child.replace_with(ans_new_soup)

for ans_each in next_all[0].children:
    if ans_each.text.startswith('Ans.') or ans_each.text.startswith('Ans. '):
        ans_each['class'] = ans_each.get('class', []) + ['start-answer']

for head_tag in next_all[0].children:
    if 'Short Answer Type' in head_tag.text or 'Long Answer Type' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-heading']

    elif 'Multiple Choice Questions' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-obj-heading']

    elif 'Assertion and Reason' in head_tag.text or 'B Assertion & Reason' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-AR-heading']
    elif "Topic-" in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-topic']

next_all_Qrep = soup.find_all('div', class_=["start-question"])
for div_tag in next_all_Qrep:
    div_tag.string = re.sub(r'Q.[\ ]*[0-9]+.', '', div_tag.text)

next_all_Arep = soup.find_all('div', class_=["start-answer"])
for div_tag in next_all_Arep:
    div_tag.string = re.sub(r'Ans\.?', '', div_tag.text)

next_all_Exrep = soup.find_all('div', class_=["start-explanation"])
for div_tag in next_all_Exrep:
    div_tag.string = re.sub(r'Explanation:', '', div_tag.text)

text_to_delete = soup.find_all(string='Choose the correct option from options given below:')
for each in text_to_delete:
    each.extract()
def Subjective_Question(Question_list, Answer_list, Meta_Dict):
    Sub_Dict = {}
    Sub_Dict["meta"] = Meta_Dict
    Sub_Dict["question"] = Question_list
    Sub_Dict["answer"] = Answer_list
    Sub_Dict["explaination"] = ""
    Total_SubQue_list.append(Sub_Dict)
def Objective_Question(Question_list, Answer_list, Obj_Meta_Dict):
    Question_lists = []
    Option_lists = []
    MCQ_Dict = {}
    if "(A)" in Question_list[0].text and "(B)" in Question_list[0].text and "(C)" in Question_list[
        0].text and "(D)" in Question_list[0].text:
        pattern = r'\((A|B|C|D)\)'
        string = str(Question_list[0])
        result = [x for x in re.split(pattern, string) if x not in ['A', 'B', 'C', 'D']]
        remove_List = []
        Question = []
        for eachStr in result:
            remove_List.append(
                str(eachStr).replace("\n", "").replace("<li>", "").replace("<div>", "").replace("</div>", "").replace(
                    "</li>", ""))
        for each in remove_List:
            Question.append("<div>" + each + "</div>")
        Question_lists.append(Question[0])
        Option_lists.append(Question[1])
        Option_lists.append(Question[2])
        Option_lists.append(Question[3])
        Option_lists.append(Question[4])
    else:
        for Q_each in Question_list:
            if "(A)" in Q_each.text and "(B)" in Q_each.text and "(C)" in Q_each.text and "(D)" in Q_each.text:
                pattern = r'\((A|B|C|D)\)'
                string = str(Q_each)
                result = [x for x in re.split(pattern, string) if x not in ['A', 'B', 'C', 'D']]
                remove_List = []
                Question = []
                for eachStr in result:
                    remove_List.append(
                        eachStr.replace("\n", "").replace("<li>", "").replace("<div>", "").replace("</div>",
                                                                                                   "").replace("</li>",
                                                                                                               ""))
                for each in remove_List:
                    Question.append("<div>" + each + "</div>")
                Question_lists.append(Question[0])
                Option_lists.append(Question[1])
                Option_lists.append(Question[2])
                Option_lists.append(Question[3])
                Option_lists.append(Question[4])
            else:
                Question_lists.append(Q_each)
        if len(Question_list) >= 5:
            if Question_list[1].text.startswith('Statement'):
                Question_lists = [Question_list[0], Question_list[1]]
                Option_lists = [Question_list[3], Question_list[4], Question_list[5], Question_list[6]]
            else:
                Question_lists = [Question_list[0]]
                Option_lists = [Question_list[1], Question_list[2], Question_list[3], Question_list[4]]
    correct_Answer = ["Not Given"]
    for i in Answer_list[:1]:
        if "(A)" in i.text:
            correct_Answer = [1]
        elif "(B)" in i.text:
            correct_Answer = [2]
        elif "(C)" in i.text:
            correct_Answer = [3]
        elif "(D)" in i.text:
            correct_Answer = [4]
    MCQ_Dict["meta"] = Obj_Meta_Dict
    MCQ_Dict["question"] = Question_lists
    MCQ_Dict["options"] = Option_lists
    MCQ_Dict["correct_answer"] = correct_Answer
    MCQ_Dict["explaination"] = Answer_list[1:]
    Total_ObjQue_list.append(MCQ_Dict)
def Assertion_Reason(Question_list, Answer_list, AR_Meta_Dict):
    AQ_Dict = {}
    Assertion = []
    Reason = []
    if "Assertion (A)" in Question_list[0].text and len(Question_list) >= 2:
        Assertion.append(Question_list[0])
        if "Reason" in Question_list[1].text:
            Reason.append(Question_list[1])
        elif "Reason" in Question_list[2].text:
            Reason.append(Question_list[2])
    elif "Assertion (A)" in Question_list[0].text:
        Assertion.append(Question_list[0])
        Reason.append([])
    correct_Answer = ["Not Given"]
    for i in Answer_list[:1]:
        if "(A)" in i.text:
            correct_Answer = [1]
        elif "(B)" in i.text:
            correct_Answer = [2]
        elif "(C)" in i.text:
            correct_Answer = [3]
        elif "(D)" in i.text:
            correct_Answer = [4]
    AQ_Dict["meta"] = AR_Meta_Dict
    AQ_Dict["assertion_text"] = Assertion
    AQ_Dict["reason_text"] = Reason
    AQ_Dict["correct_option"] = correct_Answer
    AQ_Dict["explaination"] = Answer_list[1:]
    Total_ARQue_list.append(AQ_Dict)
def extract_this_section(next_all_tags,Meta_Dict,key_name):
    for each_Que_ans in next_all_tags:
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
            elif "start-obj-heading" in find_next.get('class', []):
                break
            elif "start-AR-heading" in find_next.get('class', []):
                break
            elif "start-heading" in find_next.get('class', []):
                break
            elif find_next.name == "h2" and "Topic-" not in find_next.text:
                break
            if is_answer_mode:
                find_next.text.replace("Ans.", "")
                Answer_list.append(find_next)
            else:
                Question_list.append(find_next)
            find_next = find_next.find_next_sibling()
        if key_name == "Multiple Choice":
            Objective_Question(Question_list, Answer_list, Meta_Dict)
        elif key_name == "Assertion and Reason":
            Assertion_Reason(Question_list,Answer_list,Meta_Dict)
        else:
            Subjective_Question(Question_list, Answer_list, Meta_Dict)

specified_elements = soup.find_all(class_='start-topic')
sub_soups = []
for i in range(len(specified_elements)):
    start_element = specified_elements[i]
    if i + 1 < len(specified_elements):
        end_element = specified_elements[i + 1]
    else:
        end_element = None
    extracted_html = ""
    current_element = start_element.find_next_sibling()
    while current_element != end_element:
        extracted_html += str(current_element)
        current_element = current_element.find_next_sibling()
    sub_soup = BeautifulSoup(extracted_html, 'html.parser')
    sub_soups.append(sub_soup)
# Print the sub-soups
all_quetions=[]
for each_soup in range(len(sub_soups)):
    Total_SubQue_list = []
    Total_ARQue_list = []
    Total_ObjQue_list = []
    Main_Dict = {}
    class_blocks = sub_soups[each_soup].find_all(class_='start-heading')
    for each_block in class_blocks:
        Question_class = []
        next_sibling = each_block.find_next_sibling()
        while next_sibling and 'start-heading' not in next_sibling.get('class', []) and 'start-obj-heading' not in next_sibling.get('class', []) and 'start-AR-heading' not in next_sibling.get('class', []):
            if "start-question" in next_sibling.get('class', []):
                Question_class.append(next_sibling)
            next_sibling = next_sibling.find_next_sibling()
        key_name = each_block.text.replace("\n", "")[3:16]
        Meta_Dict = {}
        Meta_Dict["type"] = key_name
        Meta_Dict["location"] = "Exercise" + " " + each_block.text.replace("\n", "")[:2]
        extract_this_section(Question_class, Meta_Dict, key_name)

    Main_Dict["subjective_questions"] = Total_SubQue_list

    Obj_class_blocks = sub_soups[each_soup].find_all(class_='start-obj-heading')
    for each_block in Obj_class_blocks:
        Obj_Question_class = []
        next_sibling = each_block.find_next_sibling()
        while next_sibling and 'start-AR-heading' not in next_sibling.get('class', []):
            if "start-question" in next_sibling.get('class', []):
                Obj_Question_class.append(next_sibling)
            next_sibling = next_sibling.find_next_sibling()
        key_name = "Multiple Choice"
        Obj_Meta_Dict = {}
        Obj_Meta_Dict["type"] = key_name
        Obj_Meta_Dict["location"] = "Exercise" + " " + each_block.text.replace("\n", "")[:2]
        extract_this_section(Obj_Question_class, Obj_Meta_Dict, key_name)

    Main_Dict["objective_questions"] = Total_ObjQue_list

    Obj_class_blocks = sub_soups[each_soup].find_all(class_='start-AR-heading')
    for each_block in Obj_class_blocks:
        AR_Question_class = []
        next_sibling = each_block.find_next_sibling()
        while next_sibling and 'start-AR-heading' not in next_sibling.get('class', []):
            if "start-question" in next_sibling.get('class', []):
                AR_Question_class.append(next_sibling)
            next_sibling = next_sibling.find_next_sibling()

        key_name = "Assertion and Reason"
        AR_Meta_Dict = {}
        AR_Meta_Dict["type"] = key_name
        AR_Meta_Dict["location"] = "Exercise" + " " + each_block.text.replace("\n", "")[:2]
        extract_this_section(AR_Question_class, AR_Meta_Dict, key_name)
    Main_Dict["assertion_questions"] = Total_ARQue_list
    def convert_to_serializable(obj):
        if isinstance(obj, int):
            return obj
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}
        else:
            return str(obj)
    Topic_wise_Dict = {}
    Main_Dict = convert_to_serializable(Main_Dict)
    Topic_wise_Dict["topic"] = "Topic" + "-" +str((each_soup+1))
    Topic_wise_Dict["questions"] = Main_Dict
    all_quetions.append(Topic_wise_Dict)
out_File = open("topic_wise.json", "w")
json.dump(all_quetions, out_File, indent=6)
