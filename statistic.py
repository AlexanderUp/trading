# encoding:utf-8
# module for simple statistic operations


from collections import Counter


class StatisticCalc():

    def __init__(self, source):
        self.source = source
        self.average = self.average()
        self.median = self.median()
        self.mode = self.mode()
        self.swing = self.swing()
        self.dispersion = self.dispersion()
        self.quality_of_standard_deviation = self.quality_of_standard_deviation()

    def average(self):
        return sum(self.source)/len(self.source)

    def median(self):
        if len(self.source) % 2:
            return sorted(self.source)[len(self.source) // 2]
        return sum(sorted(self.source)[(len(self.source) // 2 - 1):(len(self.source) // 2 + 1)]) / 2

    def mode(self):
        c = Counter(self.source)
        return c.most_common()[0][0]

    def swing(self):
        return max(self.source) - min(self.source)

    def dispersion(self):
        s = sum([(x - self.average) ** 2 for x in self.source])
        return s / len(self.source)

    def quality_of_standard_deviation(self):
        return self.dispersion ** 0.5

    def emission_clearance(self, source, average, quality_of_standard_deviation):
        lower_limit = average - quality_of_standard_deviation
        upper_limit = average + quality_of_standard_deviation
        source = [x for x in source if x < upper_limit or x > lower_limit]
        return source

    def covariance(self, other):
        '''Other sequence should be same lenght as self.source!'''
        zipped_sequence = list(zip(self.source, other.source))
        temp_list = [(x - self.average) * (y - other.average) for x, y in zipped_sequence]
        return sum(temp_list) / len(self.source)

    def correlation(self, other):
        return self.covariance(other) / (self.quality_of_standard_deviation * other.quality_of_standard_deviation)
