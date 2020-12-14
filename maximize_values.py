"""
This class represent an agent with values between low and high for buying an item
"""
class Uniform:
    low: float
    high: float

    def __init__(self, low, high):
        self.low = low
        self.high = high

    # Function that gets a value between low and high for the agent and return the revenue expectation of the salesman
    def get_RV(self, value:float)->float:
        return 2*value - self.high

    # Function that return the payment for this agent to the salesman's item
    def get_threshold(self)->float:
        return self.high/2


def max_revenue_auction(agent1:Uniform, value1:float)->None:
    """Function that get an agent and value between low-high of the agent and
        shows whether the agent has won the item and how much he will pay for it.

        Doctest:
        run with: python -m doctest -v maximize_values.py

        >>> max_revenue_auction(Uniform(10,30), 12)
        No agent wins

        >>> max_revenue_auction(Uniform(10,30), 18)
        Agent1 wins and pays 15.0

        >>> max_revenue_auction(Uniform(20,40), 19.9999)
        No agent wins

        >>> max_revenue_auction(Uniform(20,40), 20)
        No agent wins

        >>> max_revenue_auction(Uniform(20,40), 20.0001)
        Agent1 wins and pays 20.0

        """

    rv = agent1.get_RV(value1) # this is the value of the virtual function of the agent

    # if the value is positive - its maximize the salesman revenue expectation
    if rv > 0:
        threshold = agent1.get_threshold() # this is the payment for the agent (myersion auction with one buyer and one salesman)
        print("Agent1 wins and pays", threshold)
    else:
        print("No agent wins")

def max_revenue_auction(agent1:Uniform, agent2:Uniform, value1:float, value2:float)->None:
    """Function that get 2 agents and value between low-high of the agents and
       shows which buyer won (if any) and how much he paid.

       The rule of choice is: sell to an agent with the highest ri(vi), provided that ri(vi)> 0
       The payment: the threshold according to meyrson auction

            Doctest:
            run with: python -m doctest -v maximize_values.py

            #### 2 Agents: agent1 (10,30), agent2 (20,40) ####

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 23, 27)
            Agent1 wins and pays 22.0

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 18, 27)
            Agent2 wins and pays 23.0

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 14, 19)
            No agent wins

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 14, 26)
            Agent2 wins and pays 20.0

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 19, 19)
            Agent1 wins and pays 15.0

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 15, 20)
            No agent wins

            >>> max_revenue_auction(Uniform(10,30), Uniform(20,40), 16, 21)
            Agent1 wins and pays 15.0

            """

    rv1 = agent1.get_RV(value1)
    rv2 = agent2.get_RV(value2)

    # if both agents rv is less than 0 - no one wins
    if rv1 <= 0 and rv2 <= 0:
        print("No agent wins")
    else:
        # if only agent1 is good to the salesman profit
        if rv1 <= 0:
            threshold_2 = agent2.get_threshold()
            print("Agent2 wins and pays", threshold_2)
        # if only agent2 is good to the salesman profit
        elif rv2 <= 0:
            threshold_1 = agent1.get_threshold()
            print("Agent1 wins and pays", threshold_1)
        # if both agents rv are positive - need to check which rv is greater and find the threshold - depend on the other agent value
        else:
            if rv1 > rv2: # check how much agent 1 need to pay according to meyrson auction
                threshold_1 = payment_for_agent(agent1, value1, rv2)
                print("Agent1 wins and pays", threshold_1)
            elif rv2 > rv1: # check how much agent 2 need to pay according to meyrson auction
                threshold_2 = payment_for_agent(agent2, value2, rv1)
                print("Agent2 wins and pays", threshold_2)
            else: # rv's of the agents are equal - sell the item to agent1 (arbitrary)
                threshold_1 = agent1.get_threshold()
                print("Agent1 wins and pays", threshold_1)

# Function that gets an agent, value and rv of the other agent and find the correct payment for the agent - according to meyrson auction
def payment_for_agent(agent:Uniform, value:float, rv:float)->float:
    eps = 0.001 # determine one step
    rv1_temp = agent.get_RV(value)
    #while the new ri(vi) value (value-minus step) is still greater than rj(vj), calculate again the new ri(vi)
    while rv1_temp > rv:
        value -= eps
        rv1_temp = agent.get_RV(value)
    value = float(round(value)) # round the final number and cast it to float for doctest success
    return value
