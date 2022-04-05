import random 

def random_quote():
    """Picks a random quote to show"""
    quotes = ["'I encourage everybody to hop on Google and type in ‘national park’ in whatever state they live in and see the beauty that lies in their own backyard. It’s that simple.' - Jordan Fisher, Singer, Dancer, & Actor", 
    "'A national park is not a playground. it’s a sanctuary for nature and for humans who will accept nature on nature’s own terms.' - Michael Frome, Writer & Educator",
    "'Between every two pine trees there is a door leading to a new way of life…Climb the mountains and get their good tidings. Nature’s peace will flow into you as sunshine into trees.' - John Muir, Naturalist, Explorer, Environmental Philosopher", 
    "'If future generations are to remember us with gratitude rather than contempt, we must leave them something more than the miracles of technology. We must leave them a glimpse of the world as it was in the beginning, not just after we got through it.' - Lyndon B. Johnson, 36th President of the United States",
    "'National parks and reserves are an integral aspect of intelligent use of natural resources. It is the course of wisdom to set aside an ample portion of our natural resources as national parks and reserves, thus ensuring that future generations may know the majesty of the earth as we know it today.' - John F. Kennedy, 35th President of the United States",
    "'In wilderness is the preservation of the world.' - Henry David Thoreau, Writer"]

    rand_q = random.choice(quotes)

    return rand_q