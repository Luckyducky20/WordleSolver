from wordle import Wordle
from solver import WordleSolver


def run_new_game(wordle, solver):
    wordle.next_game()
    solver.reset()
    # print(f"Actual word: {wordle.todays_word}")
    result = solver.solve(wordle)
    # print(f"result {result} attempts: {wordle.attempt}")
    return result, solver.attempt


def run_benchmark():
    # creating the game and solver class
    wordle = Wordle()
    solver = WordleSolver()

    # keeping track of failed and successful attempts
    failed_attempts = []
    attempt_tracker = [0,0,0,0,0,0]

    # declaring the total amount of words in the word list
    total_games = wordle.max_word_count()

    # playing through the games
    for i in range(total_games):

        # printing out the current progress
        if i % 100 == 0:
            print(f"Progress: ran {i} games")

        # running a game and storing the results
        # result is a boolean(0 or 1)
        # 1 being a win
        # 0 being a fail
        #
        # attempts records how many attempts it took to win the game
        result, attempt = run_new_game(wordle, solver)

        # if the game returned with a 0 and not a 1, then it runs this
        if not result:
            fail = (wordle.todays_word, solver.game_number, solver.attempt, solver.tries[:])
            print(fail)
            failed_attempts.append(fail)
        
        # if the game was a winning game, then it records the statisticss
        else:
            attempt_tracker[attempt-1] += 1
            
    
    # printing out all of the statistics for the games
    print(f"Ran: {total_games} games.")
    print(f"Solved: {total_games - len(failed_attempts)}/{total_games} = {((total_games - len(failed_attempts)) * 100 / total_games):.02f}%")

    print("\nWinning game on:")
    for slot, attempts in enumerate(attempt_tracker):
        print(f"Attempt {slot+1}: {attempts}")

    print("\nDetails:")
    for fail in failed_attempts:
        print(fail)

# checking who is running the file
# if it is imported, then it won't instantly run
if __name__ == '__main__':
    run_benchmark()

