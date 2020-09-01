#!/usr/bin/env python
# coding: utf-8

# ## Profitable App Profiles for the App Store and Google Play Markets. ##
# 
# For this project, we'll pretend we're working as data analysts for a company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the ads, the better. Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.

# we have two datasets:
# - [Android apps](https://www.kaggle.com/lava18/google-play-store-apps)
# - [iOS apps](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps)

# We'll start by opening and exploring these two data sets. To make them easier for you to explore, we created a function named **explore_data()** that you can repeatedly use to print rows in a readable way.

# In[1]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# We'll start by opening and exploring these two data sets.

# In[3]:


# Opening android apps dataset from Google Play #

from csv import reader
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]


# In[4]:


# Opening iOS apps dataset from Apple Store #

from csv import reader
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[5]:


# Exploring Google play data #

print(android_header)
print('\n')
explore_data(android,0,5,rows_and_columns=True)


# We can see that Google play data above has 10841 rows and 13 columns.
# *Most interesting columns are: App, Rating, Reviews, Price, Genre*

# In[6]:


# Exploring Apple data #

print(ios_header)
print('\n')
explore_data(ios,0,5,rows_and_columns=True)


# We can see that Apple data has 7197 apps.
# *Most interesting columns are: track_name, currency, price, user_rating,prime_genre*

# ## We will now be doing data cleaning##

# The Google Play data set has a dedicated [discussion section](https://www.kaggle.com/lava18/google-play-store-apps/discussion), and we can see that one of the [discussions](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015) describes an error for a certain row.
# 
# **Wrong rating for entry 10472**
# 
# Easiest is to delete that entry as described in the code below

# In[8]:


print(android_header)
print('\n')
print(android[10472])


# We can see above that there is no category description, hence below is how we delete that row and we will check that row is deleted by printing same row again

# In[9]:


del android[10472]
print(android[10472])


# In the last step, we started the data cleaning process and deleted a row with incorrect data from the Google Play data set. If you explore the Google Play data set long enough or look at the discussions section, you'll notice some apps have duplicate entries. For instance, Instagram has four entries:

# In[12]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In total there are a lot of duplicates: total number listed below as the first one:

# In[36]:


unique_apps = []
duplicate_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

print(len(duplicate_apps))
print('\n')
print(len(unique_apps))


# We don't want to count certain apps more than once when we analyze data, so we need to remove the duplicate entries and keep only one entry per app. One thing we could do is remove the duplicate rows randomly, but we could probably find a better way.
# 
# If you examine the rows we printed for the Instagram app, the main difference happens on the fourth position of each row, which corresponds to the number of reviews. The different numbers show the data was collected at different times.
# 
# We can use this information to build a criterion for removing the duplicates. The higher the number of reviews, the more recent the data should be. Rather than removing duplicates randomly, we'll only keep the row with the highest number of reviews and remove the other entries for any given app.

# Create a dictionary where each key is a unique app name and the corresponding dictionary value is the highest number of reviews of that app.
# 
# Start by creating an empty dictionary named reviews_max.
# Loop through the Google Play data set (make sure you don't include the header row). For each iteration:
# Assign the app name to a variable named name.
# Convert the number of reviews to float. Assign it to a variable named n_reviews.
# If name already exists as a key in the reviews_max dictionary and reviews_max[name] < n_reviews, update the number of reviews for that entry in the reviews_max dictionary.
# If name is not in the reviews_max dictionary as a key, create a new entry in the dictionary where the key is the app name, and the value is the number of reviews. Make sure you don't use an else clause here, otherwise the number of reviews will be incorrectly updated whenever reviews_max[name] < n_reviews evaluates to False.
# Inspect the dictionary to make sure everything went as expected. Measure the length of the dictionary — remember that the expected length is 9,659 entries.

# In[37]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif n_reviews not in reviews_max:
        reviews_max[name] = n_reviews
        
print(len(reviews_max))


# If n_reviews is the same as the number of maximum reviews of the app name (the number can be found in the reviews_max dictionary) and name is not already in the list already_added (read the solution notebook to find out why we need this supplementary condition):
# Append the entire row to the android_clean list (which will eventually be a list of list and store our cleaned data set).
# Append the name of the app name to the already_added list — this helps us to keep track of apps that we already added.

# In[45]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
    


# In[46]:


explore_data(android_clean, 0, 5, True)


# In the previous step, we managed to remove the duplicate app entries in the Google Play data set. We don't need to do the same for the App Store data because there are no duplicates — you can check that for yourself using the id column (not the track_name column).
# 
# Remember we use English for the apps we develop at our company, and we'd like to analyze only the apps that are directed toward an English-speaking audience.
# 
# The numbers corresponding to the characters we commonly use in an English text are all in the range 0 to 127, according to the ASCII (American Standard Code for Information Interchange) system. Based on this number range, we can build a function that detects whether a character belongs to the set of common English characters or not. If the number is equal to or less than 127, then the character belongs to the set of common English characters.

# Write a function that takes in a string and returns False if there's any character in the string that doesn't belong to the set of common English characters, otherwise it returns True.
# 
# Inside the function, iterate over the input string. For each iteration check whether the number associated with the character is greater than 127. When a character is greater than 127, the function should immediately return False — the app name is probably non-English since it contains a character that doesn't belong to the set of common English characters.
# If the loop finishes running without the return statement being executed, then it means no character had a corresponding number over 127 — the app name is probably English, so the functions should return True.
# 
# Use your function to check whether these app names are detected as English or non-English:
# 
# 'Instagram'
# '爱奇艺PPS -《欢乐颂2》电视剧热播'
# 'Docs To Go™ Free Office Suite'
# 'Instachat 😜'

# In[69]:


def English(name):
    for character in name:
        if ord(character) > 127:
            return False
        return True

print(English('Instragram'))
print(English('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(English('Docs To Go™ Free Office Suite'))
print(English('Instachat 😜'))


# On the previous screen, we wrote a function that detects non-English app names, but we saw that the function couldn't correctly identify certain English app names like 'Docs To Go™ Free Office Suite' and 'Instachat 😜'. This is because emojis and characters like ™ fall outside the ASCII range and have corresponding numbers over 127.

# In[50]:


print(ord('™'))
print(ord('😜'))


# If we're going to use the function we've created, we'll lose useful data since many English apps will be incorrectly labeled as non-English. To minimize the impact of data loss, we'll only remove an app if its name has more than three characters with corresponding numbers falling outside the ASCII range. This means all English apps with up to three emoji or other special characters will still be labeled as English. Our filter function is still not perfect, but it should be fairly effective.
# 
# Let's edit the function we created in the previous screen, and then use it to filter out the non-English apps.

# Change the function you created in the previous screen. If the input string has more than three characters that fall outside the ASCII range (0 - 127), then the function should return False (identify the string as non-English), otherwise it should return True.

# In[72]:


def English(name):
    non_ASCII = 0
    
    for character in name:
        if ord(character) > 127:
            non_ASCII += 1
            
    if non_ASCII > 3:
            return False
    else:
            return True
            
        
    
print(English('Docs To Go™ Free Office Suite'))
print(English('Instachat 😜'))


# Use the new function to filter out non-English apps from both data sets. Loop through each data set. If an app name is identified as English, append the whole row to a separate list.
# 
# Explore the data sets and see how many rows you have remaining for each data set.

# In[73]:


android_English = []

for app in android_clean:
    name = app[0]
    if English(name):
        android_English.append(app)
   
explore_data(android_English,0,3,True)       
        


# In[74]:


ios_English = []

for app in ios:
    name = app[1]
    if English(name):
        ios_English.append(app)
        
explore_data(ios_English,0,3,True)        


# So far in the data cleaning process, we:
# 
# Removed inaccurate data
# Removed duplicate app entries
# Removed non-English apps
# As we mentioned in the introduction, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our data sets contain both free and non-free apps; we'll need to isolate only the free apps for our analysis.
# 
# Isolating the free apps will be our last step in the data cleaning process. 
# 
# Loop through each data set to isolate the free apps in separate lists. Make sure you identify the columns describing the app price correctly.
# 
# After you isolate the free apps, check the length of each data set to see how many apps you have remaining.

# In[81]:


android_final = []
ios_final = []

for app in android_English:
    cost = app[7]
    if cost == '0':
        android_final.append(app)
        
for app in ios_English:
    cost = app[4]
    if cost == '0.0':
        ios_final.append(app)
        
print(explore_data(android_final,0,0,True))
print('\n')
print(explore_data(ios_final,0,0,True))


# So far, we spent a good amount of time on cleaning data, and:
# 
# Removed inaccurate data
# Removed duplicate app entries
# Removed non-English apps
# Isolated the free apps
# 
# Let's begin the analysis by getting a sense of what are the most common genres for each market. For this, we'll need to build frequency tables for a few columns in our data sets.
# 
# Our conclusion was that we'll need to build a frequency table for the prime_genre column of the App Store data set, and for the Genres and Category columns of the Google Play data set.
# 
# We'll build two functions we can use to analyze the frequency tables:
# 
# One function to generate frequency tables that show percentages
# Another function we can use to display the percentages in a descending order

# The display_table() function you see below:
# 
# Takes in two parameters: dataset and index. dataset is expected to be a list of lists, and index is expected to be an integer.
# Generates a frequency table using the freq_table() function (which you're going to write as an exercise).
# Transforms the frequency table into a list of tuples, then sorts the list in a descending order.
# Prints the entries of the frequency table in descending order.

# In[82]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# Create a function named freq_table() that takes in two inputs: dataset (which is expected to be a list of lists) and index (which is expected to be an integer).
# 
# The function should return the frequency table (as a dictionary) for any column we want. The frequencies should also be expressed as percentages.
# We already learned how to build frequency tables in the mission on dictionaries.
# Copy the display_table() function we wrote above. Use it to display the frequency table of the columns prime_genre, Genres, and Category. We'll analyze the resulting tables on the next screen.

# In[83]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])     


# In[84]:


display_table(ios_final,-5)


# In[85]:


display_table(android_final, 9)


# In[86]:


display_table(android_final,1)


# The frequency tables we analyzed on the previous screen showed us that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and fun apps. Now, we'd like to get an idea about the kind of apps with the most users.
# 
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Let's start with calculating the average number of user ratings per app genre on the App Store. To do that, we'll need to:
# 
# Isolate the apps of each genre.
# Sum up the user ratings for the apps of that genre.
# Divide the sum by the number of apps belonging to that genre (not by the total number of apps).
# To calculate the average number of user ratings for each genre, we'll use a for loop inside of another for loop. This is an example of a for loop used inside another for loop:
# 
# Start by generating a frequency table for the prime_genre column to get the unique app genres (below, we'll need to loop over the unique genres). You can use the freq_table() function you wrote in a previous screen.
# 
# Loop over the unique genres of the App Store data set. For each iteration (below, we'll assume that the iteration variable is named genre):
# 
# Initiate a variable named total with a value of 0. This variable will store the sum of user ratings (the number of ratings, not the actual ratings) specific to each genre.
# Initiate a variable named len_genre with a value of 0. This variable will store the number of apps specific to each genre.
# Loop over the App Store data set, and for each iteration:
# Save the app genre to a variable named genre_app.
# If genre_app is the same as genre (the iteration variable of the main loop), then:
# Save the number of user ratings of the app as a float.
# Add up the number of user ratings to the total variable.
# Increment the len_genre variable by 1.
# Compute the average number of user ratings by dividing total by len_genre. This should be done outside the nested loop.
# Print the app genre and the average number of user ratings. This should also be done outside the nested loop.
# Analyze the results and try to come up with at least one app profile recommendation for the App Store. Note that there's no fixed answer here, and it's perfectly fine if the app profile you recommended is different than the one recommended in the solution notebook.

# In[88]:


freq_table(ios_final,-5)


# In[93]:


prime_genre_freq = {'Social Networking': 3.2898820608317814,
 'Photo & Video': 4.9658597144630665,
 'Games': 58.16263190564867,
 'Music': 2.0484171322160147,
 'Reference': 0.5586592178770949,
 'Health & Fitness': 2.0173805090006205,
 'Weather': 0.8690254500310366,
 'Utilities': 2.5139664804469275,
 'Travel': 1.2414649286157666,
 'Shopping': 2.60707635009311,
 'News': 1.3345747982619491,
 'Navigation': 0.186219739292365,
 'Lifestyle': 1.5828677839851024,
 'Entertainment': 7.883302296710118,
 'Food & Drink': 0.8069522036002483,
 'Sports': 2.1415270018621975,
 'Book': 0.4345127250155183,
 'Finance': 1.1173184357541899,
 'Education': 3.662321539416512,
 'Productivity': 1.7380509000620732,
 'Business': 0.5276225946617008,
 'Catalogs': 0.12414649286157665,
 'Medical': 0.186219739292365}

for genre in prime_genre_freq:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, avg_n_ratings)



# In the previous screen, we came up with an app profile recommendation for the App Store based on the number of user ratings. We have data about the number of installs for the Google Play market, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# In[94]:


display_table(android_final, 5)


# For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to find out which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on. To perform computations, however, we'll need to convert each install number from string to float. This means we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error.

# In[98]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)
            
    
    

