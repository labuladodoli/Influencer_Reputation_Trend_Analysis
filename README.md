# Influencer_Reputation_Trend_Analysis
It used to analyze the current reputation of a specific influencer on YouTube.

Version1:

1.Use the Selenium package to scrape all comments from the latest 30 videos of a specific influencer on YouTube. Then, filter the comments to retain only those containing keywords related to the influencer.
2.Input all comments into a sentiment analysis model (PaddlePaddle BiLSTM model) to determine whether they are positive or negative. Positive comments add 1 point, negative comments subtract 1 point, and neutral comments do not change the score. This helps track how the influencer's reputation trend changes as the number of comments increases.

Version1 Analysis Result:

![sentiment_scores_1](https://github.com/user-attachments/assets/3c13306c-a1c8-4eb8-b302-9514e50366f4)



Version2:

The Version has the following issues, and I have made the following changes:
1.Outdated version
-> Update the environment and provide a list of installed packages.
2.The final chart in Version 1 shows how the influencer's reputation score changes with the number of comments. However, since the number of comments varies for each video, it is difficult to use comment count as a true representation of time progression, making it hard to depict trends. Additionally, Version 1 retrieves comments from the most recent video to the oldest, which does not align with how humans typically observe trends.
-> Modify the final chart so that the X-axis represents the video release order.
3.In Version 1, aside from the issue of improper time representation, the reputation score for each video is aggregated. This means that trend analysis relies only on the slope of the line to determine how the influencer's reputation changes within a specific comment count range, which is neither fair nor intuitive.
-> Modify the analysis so that each video has its own calculated reputation score. Normalize the score by dividing it by the number of valid comments (comments related to the influencer), ensuring that the score falls within the range of -1 to 1. This makes the chart more meaningful.

Version2 Analysis Result:
<img src="[https://github.com/user-attachments/assets/31f96b66-a021-471e-ab6b-becfb7b0d8cd]" width="300" />



Source of the sentiment analysis model:
https://github.com/PaddlePaddle/PaddleNLP/tree/develop/slm/examples/sentiment_analysis/skep

