# Habit Tracker Summary

My project models data that one might find in a habit tracking app, including information like a user's name, all of the habits they are currently tracking, and each daily log for that habit since creation.

<img src="HabitTracker Database Diagram.png">

## Query the model did well with
**Question**: How many times was each habit completed?

**Query**:
```sql
SELECT h.habit_id, h.habit_name, COUNT(hl.log_id) AS completion_count
FROM habits h
LEFT JOIN habit_logs hl ON h.habit_id = hl.habit_id AND hl.is_done = 1
GROUP BY h.habit_id, h.habit_name;
```

**Response**: Here are the completion counts for each habit: "Brush Teeth" was completed 30 times, "Call Mom" 17 times, "Clean Room" 18 times, "DISHES" 6 times, "Drink Water" 28 times, "Eat a Veggie" 12 times, "Eat Breakfast" 3 times, "Make Bed" 29 times, "Practice" 4 times, "Scriptures" 7 times, "Study" 26 times, "Walk Dog" 10 times, "Water x3" 12 times, and "Workout" 5 times.

This one, admittedly, was not very hard for the AI to figure out, as it was a simple calculation.

## Query the model did less well with
**Question**: Which habits are the hardest to maintain?

**Query**:
```sql
SELECT h.habit_name, COUNT(hl.log_id) AS log_count
FROM habits h
LEFT JOIN habit_logs hl ON h.habit_id = hl.habit_id
GROUP BY h.habit_id
ORDER BY log_count ASC
LIMIT 10;
```

**Response**: The hardest habits to maintain, based on the number of times they were logged, are "Practice," "DISHES," and "Eat Breakfast," with very few logs compared to others like "Brush Teeth" and "Clean Room."

The model was tripped up on this one because it simply counted which habits were logged the least number of times. It did not consider whether they were logged as complete or not, nor did it consider how many times it was logged as incomplete proportional to how many times it was logged at all. Practice and DISHES were both created by a user who only joined the app a week ago, but managed to complete the tasks every day since then. Thus, those habits should actually be considered some of the *easiest* to maintain. The model likely would have done better if I phrased the question to more explicitly mention needing proportions. 

I also asked the question **"What habits are people struggling with lately?"** which is very similar to the other question asked. However, this phrasing led to a different query.

**Query**:
```sql
SELECT h.habit_name, COUNT(hl.log_id) AS struggle_count
FROM habits h
JOIN habit_logs hl ON h.habit_id = hl.habit_id
WHERE hl.is_done = 0 AND hl.log_date >= DATE('now', '-30 days')
GROUP BY h.habit_id
ORDER BY struggle_count DESC;
```

**Response**: People are currently struggling the most with working out, reading scriptures, and walking their dogs, with many also having difficulty keeping their rooms clean and staying hydrated.

This response is more accurate to what I was looking for in the original question, where I wanted to see which tasks are being marked as incomplete rather than just which habits are being logged less than others. Because I asked the question with the word "lately" I am more okay with the model still not doing the proportional calculations that I was looking for earlier. Although I would not really consider the last 30 days as "lately", I appreciate the model making an effort to filter out older logs given the vague prompt.
