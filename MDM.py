
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import pandas as pd


song_one = "Buddy, you're a boy, make a big noise Playing in the street Gonna be a big man someday You got mud on your face You big disgrace Kicking your can all over the place, singing We will, we will rock you We will, we will rock you Buddy, you're a young man, hard man Shouting in the street Gonna take on the world someday You got blood on your face You big disgrace Waving your banner all over the place We will, we will rock you (Sing it out) We will, we will rock you Buddy, you're an old man, poor man Pleading with your eyes Gonna make you some peace someday You got mud on your face Big disgrace Somebody better put you back into your place We will, we will rock you, sing it We will, we will rock you, everybody We will, we will rock you, hmm We will, we will rock you, alright "
song_two = "I've paid my dues, time after time I've done my sentence, but committed no crime And bad mistakes I've made a few I've had my share of sand kicked in my face, but I've come through (And I need to go on and on, and on, and on) We are the champions, my friends And we'll keep on fighting till the end We are the champions We are the champions No time for losers 'Cause, we are the champions of the world I've taken my bows and my curtain calls You brought me fame and fortune and everything that goes with it I thank you all But it's been no bed of roses No pleasure cruise I consider it a challenge before the whole human race And I ain't gonna lose (And I need to go on and on, and on, and on) We are the champions, my friends And we'll keep on fighting till the end We are the champions We are the champions No time for losers 'Cause, we are the champions of the world We are the champions, my friends And we'll keep on fighting till the end, oh We are the champions We are the champions No time for losers 'Cause, we are the champions"
song_three = "Well, you're just seventeen All you wanna do is disappear You know what I mean There's a lot of space between our ears The way that you touch don't feel nothing Hey, hey, hey, hey It was the DNA Hey, hey, hey, hey That made me this way Do you know, do you know, do you know Just how I feel? Do you know, do you know, do you know Just how I feel? Sheer heart attack Sheer heart attack Real cardiac I feel so Inar-inar-inar-inar-inar-inar-inar-inarticulate Gotta feeling, gotta feeling Gotta feeling, like I'm paralyzed It ain't no, it ain't no It ain't no, it ain't no surprise Turn on the TV Let it drip right down in your eyes Hey, hey, hey, hey It was the DNA Hey, hey, hey, hey That made me this way Do you know, do you know, do you know Just how I feel? Do you know, do you know, do you know Just how I feel? Sheer heart attack Sheer heart attack Real cardiac I feel so inar-inar-inar-inar Inar-inar-inar-inarticulate Just how I feel Do you know, do you know, do you know Just how I feel? Do you know, do you know, do you know Just how I feel? Do you know, do you know, do you know Just how I feel? Sheer heart attack Sheer heart attack Real cardiac"
song_four = "She came without a farthing A babe without a name So much ado about nothing Is what she'd try to say So much ado, my lover So many games we played Through every fleeted summer Through every precious day All dead, all dead All the dreams we had And I wonder why I still live on All dead, all dead And alone I'm spared My sweeter half instead All dead and gone All dead All dead, all dead At the rainbow's end And still I hear her own sweet song All dead, all dead Take me back again You know my little friend's All dead and gone Her ways are always with me I wander all the while But please, you must forgive me I am old but still a child All dead, all dead But I should not grieve In time, it comes to everyone All dead, all dead But in hope I breathe Of course, I don't believe You're dead and gone All dead and gone"
song_five = "Sammy was low, just watching the show Over and over again Knew it was time, he'd made up his mind To leave his dead life behind His boss said to him Boy, you'd better begin To get those crazy notions Right out of your head Sammy, who do you think that you are? You should've been sweeping Up the Emerald Bar Spread your wings and fly away Fly away, far away Spread your little wings and fly away Fly away, far away Pull yourself together 'Cause you know you should do better That's because you're a free man He spends his evenings Alone in his hotel room Keeping his thoughts to himself He'd be leaving soon Wishing he was miles and miles away Nothing in this world Nothing would make him stay Since he was small, had no luck at all Nothing came easy to him Now it was time, he'd made up his mind This could be my last chance His boss said to him Now listen, boy! You're always dreaming You've got no real ambition You won't get very far Sammy boy, don't you know who you are? Why can't you be happy At the Emerald Bar? So honey, spread your wings and fly away Fly away, far away Spread your little wings and fly away Fly away, far away Pull yourself together 'Cause you know you should do better That's because you're a free man Come on, honey Fly with me"


# sample corpus of documents
corpus = [song_one,
          song_two,
          song_three,
          song_four,
          song_five]

# create an instance of the CountVectorizer class
vectorizer = CountVectorizer()

# fit the vectorizer to the corpus and transform the corpus into a term-document matrix
td_matrix = vectorizer.fit_transform(corpus)

# print the vocabulary (i.e., the terms)
terms = vectorizer.get_feature_names_out()
print(terms)

# create a numpy array from the term-document matrix
td_matrix_array = td_matrix.toarray()
print(td_matrix_array)

# create a pandas DataFrame from the term-document matrix
df = pd.DataFrame(td_matrix.toarray(), columns=terms)

# select the first 10 terms
df = df.iloc[:, :5]

# create a table visualization using matplotlib
fig, ax = plt.subplots()
ax.axis('off')
#ax.axis('tight')
ax.table(cellText=df.values, colLabels=df.columns, rowLabels=["We Will Rock You","We Are the Champions","Sheer Heart Attack","All Dead, All Dead","Spread Your Wings"], loc='center')
plt.show()

# create a pandas DataFrame from the term-document matrix
df = pd.DataFrame(td_matrix.toarray(), columns=terms)

# create the inverted index
inverted_index = df.transpose()

# select the first 10 terms
inverted_index = inverted_index.iloc[:10, :]

# create a table visualization using matplotlib
fig, ax = plt.subplots()
ax.axis('off')
ax.axis('tight')
ax.table(cellText=inverted_index.values, colLabels=inverted_index.columns, loc='center')
plt.show()

# print the inverted index
print(inverted_index)
