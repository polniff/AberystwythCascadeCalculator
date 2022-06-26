import numpy as np
import pandas as pd

def readData():
    data = pd.read_csv('marks.txt')
    out_modules = []
    for i in data.index: 
        module = data.loc[i]['module']
        score = data.loc[i]['mark']
        numeric_values ="".join(filter(str.isdigit, module))
        ar = []
        ar.extend(numeric_values)
        credits = ar[-2:]
        credit_value = int(credits[0] + credits[1])
        year = int(ar[0]   )  
        out_modules.append([year, credit_value, score])
    return out_modules

def sortMarks(): 
    # sorts marks by credit, lowest credit to highest
    marks = readData()
    total_credits = 0
    out_marks = []
    for i in range(len(marks)):
        year = marks[i][0]
        credit = marks[i][1]/10
        score = marks[i][2]
        total_credits += credit
        for j in range(1, int(credit)):
            out_marks.append((year, score))
    print(f"Total credits taken: {total_credits*10:.0f}", )
    return out_marks

def cascade(marks):
    # calculates the cascade grade: 
    '''
    Band 3:  Best 80 Level 3 credits, given a weighting of 3.
    Band 2:  Next Best 80 Level 3 and Level 2 credits, with a weighting of 2.
    Band 1:  Remainder of Level 3 and 2 and Level 1 credits, with a weighting of 1.
    '''
    level3 = []
    level2 = []
    for mark in marks:
        year = mark[0]
        score = mark[1]
        if(year == 3):
            level3.append(score)
        else:
            level2.append(score)
    
    level3.sort(reverse=True)
    level2.sort(reverse=True)

    grade = 0

    # band 3 -> top 8 marks in year 3 get weight of 3
    top80Level3 = np.array(level3[:8])*3
    weight3 = 0
    del level3[:8]
    for band3 in top80Level3:
        weight3 += 1
        grade += band3

    # band 2 
    allScores = np.concatenate((level2, level3))
    allScores = allScores*2
    allScores = np.sort(allScores)[::-1]
    topRemaining80 = np.array(allScores[:8])
    allScores = allScores[8:]
    weight2 = 0
    for band2 in topRemaining80:
        weight2 += 1
        grade += band2

    # band 1
    weight1 = 0
    for band1 in allScores:
        weight1 += 1
        grade += band1

    grade = (grade/((3*weight3)+(2*weight2)+(1*weight1)))
    return grade
    
def main():
    sorted_scores= sortMarks()
    grade = cascade(sorted_scores)
    if(grade>69.5):
        print(f'\nFirst Class Degree: {grade:.2f}%')
    elif(grade<=69.5) and (grade>59.5):
        print(f'\nSecond Class Degre(I): {grade:.2f}%')
    elif(grade<=59.5) and (grade>49.5):
        print(f'\nSecond Class Degree(II): {grade:.2f}%')
    elif(grade<=49.5) and (grade<39.5):
        print(f'\nThird Class Degree: {grade:.2f}%')
    elif(grade<=39.5) and (grade>=35):
        print(f'\nPassed degree: {grade:.2f}%')
    else:
        print('FAIL')

if __name__ == '__main__':
    main()