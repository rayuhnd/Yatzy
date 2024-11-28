import random as r

# Initialize score sheet with category names, all set to 0
score_sheet = {
    "Ones": 0, "Twos": 0, "Threes": 0, "Fours": 0, "Fives": 0, "Sixes": 0,
    "One Pair": 0, "Two Pairs": 0, "Three of a Kind": 0, "Four of a Kind": 0,
    "Small Straight": 0, "Large Straight": 0, "Full House": 0, "Chance": 0, "Yatzy": 0
}

bonus_pt = 50

def calculate_upper():
    # Sum all integer scores from the upper section
    upper_total = 0
    for category in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
        if isinstance(score_sheet[category], int):
            upper_total += score_sheet[category]

    return upper_total

def roll_dice():
    #Function for rolling five dice, returning a list of random values between 1 and 6.
    return [r.randint(1, 6) for _ in range(5)] 

def single_player_mode():
    #Runs the game for a single player, managing rounds, rolls, and scoring.
    rolls = 0
    rounds = 0

    while rounds < 16:   # Game runs for 15 rounds
        dice = roll_dice()    # Initial roll
        rounds += 1  
        rolls = 0 
        
        if rounds == 16:  # End of game, print final scores 
            print()
            print("Final score sheet:")
            for key, value in score_sheet.items():
                print(f"{key} {value}")

            # Calculate total score, summing only integer values
            total = 0
            # Sum all integer values in score_sheet
            for value in score_sheet.values():
                if isinstance(value, int):
                    total += value
            
            # Calculate upper total and apply bonus if necessary
            upper_total = calculate_upper()
            if upper_total >= 63:
                total += bonus_pt
            
            # Print the total score
            print("Total score:", total)
            break

        
        while rolls < 3:  # Allows up to 3 rolls per round
            print(f"You rolled: {dice}")
            rolls += 1
            
            if rolls < 3:
                play_again = input("Do you want to roll again? (Type 'y' to roll again or 'n' to keep all): ").lower()
                if play_again == 'n':
                    print("You chose to keep all.")

                    print("Current score sheet:")

                    for key, value in score_sheet.items():
                        print(f"{key} {value}")
                    break
                    
                elif play_again == 'y':  # Player chooses which dice to keep
                    indices_to_keep = input("Enter indices to keep (1-5) separated by spaces, or press Enter to keep all: ")
                    if indices_to_keep:
                        dice = re_roll(indices_to_keep, dice) 
                        for key, value in score_sheet.items():
                            print(f"{key} {value}")
                    else:
                        break
        
        print(f"Final dice: {dice}")

        # Calculate upper section scores
        upper_scores = upper_section(dice)
        upper_categories = {
            "Ones": upper_scores[0], "Twos": upper_scores[1], "Threes": upper_scores[2],
            "Fours": upper_scores[3], "Fives": upper_scores[4], "Sixes": upper_scores[5]
        }
        
        # Calculate lower section scores
        one_pair, two_pairs, three_kind, four_kind, small_straight, big_straight, full_house, chance, yatzy = lower_section(dice)
        lower_categories = {
            "One Pair": one_pair, "Two Pairs": two_pairs, "Three of a Kind": three_kind,
            "Four of a Kind": four_kind, "Small Straight": small_straight,
            "Large Straight": big_straight, "Full House": full_house, "Chance": chance, "Yatzy": yatzy
        }
        
        # Merge upper and lower categories
        merged_categories = upper_categories | lower_categories

        # Filter categories with scores > 0
        new_dict = {}
        for category, score in merged_categories.items():
            if score > 0 and score_sheet[category] == 0:
                new_dict[category] = score

        # Display possible scoring categories
        index = 1
        for category, score in new_dict.items():
            print(f"{index}. {category}")
            index += 1

        # Player selects category to score
        choose_category = int(input("Choose a category by number or type 0 to cross out: "))
        
        
        if choose_category > 0:
            index = 1
            for category, value in new_dict.items():
                if index == choose_category:
                    
                    update_score_sheet(category, value) #check if category works
                   
                    for key, value in score_sheet.items():
                        print(f"{key} {value}")
                index += 1
        
        elif choose_category == 0:
            cross_out = input("Type name of category to cross out: ")  
            if cross_out in score_sheet and score_sheet[cross_out] == 0:#name has to be on table and zero has to value
                score_sheet[cross_out] = "x" #replaces with x
                
                for key, value in score_sheet.items():
                        print(f"{key} {value}")
            else:
                print("Not a valid input.")#breaks if there is value
                break
                
    return rounds
    single_player_mode()

def update_score_sheet(category, value):
    # Check if the category is already scored or crossed out
    if score_sheet[category] != "x" and score_sheet[category] == 0:  # Category not scored or crossed out
        score_sheet[category] = value
        print(f"Scored {value} points in {category}.")
    else:
        print(f"Invalid. This category already contains a score or is crossed out.")




def re_roll(keep, roll):    
    user_re_roll = keep    
    split_re_roll = user_re_roll.split() 
    lst_keep = []
    # Append lst_keep with the indices from 'roll'
    for index in split_re_roll:     
        if int(index) - 1 < len(roll): 
            lst_keep.append(roll[int(index) - 1]) 
    #print(lst_keep)  

    # Re-roll the indices that are not in 'keep'
    roll = []
    for i in lst_keep: 
        roll.append(i) 

    # Roll the remaining dice that are not in 'keep'
    for i in range(5 - len(roll)):
        rand = r.randint(1, 6) 
        roll.append(rand)
    return roll  


def upper_section(dice):
    #Calculates scores for the upper section (Ones through Sixes).
    ones, twos, threes, fours, fives, sixes = 0, 0, 0, 0, 0, 0
    for num in dice:
        if num == 1: ones += 1
        elif num == 2: twos += 2
        elif num == 3: threes += 3
        elif num == 4: fours += 4
        elif num == 5: fives += 5
        elif num == 6: sixes += 6
    return ones, twos, threes, fours, fives, sixes

def lower_section(dice): 

    # One pair
    one_pair = 0   
    lst_pair = []
    
    for i in dice: 
        if i not in lst_pair:  # The number appears the first time
            lst_pair.append(i)  
            
    count = 0       
    for i in lst_pair: 
        if count == 0:
            if dice.count(i) > 1:  # The second time, sum the numbers  
                one_pair += i + i  
                count += 1 

        # Calculate Two Pairs
    # Initialize the two_pairs score to 0 and an empty list to track unique dice values
    two_pairs = 0
    lst_two_pair = []
    
    # Add each unique value from dice to lst_two_pair
    for i in dice:
        if i not in lst_two_pair:
            lst_two_pair.append(i)
    
    # Initialize a counter for the number of pairs found
    pair_count = 0
    
    # Loop through each unique value to check for pairs
    for i in lst_two_pair:
        if dice.count(i) > 1:  # If the value appears more than once, it's a pair
            two_pairs += i * 2  # Add the value of the pair to two_pairs
            pair_count += 1     # Increment the pair count
        
        if pair_count == 2:    # Stop if two pairs have been found
            break

    # If less than two pairs were found, set two_pairs to 0 (no score)
    if pair_count < 2:
        two_pairs = 0

    # Three of a kind 
    three_kind = 0 
    lst_three_kind = [] 
    for i in dice: 
        if i not in lst_three_kind:  # Append the number the first time it appears
            lst_three_kind.append(i)

    for i in lst_three_kind: 
        if dice.count(i) == 3 or dice.count(i) > 3:  # If the number appears three or more times in dice  
            three_kind += i * 3   

    # Four of a kind  
    four_kind = 0 
    lst_four_kind = [] 
    for i in dice: 
        if i not in lst_four_kind:  # Append the number the first time it appears
            lst_four_kind.append(i)

    for i in lst_four_kind: 
        if dice.count(i) == 4 or dice.count(i) > 4:  # If the number appears four or more times in dice
            four_kind += i * 4

    # Small straight  
    small_straight = 0  
    for i in range(len(dice)):  
        dice.sort()
        if dice == [1, 2, 3, 4, 5]:  # Check if dice matches the list
            small_straight = 15 
    
    # Large straight 
    big_straight = 0 
    for i in range(len(dice)): 
        dice.sort() 
        if dice == [2, 3, 4, 5, 6]:  # Check if dice matches the list  
            big_straight = 20

    # Full house 
    full_house = 0  
    if three_kind > 0 and (one_pair > 0 or two_pairs > 0):  # Check if three of a kind has a value and if any of the pairs have a value

        three_same_value = three_kind // 3  # Get the value that was multiplied by three 

        # If the first pair is not the same as three of a kind, use that pair's value, otherwise use pair 2.
        pair_value = one_pair // 2 if (one_pair // 2) != three_same_value else two_pairs // 2 

        # Pair value must have a value and not be the same as three of a kind's value
        if pair_value > 0 and pair_value != three_same_value: 
            full_house += three_kind + (pair_value * 2) 

    # Chance 
    chance = 0 
    for i in dice:  # Sum all the numbers
        chance += i 

    # Yatzy 
    yatzy = 0 
    for i in dice: 
        if ([dice[0]] * len(dice) == dice):  # Make a list of the first number with length 5 and compare with dice
            yatzy = 50 

    return one_pair, two_pairs, three_kind, four_kind, small_straight, big_straight, full_house, chance, yatzy  