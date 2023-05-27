
class Requirement:
    def __init__(self, phrase :str):
        self.phrase = phrase
        self.count = 1
        self.subrequirements: dict[Requirement] = {}

    def increment_count(self):
        self.count += 1

    def add_subrequirement(self, subrequirement):
        self.subrequirements[subrequirement.phrase] = subrequirement

    def check_subrequirement(self, new_phrase: str):
        def is_valid_subrequirement(new_phrase):
            requirement_words = self.phrase.split()
            subrequirement_words = new_phrase.split()

            if len(requirement_words) + 1 != len(subrequirement_words):
                return False

            for i in range(len(requirement_words)):
                if requirement_words[i] != subrequirement_words[i]:
                    return False
            return True
        if is_valid_subrequirement(new_phrase):
            new_phrase_is_current_subrequirement = False
            for subrequirement in self.subrequirements.values():
                if new_phrase == subrequirement.phrase:
                    self.subrequirements[new_phrase].increment_count()
                    new_phrase_is_current_subrequirement = True
            if not new_phrase_is_current_subrequirement:
                self.add_subrequirement(Requirement(phrase=new_phrase))
        else:
            for subrequirement in self.subrequirements.values():
                if subrequirement.phrase in new_phrase:
                    subrequirement.check_subrequirement(new_phrase)

    def print_requirements(self):
        print(f"{self.phrase}, count: {self.count}")
        for subrequirement in self.subrequirements.values():
            subrequirement.print_subrequirements()

    def print_subrequirements(self):
        for subrequirement in self.subrequirements.values():
            print(f"{subrequirement.phrase}, count: {subrequirement.count}")
            subrequirement.print_subrequirements()

