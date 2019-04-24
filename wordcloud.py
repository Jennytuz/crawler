from wordcloud import WordCloud


# Read the whole text.
text = open('wordcloud_fuzhou.txt').read()

# Generate a word cloud image
wc = WordCloud(background_color="white", repeat=True)
wc.generate(text)

wc.to_file('fuzhou.png')