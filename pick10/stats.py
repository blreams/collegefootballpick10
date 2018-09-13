class Stats(object):
    def __init__(self):
        self.scores = []
        self.picks = 0
        self.points = 0
        self.mean = 0.0
        self.median = 0
        self.mode = 0
        self.over_under = 0

    def add_score(self, points, picks):
        if picks > 0:
            self.scores.append(points)
            self.points += points
            self.picks += picks
            self.over_under += points - (picks / 2)

    def merge_stats(self, stats):
        self.scores.extend(stats.scores)
        self.points += stats.points
        self.picks += stats.picks
        self.over_under += stats.points - (stats.picks / 2)

    def calc_stats(self):
        if len(self.scores) >= 1:
            self.mean = float(sum(self.scores)) / len(self.scores)
            self.scores.sort()
            self.median = self.scores[len(self.scores) / 2]
            qty_scores = [(self.scores.count(score), score) for score in self.scores]
            qty_scores.sort(reverse=True)
            self.mode = qty_scores[0][1]

