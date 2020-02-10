import re, string, random, glob, operator, heapq, codecs, sys, optparse, os, logging, math
from functools import reduce
from collections import defaultdict
from math import log10

class Entry:
    
    def __init__(self, word, position, probability, pointer):
        self.word = word
        self.position = position
        self.probability = probability
        self.pointer = pointer

class Segment:

    def __init__(self, Pw):
        self.Pw = Pw
        self.heap = []
        self.chart = []
        self.first = ""
        self.length = 0

    def segment(self, text):
        "Return a list of words that is the best segmentation of text."
        if not text: return []

        self.length = len(text)

        self.chart = [0 for i in range(self.length)]

        for letter in text:
            self.first += letter
            matched = False
            for word in self.Pw.keys():
                if word == self.first:
                    matched = True
                    entry = Entry(word, 0, log10(self.Pw(word)), None)
                    self.heap.append(entry)
            if not matched and len(self.first) <= 1:
                entry = Entry(self.first, 0, 0, None)
                self.heap.append(entry)
                    

        endIndex = 0
        while self.heap:

            self.heap.sort(key=lambda x: x.position+len(x.word), reverse=True)            
            entry = self.heap.pop(0);
            endIndex = len(entry.word) + entry.position
            ind = len(entry.word) - 1
        

            if self.chart[endIndex-1]:
                if entry.probability > self.chart[endIndex-1].probability:
                    self.chart[endIndex-1] = entry
                else:
                    continue
            else:
                self.chart[endIndex-1] = entry

            self.first=""
            text = text[ind+1:]
            for letter in text:
                self.first += letter
                matched = False
                for newWord in self.Pw.keys():
                    if newWord == self.first:
                        matched = True
                        newEntry = Entry(self.first, endIndex, (entry.probability+log10(self.Pw(newWord))), entry)
                        if newEntry not in self.heap:
                            self.heap.append(newEntry)                
                if not matched and len(self.first) <= 1:
                    newEntry = Entry(self.first, endIndex, (entry.probability), entry)
                    if newEntry not in self.heap:
                        self.heap.append(newEntry)

        finalIndex = self.length - 1
        finalEntry = self.chart[finalIndex]

        segmentation = []
        while finalEntry != None:
            segmentation.append(finalEntry.word)
            finalEntry = finalEntry.pointer

        segmentation.reverse()
        return segmentation


#### Support functions (p. 224)

def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.values()))
        self.missingfn = missingfn or (lambda k, N: 1./N)
    def __call__(self, key): 
        if key in self: return self[key]/self.N  
        else: return self.missingfn(key, self.N)

def datafile(name, sep='\t'):
    "Read key,value pairs from file."
    with open(name) as fh:
        for line in fh:
            (key, value) = line.split(sep)
            yield (key, value)

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-c", "--unigramcounts", dest='counts1w', default=os.path.join('data', 'count_1w.txt'), help="unigram counts [default: data/count_1w.txt]")
    optparser.add_option("-b", "--bigramcounts", dest='counts2w', default=os.path.join('data', 'count_2w.txt'), help="bigram counts [default: data/count_2w.txt]")
    optparser.add_option("-i", "--inputfile", dest="input", default=os.path.join('data', 'input', 'dev.txt'), help="file to segment")
    optparser.add_option("-l", "--logfile", dest="logfile", default=None, help="log file for debugging")
    (opts, _) = optparser.parse_args()

    if opts.logfile is not None:
        logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.DEBUG)

    Pw = Pdist(data=datafile(opts.counts1w))
    segmenter = Segment(Pw)
    with open(opts.input) as f:
        for line in f:
            print(" ".join(segmenter.segment(line.strip())))
