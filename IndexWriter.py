import re
import shutil
import datetime
import os
import sys


class IndexWriter:
    index = 0
    maximum_buffersize = 1073741824 # 1 GigaByte
    term_dict = {}

    # private method to save in a dictionary <Term,term_ID>
    def add_to_dict(self, text):
        words_array = re.findall("[a-zA-Z0-9]+", text)
        for word in words_array:  # word in each review
            if word not in self.term_dict.keys():
                self.term_dict[word] = 0
    # private method to check a list of 4 items if all -1 then return false
    def Check_listZero(self,list):
        if list[0] == list[1] == list[2] == list[3] == -1:
            return False
        return True
    """ Split a strig of pairs (123,123)"""
    def get_Leftnumber(self, item):
        return int(item[:item.index(',')])

    def get_Rightnumber(self, item):
        return int(item[item.index(',')+1:])

    """ merge to sorted files of pairs """
    def merge_posting(self, buffer1, buffer2, output):
        b1_next = buffer1.readline()
        b2_next = buffer2.readline()
        while not (b1_next == '' and b2_next == ''):
            line1 = b1_next.split(",")
            line2 = b2_next.split(",")
            if line1[0] == '':
                output.write(b2_next)
                b2_next = buffer2.readline()
            elif line2[0] == '':
                output.write(b1_next)
                b1_next = buffer1.readline()
            elif int(line1[0]) < int(line2[0]):
                output.write(b1_next)
                b1_next = buffer1.readline()
            elif int(line1[0]) > int(line2[0]):
                output.write(b2_next)
                b2_next = buffer2.readline()
            else: # if equal
                output.write(b1_next)
                output.write(b2_next)
                b1_next = buffer1.readline()
                b2_next = buffer2.readline()

    def write(self, inputFile, dir):
        # checking if the file to read already exists on the disk
        if os.path.exists(inputFile) == False:
            print("file doesn't exist" + inputFile)
            return
        # checking if the directory already exists on the disk and creating new one if not exist
        if os.path.exists("../"+dir) == False:
            os.mkdir("../"+dir)
        # open the file to file to read the reviews
        try:
            reviews = open(inputFile)
        except:
            print("couldn't read file")
            return
        # create or open the first file to save the data inside
        try:
            opened_file = open("../"+dir + "\getByReviewId" + ".txt", 'w')
        except:
            print("couldn't open file getByReviewId.bin try again later")
            return
        # create or open the first file to save the data inside
        try:
            open_textFile = open("../"+dir + "\getByTokenB" + ".txt", 'w')
        except:
            print("couldn't open file 3")
            return
        """
        the first block:
             1- will analyse the reviews file in order to save it's attributes in special file named getByReviewID.txt 
             2- save in memeory a dictionary of term,termID
             3- write each review/text to a new file in order to analyse later after coverting 
                                                        it to lower case and remove every non alpha character
        """
        items = ['product/productId', 'review/helpfulness', 'review/score', 'review/text']
        pattern = re.compile('[^A-Za-z0-9]+')
        list_to_compress = [-1, -1, -1, -1]
        temporary = ""
        lower_result = ""
        buffer_text = reviews.readlines(int(self.maximum_buffersize))
        while len(buffer_text) != 0:
            for line in buffer_text:
                if line.startswith(items[0]):
                    temporary = line[19:-1]
                elif line.startswith(items[1]):
                    temp = line[20:]
                    list_to_compress[0] = (int(temp[:temp.index("/")]))
                    list_to_compress[1] = (int(temp[temp.index("/") + 1:]))
                elif line.startswith(items[2]):
                    temp = line[14:]
                    list_to_compress[2] = (int(float(temp)))
                elif line.startswith(items[3]):
                    temp = line[13:]
                    temp = re.sub("[^a-zA-Z0-9]+", " ", temp)  # removing every non alpha character
                    lower_result = temp.lower()  # convert each char to lower case
                    list_to_compress[3] = (int(len(re.split(" +", lower_result))))
                elif line == '\n':
                    if temporary != "" and self.Check_listZero(list_to_compress) == True:
                        opened_file.write(temporary + '\n' + str(list_to_compress) + '\n')
                        open_textFile.write(lower_result + '\n')
                        self.add_to_dict(lower_result)
                    temporary = ""
                    list_to_compress = [-1, -1, -1, -1]
            buffer_text = reviews.readlines(int(self.maximum_buffersize))
        buffer_text = " "
        # clearing memory
        del buffer_text
        del pattern
        del items
        # to make sure everything is ok and last review will be written to file
        if temporary != "" and self.Check_listZero(list_to_compress) == True:
            opened_file.write(temporary + '\n' + str(list_to_compress) + '\n')
            open_textFile.write((lower_result) + '\n')
            self.add_to_dict(lower_result)
        del temporary
        del list_to_compress
        del lower_result
        opened_file.close()
        open_textFile.close()
        del opened_file
        del open_textFile

        """
        the second block :
            1-will write each word in a special line in getByTokenA.txt and give each word the line that 
                present it like and ID
            Note: our Dictionary will be presented like >> <Term,Term_ID>
        """
        try:
            open_stringFile = open("../"+dir + "\getByTokenA" + ".txt", 'w')
        except:
            print("couldn't open file getByTokenA")
            return
        for word in sorted(self.term_dict.keys()):
            self.term_dict[word] = self.index
            self.index += 1
            open_stringFile.write(word+'\n')
        open_stringFile.close()
        del open_stringFile

        """
        the Third Block :
            will analysis the review text file that was written in first block and creating a new Dictionary 
                <Term,[1,2,3,4,.....,]>  numbers present the reviewID that this term was presented in
                this dictionary after a specific size will stop appending and write the first pairs file sorted ...
        """
        try:
            written_file = open("../"+dir + "\getByTokenB" + ".txt", 'r')
        except:
            print("couldn't open file getByTokenB")
            return
        self.maximum_buffersize = int(12582972 * 4)
        file_number = 0
        buffer_list = {}
        line_counter = 1
        if os.path.exists("../SortedLists0") == False:
            os.mkdir("../SortedLists0")
        for line in written_file:
            words_array = re.findall("[a-zA-Z0-9]+", line)
            for word in words_array:
                if word in buffer_list:
                    buffer_list[word].append(line_counter)
                else:
                    buffer_list[word] = [line_counter]
            if sys.getsizeof(buffer_list) >= self.maximum_buffersize: # writing to pairs file sorted
                try:
                    lists_file = open("../SortedLists0" + "\getByTokenC" + str(file_number + 1) + ".txt", 'w')
                    file_number += 1
                except:
                    print("couldn't open file getByTokenC")
                    return
                for x in sorted(buffer_list.keys()):
                    for i in range(0, len(buffer_list[x])):
                        lists_file.write(str(self.term_dict[x]) + "," + str(buffer_list[x][i]) + '\n')
                lists_file.close()
                buffer_list.clear()
            line_counter += 1
        written_file.close()
        del written_file
        # removing review texts file
        os.remove("../"+dir + "\getByTokenB.txt")
        del line_counter
        # making sure for last dictionary to be written after finishing the review text file
        if len(buffer_list.keys()) > 0:
            try:
                lists_file = open("../SortedLists0" + "\getByTokenC" + str(file_number + 1) + ".txt", 'w')
                file_number += 1
            except:
                print("couldn't open file getByTokenC")
                return
            for x in sorted(buffer_list.keys()):
                for i in range(0, len(buffer_list[x])):
                    lists_file.write(str(self.term_dict[x]) + "," + str(buffer_list[x][i]) + '\n')
            lists_file.close()
        del lists_file
        buffer_list.clear()
        del buffer_list
        self.term_dict.clear()

        """
        the Forth block :
            will merge each pairs file in order to get one file for pairs 
        """
        directory_counter = 1
        while file_number != 1:
            if os.path.exists("../SortedLists" + str(directory_counter)) == False:
                os.mkdir("../SortedLists" + str(directory_counter))
            i = 1
            j = i + 1
            output_counter = 0
            while i <= file_number:
                file_moved: bool = False
                try:
                    file1 = open("../SortedLists" + str(directory_counter - 1) + "\getByTokenC" + str(i) + ".txt", 'r')
                except:
                    print("couldn't open file i" + str(i))
                    return
                try:
                    output_file = open("../SortedLists" + str(directory_counter) + "\getByTokenC" +
                                       str(output_counter + 1) + ".txt",'w')
                    output_counter += 1
                except:
                    print("couldn't open file output" + str(output_counter))
                    return
                try:
                    file2 = open("../SortedLists" + str(directory_counter - 1) + "\getByTokenC" + str(j) + ".txt", 'r')
                except:
                    file1.close()
                    shutil.move("../SortedLists" + str(directory_counter - 1) + "\getByTokenC" + str(i) + ".txt",
                                "../SortedLists" + str(directory_counter) + "\getByTokenC" + str(
                                    output_counter) + ".txt")
                    file_moved = True
                if file_moved == False:
                    self.merge_posting(file1, file2, output_file)
                    file1.close()
                file2.close()
                output_file.close()
                i += 2
                j += 2
            shutil.rmtree("../SortedLists" + str(directory_counter - 1), ignore_errors=False, onerror=None)
            file_number = output_counter
            directory_counter += 1

        """
        The Fifth Block :
            will convert the merged pairs file in order to make the index file 
                our index file will be present like this >> 
                TermID,[] >> this list present the review ID that this token was mentioned in 
        """
        try:
            pairs_file = open("../SortedLists" + str(directory_counter - 1) + "\getByTokenC1" + ".txt", 'r')
            index_file = open("../"+dir + "\IndexFile" + ".txt", 'w')
        except:
            print("couldn't open file pairs_file or index file")
            return
        self.maximum_buffersize = 1073741824 # 1 GigaByte
        my_list = []
        buffer_pairs = pairs_file.readlines(self.maximum_buffersize)
        prev_id = self.get_Leftnumber(buffer_pairs[0])
        my_list.append(int(self.get_Rightnumber(buffer_pairs[0])))
        while len(buffer_pairs) != 0:
            for item in buffer_pairs:
                curr_id = int(self.get_Leftnumber(item))
                if prev_id == curr_id:
                    my_list.append(int(self.get_Rightnumber(item)))
                else:
                    index_file.write(str(prev_id) + "&" + str(my_list)+"\n")
                    my_list.clear()
                    my_list.append(int(self.get_Rightnumber(item)))
                    prev_id = curr_id
            buffer_pairs = pairs_file.readlines(self.maximum_buffersize)
        pairs_file.close()
        # making sure to write the last pairs for last term
        if len(my_list) > 0:
            index_file.write(str(prev_id) + "&" + str(my_list) + "\n")
        index_file.close()
        del buffer_pairs
        del prev_id
        del my_list
        # delete this pairs file form disk
        shutil.rmtree("../SortedLists" + str(directory_counter-1), ignore_errors=False, onerror=None)

    #removing the directory of index files
    def removeIndex(self, dir):
        if os.path.exists("../"+dir) == True:
            shutil.rmtree("../"+dir, ignore_errors=False, onerror=None)
            print("directory removed")
        else:
            print("No Index")

