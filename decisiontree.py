import math
from db import DB
from tree import Tree

class DecisionTree:
    __db = None
    __tree = None
    __collection = None
    # __finalv1 = None
    # __finalv2 = None

    def __init__(self, selection):
        if selection == "tennis":
            self.__collection = selection
            self.__db = DB("tennis", "tennis-attr.txt")
            self.__db.load_initial_data("tennis", "booktennis-train.txt")
            self.__finalv1 = "Yes"
            self.__finalv2 = "No"

    # def calculate_entropy(self, positive_examples, negative_examples):
    #     total_examples = positive_examples + negative_examples
    #     entropy = - ((positive_examples / total_examples) * math.log2(positive_examples / total_examples)) - \
    #               ((negative_examples / total_examples) * math.log2(negative_examples / total_examples))
    #     return entropy
    #
    # def collection_entropy(self):
    #     finalattr = self.__db.last_column(self.__collection)
    #     v1count = len(self.__db.fetch_matching_rows(self.__collection, finalattr, self.__finalv1))
    #     v2count = len(self.__db.fetch_matching_rows(self.__collection, finalattr, self.__finalv2))
    #     return self.calculate_entropy(v1count, v2count)

    def entropy(self, table):
        finalattr = self.__db.last_column(table)
        finalvalues = self.__db.possible_attribute_values(table, finalattr)
        finalvaluecounts = []
        for value in finalvalues:
            finalvaluecounts.append(len(self.__db.fetch_matching_rows(table, finalattr, value)))
        total_examples = sum(finalvaluecounts)
        entropy = 0
        for value in finalvaluecounts:
            entropy += -((value / total_examples) * math.log2(value / total_examples))
        return entropy

    def information_gain(self,table,attribute):
        samples_entropy = self.entropy(table) # Entropy of the sample
        possible_attribute_values = self.__db.possible_attribute_values(table,attribute)
        samples_per_attribute_value = [] # Number of samples per attribute value
        for value in possible_attribute_values:
            samples_per_attribute_value.append(len(self.__db.fetch_matching_rows(table,attribute,value)))
        total_attribute_samples = sum(samples_per_attribute_value) # Total samples for the attribute

        finalattr = self.__db.last_column(table)
        finalvalues = self.__db.possible_attribute_values(table, finalattr)  # Possible final values

        attribute_value_entropies = []
        for value in possible_attribute_values:
            d = {attribute:value}
            temp_view = self.__db.create_view(table,d) # Create a view temporarily
            finalvaluecounts = []
            for finalvalue in finalvalues:
                finalvaluecounts.append(len(self.__db.fetch_matching_rows(temp_view,finalattr,finalvalue)))
            self.__db.drop_view(temp_view)
            total_examples = sum(finalvaluecounts)
            entropy = 0
            for finalvalue in finalvaluecounts:
                entropy += -((finalvalue / total_examples) * math.log2(finalvalue / total_examples))
            attribute_value_entropies.append(entropy)

        information_gain = samples_entropy
        for i in range(0,len(possible_attribute_values)):
            information_gain -= (samples_per_attribute_value[i]/total_attribute_samples) * attribute_value_entropies[i]

        return information_gain

    def id3(self):
        # Incomplete.. TO DO

# dt = DecisionTree("tennis")
# dt.information_gain("tennis","Wind")
