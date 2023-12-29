# Owen Durkin
# CS470 
# 02075415


from queue import PriorityQueue

class Anagram:
    num_iterations = 0
    def anagram_expand(self, state, goal):
        node_list = []

        # Converts state and goal to lists. Program wasn't runnign without this
        state = list(state)
        goal = list(goal)

        # Calculate the heuristic as the number of misplaced& correctly placed characters
        # Lowwest solution is closer to the goal
        score = sum(1 for a, b in zip(state, goal) if a != b)
        score += sum(1 for a, b in zip(state, goal) if a == b)

        for pos in range(1, len(state)):
            new_state = state[1:pos + 1] + [state[0]] + state[pos + 1:]
            new_state_str = ''.join(new_state) 
            node_list.append((new_state_str, score)) # new append to fix error 
            # node_list.append((new_state, score)) # this was throwing an error

        return node_list


    # TO DO: b. Return either the solution as a list of states from start to goal or [] if there is no solution.
    def a_star(self, start, goal, expand):
        open_set = PriorityQueue()
        closed_set = set()
        g_scores = {start: 0}
        f_scores = {start: 0}  # Initialize f_scores with 0
        came_from = {}  # Initialize the came_from dictionary

        open_set.put((f_scores[start], start))

        while not open_set.empty():
            current = open_set.get()[1]

            self.num_iterations += 1 # iterates the amount of A* iterations for each new node paassed

            if current == goal:
                # Reconstruct the path from the goal to the start
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            closed_set.add(current)

            for neighbor, cost in expand(current, goal):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_scores[current] + cost

                if neighbor not in [node[1] for node in open_set.queue] or tentative_g_score < g_scores[neighbor]:
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score
                    open_set.put((f_scores[neighbor], neighbor))

        return []

    # Finds a solution, i.e., the set of steps from one word to its anagram
    def solve(self,start, goal):

        self.num_iterations = 0

        # TO DO: a. Add code below to check in advance whether the problem is solvable

        # start and goal count for checking character frequencies
        startcount = {}
        goalcount = {}

        # Loop to check for solution or no solution. Also returns why the solution doesn't exist
        if (len(start) == len(goal)):
            for i in start:
                if i in startcount:
                    startcount[i] += 1
                else:
                    startcount[i] = 1
            for i in goal:
                if i in goalcount:
                    goalcount[i] += 1
                else:
                    goalcount[i] = 1
            if startcount == goalcount:
                print('Solution exists')
            else:
                print('Solution is impossible. Character frequencies differ')
        else:
            print('Solution is impossible. String length differs')

        self.solution = self.a_star(start, goal, self.anagram_expand)

        if not self.solution:
            print('No solution found')
            return "NONE"

        print(str(len(self.solution) - 1) + ' steps from start to goal:')

        for step in self.solution:
            print(step)

        print(str(self.num_iterations) + ' A* iterations were performed to find this solution.')

        return str(self.num_iterations)

if __name__ == '__main__':
    anagram = Anagram()
    anagram.solve('TEARDROP', 'PREDATOR')
    anagram.solve('ALLERGY', 'LARGELY')
    anagram.solve('GOAT', 'TOGA')
    anagram.solve('HEART', 'EARTH')