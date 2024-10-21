from players.player import Player

import random


class ControllablePlayer(Player):
  '''
  Controllable player.
  '''

  def __init__(self):
    super().__init__()
    # copied from rules.py line 22
    self.card_number = ['siebener', 'achter', 'neuner', 'unter', 'ober', 'koenig', 'zehner', 'sau']
    self.card_color = ['schellen', 'herz', 'gras', 'eichel']

  def translate_allowed_actions(self, allowed_actions):
    '''
    Formatting the previous ugly number format to my uglier version :)
    '''
    translated_actions = []
    for action in allowed_actions:
        if action == [None, None]:
            translated_actions.append("[None, None] (pass)")
        elif isinstance(action, bool):
            translated_actions.append(str(action))
        else:
            color, number = action
            color_name = f"{color} ({self.card_color[color]})" if color is not None else "None" # [0]
            number_name = f"{number} ({self.card_number[number]})" if number is not None else "None"
            translated_actions.append(f"[{color_name}, {number_name}]")
    
    print("Allowed actions:", ", ".join(translated_actions))

  '''
  TODO: Implement finish translated actions and simpler player choices.
  '''
  def act(self, state):
    allowed_actions, gamestate = state["allowed_actions"], state["game_state"]

    if gamestate.game_stage == self.rules.BIDDING:
        return self.handle_bidding(allowed_actions)
    elif gamestate.game_stage in [self.rules.CONTRA, self.rules.RETOUR]:
        return self.handle_contra_retour(allowed_actions)
    else:  # TRICK stage
        return self.handle_trick(allowed_actions)    


  def handle_bidding(self, allowed_actions):
    '''
    Bidding phase
    '''
    print("\nBidding Stage:")
    self.translate_allowed_actions(allowed_actions) # print the allowed actions

    while True:
        action = input("Choose your action! (format: color,number OR 'pass'): ")
        if action.lower() == 'pass':
            return [None, None], 1
        try:
            color, type_ = map(int, action.split(','))
            if [color, type_] in allowed_actions:
                return [color, type_], 1
        except:
            pass
        print("\nInvalid action. Try again.")
        self.translate_allowed_actions(allowed_actions) # print the allowed actions

  def handle_contra_retour(self, allowed_actions):
    '''
    Contra/Retour phase
    '''
    print("\nContra/Retour Stage:")
    self.translate_allowed_actions(allowed_actions) # print the allowed actions

    while True:
        action = input("Choose action ('true' to double, 'false' to pass): ").lower()
        if action == 'true' and True in allowed_actions:
            return True, 1
        elif action == 'false' and False in allowed_actions:
            return False, 1
        print("\nInvalid action. Try again.")
        self.translate_allowed_actions(allowed_actions) # print the allowed actions

  def handle_trick(self, allowed_actions):
    '''
    Trick phase
    '''
    print("\nTrick Stage:")
    self.translate_allowed_actions(allowed_actions) # print the allowed actions

    while True:
        action = input("Choose a card to play (format: color,number): ")
        try:
            color, number = map(int, action.split(','))
            if [color, number] in allowed_actions:
                return [color, number], 1
        except:
            pass
        print("\nInvalid action. Try again.") # may remove newline command if you prefer to.
        self.translate_allowed_actions(allowed_actions) # print the allowed actions


