# Analysis of Word Frequencies in the Common Voice Sentences

I have way too much free time on my hands, so I decided to crunch some numbers
and see how diverse and varied the sentences in Common Voice are. 

Disclaimer: I'm not a statistician or anything (does Crash Course count?) so
take whatever I say with a grain of salt, because I probably got something wrong
somewhere.

## Word Frequencies from Wikipedia

First, let's get a bunch of sample text. Wikipedia is an easy source, and it's
got lots of words from a wide variety of topics. `00_get_wikipedia_words.py`
downloads random articles from Wikipedia and counts the word frequencies there.
Articles are cached in the `cache` directory, so subsequent runs should be
faster. The script is set to download 10 million words (approximately); to
change this, edit the `WORDCOUNT_GOAL` variable at the top of the script.

For the purposes of this analysis, let's only consider English words. I've
downloaded the ENABLE wordlist, which contains about 172000 words. Only words on
that list are included in the output. However, the total wordcount includes all
words, whether they are in the dictionary or not.

Also note that I excluded the following words: "bibliography," "external,"
"links," and "references," because they appear abnormally often in Wikipedia.

The script outputs to `01_frequencies_wikipedia.csv`. The columns in that file
are Frequency, Relative Frequency, Word. The frequency is the number of times
it occurs; relative frequency is frequency divided by the total wordcount (in
other words, the percent of the sample that is that word).

When I ran the script, I got the following statistics:

    WORDS: 10001808 (UNIQUE: 360794, IN DICTIONARY: 60631)
    PAGES: 22159

## Word Frequencies in Common Voice

Running a similar script, `04_get_common_voice_words.py`, gives us the same
statistics for Common Voice. I downloaded the data at commit eb3a077 of
<https://github.com/mozilla/voice-web/>. Here are the statistics:

    WORDS: 1734462 (UNIQUE: 30870, IN DICTIONARY: 20299)

The output for this script, in the same format as for Wikipedia, is in
`05_frequencies_common_voice.csv`.

## Analyzing the data

Now it's time to really get our hands dirty. `06_get_frequency_ratios.py` tells
us how over- or under-represented each word is in Common Voice. Specifically,
it gives a measure of how much more (or less) the word should appear in order to
be represented adequately.

The formula for this measure is `(freq - target_freq) / (target_freq - 1)`. The
denominator here is a correction factor that takes into account the growth of
the dataset when more words are added; if you want me to explain in detail how I
came up with the formula, ask in the comments.

Anyway, if we run this script, we get a new CSV file,
`07_common_voice_word_representation.csv`. This is the data we're looking for.
The columns are Representation (the formula above), Frequency (Wikipedia),
Frequency (Common Voice), Word.

In addition, the script outputs some other statistics:

    OVERREPRESENTED: 8327
    NOT REPRESENTED: 41981
    NOT IN WIKIPEDIA: 1649

So Common Voice contains 8327 words that are overrepresented--that is, they
occur more often there than in Wikipedia and have a negative representation
score. The Wikipedia sample contains a whopping 41981 words that aren't in
Common Voice at all, while Common Voice contains only 1649 words not in the
Wikipedia sample.

Okay, now let's look at the data itself. A simple
`head -n 100 07_common_voice_word_representation.csv` gives us the most
*underrepresented* words--that is, the ones that Common Voice really needs more
of. And, drum roll, at the top of the list is... ***THE?!***

Yep, "the" is highly underrepresented. In normal English, it accounts for about
6.5% of words, while in Common Voice, it's only about 3.7%. Surprisingly, "in"
actually occurs *more* than "the" in the dataset--that's highly unusual.

However, we get more diverse words as we scroll down--stuff like "university,"
"years," and "national." These words all occur in Common Voice, but not nearly
as often as in Wikipedia. There's also the words that don't occur in Common
Voice at all--those are the ones with 0.0000000000 in the Common Voice column
of the CSV file.

## Suggestions

Right now, sentences are accepted into the dataset through a GitHub issue and
manually reviewed by the maintainers, but submission through the site itself is
a planned feature. Variety and diversity are vital to creating a useful corpus
of free voice samples. Tools like the one I've built, along with others, could
be used to suggest words to contributors and make sure the dataset contains a
healthy sample of the English language, including words people might not
otherwise think to use.

