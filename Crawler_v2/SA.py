from paddlenlp import Taskflow
from opencc import OpenCC
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv
import os

counter = 0
scores = []
cc = OpenCC('t2s')
senta = Taskflow("sentiment_analysis", model="skep_ernie_1.0_large_ch")

for order in range(10):
    score = 0
    num_of_comment = 0
    with open(os.path.join("excel", f"comment_{order+1}.csv"), "r", encoding='utf-8', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            num_of_comment += 1
            try:
                if senta(cc.convert(row[1]))[0]['label'] == 'positive':
                    score += 1
                elif senta(cc.convert(row[1]))[0]['label'] == 'negative':
                    score -= 1
            except ZeroDivisionError:
                print( "it occurs a ZeroDivisionError" )
            if num_of_comment%10 == 0 :
                print( num_of_comment,"items be done" )
            
    csvfile.close()
    score /= num_of_comment
    scores.append(score)
    print( "favorable_rating : ", score)

plt.plot(range(1, 11), scores, marker='o', linestyle='-', color='b')

plt.title("Sentiment Score of Videos")
plt.xlabel("Video Release Order")
plt.ylabel("Critic Score")

plt.xticks(range(1, 11))
plt.ylim(-1, 1)
plt.yticks([-1, 0, 1])
plt.grid(True)
plt.savefig("sentiment_scores.png", dpi=300, bbox_inches='tight')

