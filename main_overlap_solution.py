import os
import re
from nltk import sent_tokenize
from Data_Class import Data_Class



from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

import  nltk

nltk.download('punkt')

punkt_param = PunktParameters()
abbreviation = ["u.s.a", "fig", "Fig","et al", "i,e", "e.g", "ref", "c.f", "Eq", "e.q", "eqn", "Eqn", "dr", "Dr"]

punkt_param.abbrev_types = set(abbreviation)
tokenizer = PunktSentenceTokenizer(punkt_param)




# nltk.download('punkt')
directory = "BioNLP-OST-2019_BB-rel_dev"

data = Data_Class()


def Build_file_content_by_sentence(dir, db):
    """Reads each txt file in the input directory and performs sentence tokenization for each file. Returns a list with dimension equal to number of txt file in the given directory where each list item is another list consists of sentences"""

    documents = os.listdir(dir)
    documents.sort()

    for doc in documents:
        if doc.endswith(".txt"):
            with open(os.path.join(dir, doc), 'r') as f:
                file_content = f.read()

            db.file_names_ending_with_a1.append(doc[:-4] + ".a1")
            #db.file_contents_by_sentence.append(sent_tokenize(file_content))
            db.file_contents_by_sentence.append(tokenizer.tokenize(file_content))

    return db.file_contents_by_sentence


def Build_sentence_indices(param_file_contents_by_sentence, db):
    for a in range(len(param_file_contents_by_sentence)):
        j = 0
        begin, end = 0, 0
        for i in range(len(param_file_contents_by_sentence[a])):
            tmp = []
            offset = len(param_file_contents_by_sentence[a][i])
            end = begin + offset
            tmp.append(begin)
            tmp.append(end)
            db.sentences_indices["Sentence_" + str(i + 1)] = tmp

            begin = end
            j = j + 1

        db.sentences_indices_list.append(db.sentences_indices)
        db.sentences_indices = {}

    return db.sentences_indices_list


def Build_file_contents_a1(param_file_contents_by_sentence, dir, param_file_names_ending_with_a1, db):
    for i in range(len(param_file_contents_by_sentence)):
        m = open(os.path.join(dir, param_file_names_ending_with_a1[i]), encoding='UTF-8')
        listOfLines = m.readlines()
        m.close()
        temp = []
        for line in listOfLines:
            # temp.append(line)
            temp.append(re.sub('\s+', ' ', line.strip()))

        db.file_contents_a1.append(temp)
    return db.file_contents_a1


def Update_file_contents_a1(param_file_contents_a1, db):
    dim_x = len(param_file_contents_a1)

    for i in range(dim_x):
        dim_y = len(param_file_contents_a1[i])
        db.updated_file_contents_a1.append([])

        for j in range(dim_y):
            if "Title" in str(param_file_contents_a1[i][j][0:12]) or "Paragraph" in str(
                    param_file_contents_a1[i][j][0:12]):
                pass
            else:
                db.updated_file_contents_a1[i].append(param_file_contents_a1[i][j])

    return db.updated_file_contents_a1



def New_a1_file_content_with_sentenceID(param_updated_file_contents_a1, param_sentences_indices, db):
    dim_x = len(param_updated_file_contents_a1)

    for i in range(dim_x):  # Her dosya için

        db.file_contents_a1_with_sentenceID.append([])

        dim_y = len(param_updated_file_contents_a1[i])

        for j in range(dim_y):  # Dosyadaki her satır için

            tmp = param_updated_file_contents_a1[i][j]
            # print(tmp.split()[2])

            for z in range(len(param_sentences_indices[i])):

                if int(tmp.split()[2]) >= int(param_sentences_indices[i]["Sentence_" + str(z + 1)][0]) and int(
                        tmp.split()[2]) <= int(param_sentences_indices[i]["Sentence_" + str(z + 1)][1]):
                    db.file_contents_a1_with_sentenceID[i].append(param_updated_file_contents_a1[i][j])

                    db.file_contents_a1_with_sentenceID[i][j] = db.file_contents_a1_with_sentenceID[i][
                                                                    j] + " Sentence_" + str(z + 1)
                    break

    return db.file_contents_a1_with_sentenceID

###################################
def Remove_overlap(param,db):

    tmp_list = []
    dim_x = len(param)

    for i in range(dim_x):

        we = []
        db.file_contents_a1_with_sentenceID_shotened.append([])
        db.overlap_indices.append([])
        tmp_list.append([])
        dim_y = len(param[i])

        for j in range(dim_y):
            tmp = param[i][j].split()[4:]
            we.append(tmp[-1])
            for t2 in tmp[:-1]:
                we.append(t2)

            tmp_res= ''

            for element in we:
                tmp_res += str(element)

            tmp_list[i].append(tmp_res)
            we = []
            #db.file_contents_a1_with_sentenceID_shotened[i].append(tmp_res)
    for i in range(dim_x):
        for j in range(len(tmp_list[i])):
            count = 0
            tmp_word = tmp_list[i][j]

            for t_1 in tmp_list[i]:
                if tmp_word in t_1:
                    count += 1
            if count > 1:
                db.overlap_indices[i].append(j)

            count = 0
    for i in range(dim_x):
      for j in range(len(param[i])):
        if j not in db.overlap_indices[i]:
          db.file_contents_a1_with_sentenceID_shotened[i].append(param[i][j])

    #db.overlap_indices [3, 4, 5, 9, 10, 11, 18, 19]
    #return db.file_contents_a1_with_sentenceID_shotened
    return db.file_contents_a1_with_sentenceID_shotened

############


def Result_Helper_Function(param_file_contents_a1_with_sentenceID, db):
    dim_x = len(param_file_contents_a1_with_sentenceID)

    for i in range(dim_x):

        dim_y = len(param_file_contents_a1_with_sentenceID[i])

        entity_set = set()

        for j in range(dim_y):
            entity_set.add(param_file_contents_a1_with_sentenceID[i][j].split()[1])

        for entity in entity_set:
            db.result_helper[entity] = []

        for j in range(dim_y):
            qw = param_file_contents_a1_with_sentenceID[i][j].split()[1]

            db.result_helper[qw].append(param_file_contents_a1_with_sentenceID[i][j].split()[-1])

        db.result_helper_list.append(db.result_helper)
        db.result_helper = {}

    return db.result_helper_list


def Find_Relationship(param_result_helper_list, db):
    dim_x = len(param_result_helper_list)

    for i in range(dim_x):

        dim_y = len(db.file_contents_a1_with_sentenceID_shotened[i])

        if 'Microorganism' in param_result_helper_list[i] and 'Phenotype' in param_result_helper_list[i]:
            tmp_1 = param_result_helper_list[i]['Microorganism']
            tmp_2 = param_result_helper_list[i]['Phenotype']

            intersect = list(set(tmp_1) & set(tmp_2))
            # intersect = list(set(tmp_1).union(set(tmp_2)))

            if len(intersect) != 0:

                num_lines = sum(1 for line in open(db.file_names_ending_with_a1[i][:-3] + ".a2"))

                q = 0

                with open(db.file_names_ending_with_a1[i][:-3] + ".a2", 'a+') as the_file:


                    for m in range(len(intersect)):

                        tmp_t1 = []
                        tmp_t2 = []

                        for j in range(dim_y):

                            if intersect[m] == db.file_contents_a1_with_sentenceID_shotened[i][j].split()[-1] and \
                                    db.file_contents_a1_with_sentenceID_shotened[i][j].split()[1] == "Microorganism":
                                tmp_t1.append(db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0])
                                # tmp_t1 = db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0]

                            if intersect[m] == db.file_contents_a1_with_sentenceID_shotened[i][j].split()[-1] and \
                                    db.file_contents_a1_with_sentenceID_shotened[i][j].split()[1] == "Phenotype":
                                tmp_t2.append(db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0])
                                # tmp_t2 = db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0]

                        for r in range(len(tmp_t1)):
                            the_file.write(
                                'R{}\tExhibits Microorganism:{} Property:{}\n'.format(num_lines + q + m + r + 1, tmp_t1[r],
                                                                                      tmp_t2[0]))
                        q = q + r
                        #num_lines = num_lines + 1



                        # the_file.write('R{}\tExhibits Microorganism:{} Property:{}\n'.format(num_lines+m+1,tmp_t1,tmp_t2))

        ################################################

        if 'Microorganism' in param_result_helper_list[i] and 'Habitat' in param_result_helper_list[i]:
            tmp_1 = param_result_helper_list[i]['Microorganism']
            tmp_2 = param_result_helper_list[i]['Habitat']
            intersect = list(set(tmp_1) & set(tmp_2))
            # intersect = list(set(tmp_1).union(set(tmp_2)))

            if len(intersect) != 0:

                num_lines = sum(1 for line in open(db.file_names_ending_with_a1[i][:-3] + ".a2"))

                q = 0

                with open(db.file_names_ending_with_a1[i][:-3] + ".a2", 'a+') as the_file:

                    for m in range(len(intersect)):
                        tmp_t1 = []
                        tmp_t2 = []

                        for j in range(dim_y):

                            if intersect[m] == db.file_contents_a1_with_sentenceID_shotened[i][j].split()[-1] and \
                                    db.file_contents_a1_with_sentenceID_shotened[i][j].split()[1] == "Microorganism":
                                tmp_t1.append(db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0])
                                # tmp_t1 = db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0]

                            if intersect[m] == db.file_contents_a1_with_sentenceID_shotened[i][j].split()[-1] and \
                                    db.file_contents_a1_with_sentenceID_shotened[i][j].split()[1] == "Habitat":
                                tmp_t2.append(db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0])
                                # tmp_t2 = db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0]

                        for r in range(len(tmp_t2)):
                            the_file.write(
                                'R{}\tLives_In Microorganism:{} Location:{}\n'.format(num_lines + q + m + r + 1, tmp_t1[0],
                                                                                      tmp_t2[r]))
                        q = q + r

                        #num_lines = num_lines + 1

                        # the_file.write('R{}\tLives_In Microorganism:{} Location:{}\n'.format(num_lines+m+1,tmp_t1,tmp_t2))

        ################################################

        if 'Microorganism' in param_result_helper_list[i] and 'Geographical' in param_result_helper_list[i]:
            tmp_1 = param_result_helper_list[i]['Microorganism']
            tmp_2 = param_result_helper_list[i]['Geographical']
            intersect = list(set(tmp_1) & set(tmp_2))
            # intersect = list(set(tmp_1).union(set(tmp_2)))

            if len(intersect) != 0:

                num_lines = sum(1 for line in open(db.file_names_ending_with_a1[i][:-3] + ".a2"))

                q = 0

                with open(db.file_names_ending_with_a1[i][:-3] + ".a2", 'a+') as the_file:

                    for m in range(len(intersect)):
                        tmp_t1 = []
                        tmp_t2 = []

                        for j in range(dim_y):

                            if intersect[m] == db.file_contents_a1_with_sentenceID_shotened[i][j].split()[-1] and \
                                    db.file_contents_a1_with_sentenceID_shotened[i][j].split()[1] == "Microorganism":
                                tmp_t1.append(db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0])
                                # tmp_t1 = db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0]

                            if intersect[m] == db.file_contents_a1_with_sentenceID_shotened[i][j].split()[-1] and \
                                    db.file_contents_a1_with_sentenceID_shotened[i][j].split()[1] == "Geographical":
                                tmp_t2.append(db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0])
                                # tmp_t2 = db.file_contents_a1_with_sentenceID_shotened[i][j].split()[0]

                        for r in range(len(tmp_t2)):
                            the_file.write(
                                'R{}\tLives_In Microorganism:{} Location:{}\n'.format(num_lines + m + q + r + 1, tmp_t1[0],
                                                                                      tmp_t2[r]))
                        q = q + r
                        #num_lines = num_lines + 1

                        # the_file.write('R{}\tLives_In Microorganism:{} Location:{}\n'.format(num_lines+m+1,tmp_t1,tmp_t2))


################################################

a = Build_file_content_by_sentence(directory, data)

b = Build_sentence_indices(a, data)

c = Build_file_contents_a1(a, directory, data.file_names_ending_with_a1, data)

d = Update_file_contents_a1(c, data)

#######*******************************################33


e = New_a1_file_content_with_sentenceID(d, b, data)

e_2 = Remove_overlap(e,data)

for i in range(len(data.file_names_ending_with_a1)):
    with open(data.file_names_ending_with_a1[i][:-3] + ".a2", 'w+') as the_file:
        pass

f = Result_Helper_Function(e_2, data)
# print(f[29])

Find_Relationship(f, data)

"""
for i in range(len(data.file_names_ending_with_a1)):
  if data.file_names_ending_with_a1[i] == "BB-rel-F-20167385-000.a1":
    print(i)
"""

print(a[48])
print("\n")
print(b[48])
print("\n")
print(c[48])
print("\n")
print(d[48])
print("\n")
print(e[48])
print("\n")
print(e_2[48])
print("\n")
print(f[48])
print("\n")



#print(remove_overlap(e,data)[1])

#print(data.overlap_indices[1])



