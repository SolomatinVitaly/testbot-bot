from transitions import Machine


class StateMachine(object):


    states = ['start_state', 'food_size', 'payment_form', 'checking']


    def __init__(self, initial_state='start_state'):
        self.machine = Machine(model=self, states=StateMachine.states, initial=initial_state)
        self.machine.add_ordered_transitions(self.states)
        self.machine.add_transition(trigger='cancel', source='*', dest='start_state')
