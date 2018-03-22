wikipedia = {}
with open("01_frequencies_wikipedia.csv", "r") as f:
    for line in f:
        (freq_abs, freq, word) = line.strip().split(",")
        wikipedia[word] = float(freq)

commonvoice = {}
with open("05_frequencies_common_voice.csv", "r") as f:
    for line in f:
        (freq_abs, freq, word) = line.strip().split(",")
        commonvoice[word] = float(freq)

# the formula below is a measure of how many times the word must be added to the dataset for the frequencies to match
ratios = [(word, (commonvoice.get(word, 0) - wikipedia[word]) / (wikipedia[word] - 1)) for word,freq in wikipedia.items()]
ratios.sort(key=lambda k: k[1], reverse=True)

with open("07_common_voice_word_representation.csv", "w") as f:
    for word in ratios:
        f.write("{:.10f},{:.10f},{:.10f},{}\n".format(word[1], wikipedia[word[0]], commonvoice.get(word[0], 0), word[0]))

overrepresented = [word for word in ratios if word[1] < 0]
notrepresented = [word for word in ratios if word[0] not in commonvoice ]
extra = [word for word in commonvoice if word not in wikipedia]
print("OVERREPRESENTED: {}".format( len(overrepresented)) )
print("NOT REPRESENTED: {}".format( len(notrepresented) ))
print("NOT IN WIKIPEDIA: {}".format( len(extra) ))

