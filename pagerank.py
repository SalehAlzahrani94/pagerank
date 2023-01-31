import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    destination={}
    dict_len=len( corpus.keys() )# look if our page gas links 
    pages_len=len( corpus[page] )
    # less than one that maen there is no out pages 
    if len( corpus[page ] )<1:
        for i in corpus.keys():# chose randomly 
            destination[i ]=1/dict_len
    else:# if the if contion not true do this part ( there is outgonin pages)
        factors=( 1 - damping_factor )/dict_len# this part for calculat 
        factors_even=damping_factor/pages_len# use to look for even
        for i in corpus.keys():# i in each key in corpus keys 
            if i not in corpus[ page]:# if jey is not init 
                destination[i ]=factors
            else: # if key init 
                destination[i ]=factors_even + factors

    return destination


    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, r):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # start by number of samples which is 0
    dicttionary=corpus.copy()
    for i in dicttionary:
        dicttionary[ i]=0
    sampleing=None
# go over r times
    for nonuse in range( r):
        if sampleing : # if its ture then the are samples 
            dist=transition_model( corpus, sampleing , damping_factor ) # using transition model method 

            dist_lst= list( dist.keys() )
            dist_weights=[dist[ i] for itme in dist ] # loops over all dist
            sampleing = random.choices( dist_lst , dist_weights , k=1)[ 0] #starting with a page at random
        else:# if its false then do this part ( no samples)
            # choosing randomly
            sampleing = random.choice( list( corpus.keys()) )

        # counting samples by adding one  
        dicttionary[ sampleing ] +=1

    # make samples count by % 
    for num in dicttionary :# loop over all dicttionary
        dicttionary[ num ] /= r# div by r

    return dicttionary# return what we need py percent
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    number_of_pages  = len(corpus)# take the lentgh of corpus 
    old_dictionary= {}
    new_dictionary= {}

    #we make each page rank 1/i, note: i is the total of pages in our corpus
    for num in corpus :
        old_dictionary[ num ]= 1/number_of_pages 
    #  while true will calculat the new rank
    while True:
        for num in corpus :# go over all corpus 
            x=0# initial by 0
            for link_of_page in corpus:# go over all corpus 
                if num in corpus [ link_of_page ] :#look for links to our page
                    x += (old_dictionary[ link_of_page ]/len( corpus[ link_of_page ] ))
                if len( corpus[ link_of_page ] )==0 : # in this part look if no links, then says its having one link for other pages
                    x +=( old_dictionary [ link_of_page ])/len(corpus)
            x *=damping_factor
            x +=( 1 - damping_factor )/number_of_pages 
            new_dictionary[num] = x # save the calculated nember (dictionary)

        diff=max( [abs(new_dictionary [x ]- old_dictionary[ x ])for x in old_dictionary] )# find highest (absolute value)
        if diff < 0.001:# if the value difference less than 0.001 stop
            break# 
        else:# if the value differece greater than 0.001 do this part 
            old_dictionary=new_dictionary.copy() 

    return old_dictionary

    raise NotImplementedError


if __name__ == "__main__":
    main()
