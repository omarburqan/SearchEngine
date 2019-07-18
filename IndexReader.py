import re
import datetime
import random

def getByReviewID(dir, reviewId):
    """
    a private method in order to get the needed line of this reviewId
    :param dir: directory to open the file
    :param reviewId: reviewId that need to be entered
    :return: the line of this reviewId in getByReviewID
    """
    with open(dir + "\getByReviewId" + ".txt", "r") as f1:
        buffer_text = f1.readlines(int(1073741824))
        review_No = 0
        list = []
        while len(buffer_text) != 0:
            review_No += len(buffer_text)
            if ((reviewId*2)-1) < review_No:
                list.append(buffer_text[(reviewId*2)-2-(review_No-len(buffer_text))])
                list.append(buffer_text[(reviewId*2)-1-(review_No-len(buffer_text))])
                buffer_text.clear()
                return list
            elif (reviewId*2-1) == review_No:
                list.append(buffer_text[(reviewId*2)-2-(review_No-len(buffer_text))])
                list.append(f1.readline())
                buffer_text.clear()
                return list
            buffer_text = f1.readlines(int(1073741824))


# Returns index of x in arr if present, else -1
def binarySearch(arr, l, r, x):
    # Check base case
    if r >= l:
        mid = l + (r - l) / 2
        mid = int(mid)
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
            # Else the element can only be present in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        # Element is not present in the array
        return -1


def binarySearch_withkey(arr, l, r, x):
    # Check base case
    if r >= l:
        mid = l + (r - l) / 2
        mid = int(mid)
        # If element is present at the middle itself
        if arr[mid].startswith(str(x)):
            return mid
            # If element is smaller than mid, then it can only
        # be present in left subarray

        elif int(arr[mid][:arr[mid].index("&")]) > int(x):
            return binarySearch_withkey(arr, l, mid - 1, x)
            # Else the element can only be present in right subarray
        else:
            return binarySearch_withkey(arr, mid + 1, r, x)
    else:
        # Element is not present in the array
        return -1


def getLineBytoken(dir, token):
    """
    retuning a line in getByTokenB.bin
    :param dir: directory to be opened
    :param token: the word that  will be needed to get it's attribute
    :return: the attributes for this token by returning the line in getByTokenB.bin by using the index of this word
    getByTokenB.bin
    """
    if token == "":
        return -1
    token_indexLocation = -1
    with open(dir + "\getByTokenA.txt", "r") as f1:
        tokens_text = f1.readlines()
        token_indexLocation = binarySearch(tokens_text, 0, len(tokens_text)-1, token+'\n')
    if token_indexLocation == -1:
        return token_indexLocation
    with open(dir + "\IndexFile.txt", "r") as fp:
        buffer_list = fp.readlines(int(1073741824))
        words_counter = 0
        token_attributes = None
        while len(buffer_list) != 0:
            words_counter += len(buffer_list)
            if token_indexLocation <= words_counter:
                token_attributes = binarySearch_withkey(buffer_list,0,len(buffer_list)-1,token_indexLocation)
                if token_attributes == -1:
                    return token_attributes
                return buffer_list[int(token_attributes)]
            buffer_list = fp.readlines(int(1073741824))

class IndexReader:
    def __init__(self, dir):
        """Creates an IndexReader which will read from
        the given directory"""
        self.dir = "../"+dir

    def getProductId(self, reviewId):
        """Returns the product identifier for the given
        review
        Returns null if there is no review with the
        given identifier"""
        try:
            result = getByReviewID(self.dir, reviewId)
            return str(result[0][:-1])
        except:
            return None

    def getReviewScore(self, reviewId):
        """Returns the score for a given review
        Returns -1 if there is no review with the given
        identifier"""
        try:
            result = getByReviewID(self.dir, reviewId)
            return int(result[1].split(',')[2][1:])
        except:
            return -1

    def getReviewHelpfulnessNumerator(self, reviewId):
        """Returns the numerator for the helpfulness of
        a given review
        Returns -1 if there is no review with the given
        identifier"""
        try:
            result = getByReviewID(self.dir, reviewId)
            return int(result[1].split(',')[0][1:])
        except:
            return -1


    def getReviewHelpfulnessDenominator(self, reviewId):
        """Returns the denominator for the helpfulness
        of a given review
        Returns -1 if there is no review with the given
        identifier"""
        try:
            result = getByReviewID(self.dir, reviewId)
            return int(result[1].split(',')[1][1:])
        except:
            return -1

    def getReviewLength(self, reviewId):
        """Returns the number of tokens in a given
        review
        Returns -1 if there is no review with the given
        identifier"""
        try:
            result = getByReviewID(self.dir, reviewId)
            return int(result[1].split(',')[3][:-2])
        except:
            return -1


    def getTokenFrequency(self, token):
        """Return the number of reviews containing a
        given token (i.e., word)
        Returns 0 if there are no reviews containing
        this token"""
        final_result = getLineBytoken(self.dir, token)
        if final_result == -1:
            return int(0)
        final_result = final_result[final_result.index("&") + 1:]
        final_result = final_result[1:-2]
        final_result = re.findall(r'\d+', final_result)
        final_result = list(map(int, final_result))
        final_result = list(dict.fromkeys(final_result))
        return len(final_result)


    def getTokenCollectionFrequency(self, token):
        """Return the number of times that a given
        token (i.e., word) appears in
        the reviews indexed
        Returns 0 if there are no reviews containing
        this token"""
        final_result = getLineBytoken(self.dir, token)
        if final_result == -1:
            return int(0)
        final_result = final_result[final_result.index("&") + 1:]
        final_result = final_result[1:-2]
        final_result = re.findall(r'\d+', final_result)
        final_result = list(map(int, final_result))
        return len(final_result)


    def getReviewsWithToken(self, token):
        """Returns a series of integers of the form id-1, freq-1, id-2, freq-2, ... such
        that id-n is the n-th review containing the
        given token and freq-n is the
        number of times that the token appears in
        review id-n
        Note that the integers should be sorted by id
        Returns an empty Tuple if there are no reviews
        containing this token"""
        final_result = getLineBytoken(self.dir, token)
        if final_result == -1:
            return ()
        final_result = final_result[final_result.index("&") + 1:]
        final_result = final_result[1:-2]
        final_result = re.findall(r'\d+', final_result)
        final_result = list(map(int, final_result))
        final_result.sort()
        if len(final_result) == 1:
            temporary = (final_result[0], 1)
            return temporary
        res = []
        prev_reviewID = final_result[0]
        counter = 0
        for item in final_result:
            if prev_reviewID == item:
                counter += 1
            else:
                temporary = (prev_reviewID, counter)
                res.append(temporary)
                counter = 1
                prev_reviewID = item
        temporary = (final_result[len(final_result) - 1], counter)
        res.append(temporary)
        return tuple(res)


    def getNumberOfReviews(self):
        """Return the number of product reviews
        available in the system"""
        with open(self.dir + "\getByReviewId" + ".txt", "r") as f1:
            buffer_text = f1.readlines(int(1073741824))
            reviews_No = 0
            while len(buffer_text) != 0:
                reviews_No += len(buffer_text)
                buffer_text = f1.readlines(int(1073741824))
            buffer_text.clear()
            return int(reviews_No/2)


    def getTokenSizeOfReviews(self):
        """Return the number of tokens in the system
        (Tokens should be counted as many times as they
        appear)"""
        with open(self.dir + "\getByReviewId" + ".txt", "r") as f1:
            buffer_text = f1.readlines(int(1073741824))
            token_counter = 0
            index_line = 1
            while len(buffer_text) != 0:
                for item in buffer_text:
                    if index_line % 2 == 0:
                        token_counter += int(item.split(',')[3][:-2])
                    index_line += 1
                buffer_text = f1.readlines(int(1073741824))
            buffer_text.clear()
            return int(token_counter)


    def getProductReviews(self, productId):
        """Return the ids of the reviews for a given
        product identifier
        Note that the integers returned should be
        sorted by id
        Returns an empty Tuple if there are no reviews
        for this product"""
        results_tuple = []
        with open(self.dir + "\getByReviewId" + ".txt", "r") as f1:
            buffer_text = f1.readlines(int(1073741824))
            index_line = 1
            while len(buffer_text) != 0:
                for item in buffer_text:
                    if index_line % 2 != 0:
                        line = str(item[:-1])
                        if productId == line:
                            results_tuple.append(int(index_line / 2) + 1)
                    index_line += 1
                buffer_text = f1.readlines(int(1073741824))
            buffer_text.clear()
            return tuple(results_tuple)

