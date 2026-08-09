import random
from dataclasses import dataclass

@dataclass
class Gene:
    course_id: str
    slot_id: str
    room_id: str

class TimetableGA:
    def __init__(self, courses, slots, rooms, population_size=80, generations=150, mutation_rate=0.08, seed=42):
        self.courses, self.slots, self.rooms = courses, slots, rooms
        self.population_size, self.generations = population_size, generations
        self.mutation_rate, self.rng = mutation_rate, random.Random(seed)
        self.best_history, self.avg_history = [], []

    def random_gene(self, course):
        return Gene(course["course_id"], self.rng.choice(self.slots)["slot_id"], self.rng.choice(self.rooms)["room_id"])

    def create_individual(self):
        return [self.random_gene(c) for c in self.courses]

    def fitness(self, individual):
        penalty = 0
        courses = {c["course_id"]: c for c in self.courses}
        rooms = {r["room_id"]: r for r in self.rooms}
        teacher_slot, room_slot = set(), set()
        for g in individual:
            c, r = courses[g.course_id], rooms[g.room_id]
            ts, rs = (c["teacher_id"], g.slot_id), (g.room_id, g.slot_id)
            if ts in teacher_slot: penalty += 20
            if rs in room_slot: penalty += 20
            teacher_slot.add(ts); room_slot.add(rs)
            if int(r["capacity"]) < int(c["students"]): penalty += 15
        return 1 / (1 + penalty)

    def select(self, pop, scores):
        ids = self.rng.sample(range(len(pop)), 3)
        return pop[max(ids, key=lambda i: scores[i])]

    def crossover(self, a, b):
        p = self.rng.randint(1, len(a)-1)
        return a[:p] + b[p:]

    def mutate(self, child):
        out = []
        for g in child:
            if self.rng.random() < self.mutation_rate:
                if self.rng.random() < 0.5:
                    g = Gene(g.course_id, self.rng.choice(self.slots)["slot_id"], g.room_id)
                else:
                    g = Gene(g.course_id, g.slot_id, self.rng.choice(self.rooms)["room_id"])
            out.append(g)
        return out

    def evolve(self):
        pop = [self.create_individual() for _ in range(self.population_size)]
        best, best_score = None, -1
        for _ in range(self.generations):
            scores = [self.fitness(x) for x in pop]
            mx, avg = max(scores), sum(scores)/len(scores)
            self.best_history.append(mx); self.avg_history.append(avg)
            i = scores.index(mx)
            if mx > best_score:
                best_score = mx
                best = [Gene(g.course_id,g.slot_id,g.room_id) for g in pop[i]]
            if best_score >= 1: break
            new = [best]
            while len(new) < self.population_size:
                new.append(self.mutate(self.crossover(self.select(pop,scores), self.select(pop,scores))))
            pop = new
        return best, best_score
