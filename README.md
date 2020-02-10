# ensegment
Chinese Word Segmentation

The iterative segmenter is able to achieve an F-score of 0.87 on the dev set. It is able to do so by taking advantage of some basic data structures and an approach based on the provided pseudo code.

A basic python list is used for the chart as well as the heap. The heap is sorted at the start of every iteration based on the starting position of the entry plus the length of the word in entry. 

The heap is initialized by looking up every possible word that starts at position 0 of input. If a word is not found in the data and has a length of 1, it is added to the heap with a probability of 0. The same approach is used to add the rest of the input to the heap (starting at endIndex+1 and adding its log probability to the probability of the current entry, which itself is the sum of log probabilities of all its predecessors. This approach makes things run much faster by taking advantage of dynamic programming and not having to calculate probabilities which we have already calculated).

The chart is a list of the same length as the input. The elements of chart are Entry objects each containing information about the entry, namely the probability, the word itself, the starting position, as well as a back pointer connecting it to its previous entry.

In the end, we end up with a full chart. By following the back pointer of its last element until the pointer becomes None, we are able to build the full segmented text in reverse order. By simply running the reverse function on this list, we are able to retrieve the original text with the best segmentation, using unigram counts.

One of the tricks was properly sorting the heap at every iteration. The sum of the starting position with the length of the word, did the job. Another trick was in taking into account all the single characters which were not found in data. Otherwise, we would leave behind holes in chart. I simply, added the words with probability 0 to the heap as if they are "unknown" words. Obsiously, better results could have been achieved by using the bigram counts, however, due to lack of time, unigram counts were used which were still able to deliver reasonable results.
