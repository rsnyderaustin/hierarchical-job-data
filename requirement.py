
class Requirement:
    def __init__(self, requirement: str):
        self.requirement = requirement
        self.count = 1
        self.subrequirements: dict[Requirement] = {}
        self.subquery_iterations = 0

    def increment_count(self):
        self.count += 1

    def add_subrequirement(self, subrequirement):
        self.subrequirements[subrequirement.requirement] = subrequirement

    def process_as_subrequirement(self, new_requirement: str) -> bool:
        def is_valid_subrequirement(new_requirement):
            requirement_words = self.requirement.split()
            subrequirement_words = new_requirement.split()

            if len(requirement_words) + 1 != len(subrequirement_words):
                return False

            for i in range(len(requirement_words)):
                if requirement_words[i] != subrequirement_words[i]:
                    return False
            return True
        if is_valid_subrequirement(new_requirement):
            new_requirement_is_current_subrequirement = False
            for subrequirement in self.subrequirements.keys():
                if new_requirement == subrequirement:
                    self.subrequirements[new_requirement].increment_count()
                    new_requirement_is_current_subrequirement = True
            if not new_requirement_is_current_subrequirement:
                self.add_subrequirement(Requirement(requirement=new_requirement))
            return True
        else:
            for subrequirement in self.subrequirements:
                if subrequirement in new_requirement:
                    if self.subrequirements[subrequirement].process_as_subrequirement(new_requirement):
                        return True
        return False

    def print_requirements(self, iterations):
        print('\t' * iterations + f"{self.requirement}, count: {self.count}")
        iterations += 1
        for subrequirement in self.subrequirements.values():
            subrequirement.print_requirements(iterations)
