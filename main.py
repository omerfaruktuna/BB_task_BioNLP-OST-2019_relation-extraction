import os
import re
from nltk import sent_tokenize
from Data_Class import Data_Class

#nltk.download('punkt')
directory = "BioNLP-OST-2019_BB-rel_dev"

data = Data_Class()

def Build_file_content_by_sentence(dir,db):

    """Reads each txt file in the input directory and performs sentence tokenization for each file. Returns a list with dimension equal to number of txt file in the given directory where each list item is another list that consists of sentences

    Ex: ['Atypical mycobacteria causing non-pulmonary disease in Queensland.', 'During the period 1971--7, the Tuberculosis Reference Laboratory in Queensland dealt with 52 isolates of atypical mycobacteria made from non-pulmonary sites under circumstances suggesting complicity in disease.', 'Twenty-four isolates belonging to the MAIS complex were associated with lymph node infections in children.', 'Twelve isolates belonged to the M. fortuitum-chelonei complex; most were from superficial abscesses.', 'Five cases of M. marinum infection and 8 of M. ulcerans disease were detected.']

    """

    documents = os.listdir(dir)
    documents.sort()

    for doc in documents:
        if doc.endswith(".txt"):
            with open(os.path.join(dir, doc), 'r') as f:
                file_content = f.read()

            db.file_names_ending_with_a1.append(doc[:-4] + ".a1")
            db.file_contents_by_sentence.append(sent_tokenize(file_content))

    return db.file_contents_by_sentence

def Build_sentence_indices(param_file_contents_by_sentence,db):

    """Returns a list of dictionary with dimension equal to number of txt file in the given directory. Dictionary consists of key value pairs where key's represent Sentence id's and list show beginning and end of each sentence

    Ex: {'Sentence_5': [482, 560], 'Sentence_3': [276, 382], 'Sentence_4': [382, 482], 'Sentence_2': [66, 276], 'Sentence_1': [0, 66]}

    """

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

def Build_file_contents_a1(param_file_contents_by_sentence, dir, param_file_names_ending_with_a1,db):

    """ Returns a list with dimension equal to number of txt file in the given directory where each list item is another list that consists of lines of a1 files"""

    for i in range(len(param_file_contents_by_sentence)):
        m = open(os.path.join(dir, param_file_names_ending_with_a1[i]), encoding='UTF-8')
        listOfLines = m.readlines()
        m.close()
        temp = []
        for line in listOfLines:
            temp.append(re.sub('\s+', ' ', line.strip()))

        db.file_contents_a1.append(temp)
    return db.file_contents_a1

def Update_file_contents_a1(param_file_contents_a1,db):

    """ Returns a list with dimension equal to number of txt file in the given directory where each list item is another list that consists of lines of a1 files excluding lines related with Title or Paragraph """

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

def New_a1_file_content_with_sentenceID(param_updated_file_contents_a1, param_sentences_indices,db):

    """ Returns a list with dimension equal to number of txt file in the given directory where each list item is another list that consists of lines of a1 files. But end of each line shows the sentence id of the related term in the line

    Ex: ['T3 Microorganism 9 21 mycobacteria Sentence_1', 'T4 Phenotype 22 51 causing non-pulmonary disease Sentence_1', 'T5 Habitat 34 43 pulmonary Sentence_1', 'T6 Geographical 55 65 Queensland Sentence_1', 'T7 Habitat 98 131 Tuberculosis Reference Laboratory Sentence_2']

    """

    dim_x = len(param_updated_file_contents_a1)

    for i in range(dim_x):   #Her dosya için

        db.file_contents_a1_with_sentenceID.append([])

        dim_y = len(param_updated_file_contents_a1[i])

        for j in range(dim_y):  #Dosyadaki her satır için

            tmp = param_updated_file_contents_a1[i][j]
            #print(tmp.split()[2])

            for z in range(len(param_sentences_indices[i])):

                if int(tmp.split()[2]) >= int(param_sentences_indices[i]["Sentence_" + str(z + 1)][0]) and int(tmp.split()[2]) <= int(param_sentences_indices[i]["Sentence_" + str(z + 1)][1]):

                    db.file_contents_a1_with_sentenceID[i].append(param_updated_file_contents_a1[i][j])

                    db.file_contents_a1_with_sentenceID[i][j] = db.file_contents_a1_with_sentenceID[i][j] + " Sentence_" + str(z + 1)
                    break

    return db.file_contents_a1_with_sentenceID

def Result_Helper_Function(param_file_contents_a1_with_sentenceID,db):

    """Returns a list of dictionary where each dictionary is in below format:

    Ex: {'Phenotype': ['Sentence_1', 'Sentence_2'], 'Microorganism': ['Sentence_1', 'Sentence_2', 'Sentence_4', 'Sentence_5', 'Sentence_5'], 'Habitat': ['Sentence_1', 'Sentence_2', 'Sentence_2', 'Sentence_3', 'Sentence_3', 'Sentence_3', 'Sentence_4'], 'Geographical': ['Sentence_1', 'Sentence_2']}

    """

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

def Find_Relationship(param_result_helper_list,db):

    dim_x = len(param_result_helper_list)
    for i in range(dim_x):
        dim_y = len(db.file_contents_a1_with_sentenceID[i])
        if 'Microorganism' in param_result_helper_list[i] and 'Phenotype' in param_result_helper_list[i]:
            tmp_1 = param_result_helper_list[i]['Microorganism']
            tmp_2 = param_result_helper_list[i]['Phenotype']
            intersect = list(set(tmp_1) & set(tmp_2))

            if len(intersect) != 0:

                with open(db.file_names_ending_with_a1[i][:-3]+".a2", 'w+') as the_file:

                    num_lines = sum(1 for line in open(db.file_names_ending_with_a1[i][:-3]+".a2"))

                    for m in range(len(intersect)):

                        for j in range(dim_y):

                            if intersect[m] == db.file_contents_a1_with_sentenceID[i][j].split()[-1] and db.file_contents_a1_with_sentenceID[i][j].split()[1] == "Microorganism":
                                tmp_t1 = db.file_contents_a1_with_sentenceID[i][j].split()[0]

                            if intersect[m] == db.file_contents_a1_with_sentenceID[i][j].split()[-1] and db.file_contents_a1_with_sentenceID[i][j].split()[1] == "Phenotype":

                                tmp_t2 = db.file_contents_a1_with_sentenceID[i][j].split()[0]

                        the_file.write('R{}\tExhibits\tMicroorganism:{}\tProperty:{}\n'.format(num_lines+m+1,tmp_t1,tmp_t2))


################################################

        if 'Microorganism' in param_result_helper_list[i] and 'Habitat' in param_result_helper_list[i]:
            tmp_1 = param_result_helper_list[i]['Microorganism']
            tmp_2 = param_result_helper_list[i]['Habitat']
            intersect = list(set(tmp_1) & set(tmp_2))

            if len(intersect) != 0:

                with open(db.file_names_ending_with_a1[i][:-3]+".a2", 'a+') as the_file:

                    num_lines = sum(1 for line in open(db.file_names_ending_with_a1[i][:-3]+".a2"))
                    for m in range(len(intersect)):
                        for j in range(dim_y):


                            if intersect[m] == db.file_contents_a1_with_sentenceID[i][j].split()[-1] and db.file_contents_a1_with_sentenceID[i][j].split()[1] == "Microorganism":
                                tmp_t1 = db.file_contents_a1_with_sentenceID[i][j].split()[0]

                            if intersect[m] == db.file_contents_a1_with_sentenceID[i][j].split()[-1] and db.file_contents_a1_with_sentenceID[i][j].split()[1] == "Habitat":

                                tmp_t2 = db.file_contents_a1_with_sentenceID[i][j].split()[0]

                        the_file.write('R{}\tLives_In\tMicroorganism:{}\tLocation:{}\n'.format(num_lines+m+1,tmp_t1,tmp_t2))

################################################

        if 'Microorganism' in param_result_helper_list[i] and 'Geographical' in param_result_helper_list[i]:
            tmp_1 = param_result_helper_list[i]['Microorganism']
            tmp_2 = param_result_helper_list[i]['Geographical']
            intersect = list(set(tmp_1) & set(tmp_2))

            if len(intersect) != 0:

                with open(db.file_names_ending_with_a1[i][:-3]+".a2", 'a+') as the_file:

                    num_lines = sum(1 for line in open(db.file_names_ending_with_a1[i][:-3]+".a2"))

                    for m in range(len(intersect)):
                        for j in range(dim_y):


                            if intersect[m] == db.file_contents_a1_with_sentenceID[i][j].split()[-1] and db.file_contents_a1_with_sentenceID[i][j].split()[1] == "Microorganism":
                                tmp_t1 = db.file_contents_a1_with_sentenceID[i][j].split()[0]

                            if intersect[m] == db.file_contents_a1_with_sentenceID[i][j].split()[-1] and db.file_contents_a1_with_sentenceID[i][j].split()[1] == "Geographical":

                                tmp_t2 = db.file_contents_a1_with_sentenceID[i][j].split()[0]

                        the_file.write('R{}\tLives_In\tMicroorganism:{}\tLocation:{}\n'.format(num_lines+m+1,tmp_t1,tmp_t2))

################################################

a = Build_file_content_by_sentence(directory,data)

b = Build_sentence_indices(a,data)

c = Build_file_contents_a1(a, directory, data.file_names_ending_with_a1,data)

d = Update_file_contents_a1(c,data)

e = New_a1_file_content_with_sentenceID(d, b,data)

f = Result_Helper_Function(e,data)

Find_Relationship(f,data)

#print(data.file_names_ending_with_a1[28])





