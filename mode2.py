from island import Island
from data_structures.bst import BinarySearchTree
class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, n_pirates: int) -> None:
        """
        best = worst = O(1)
        """
        self.pirates = n_pirates
        self.map =  BinarySearchTree()

    def add_islands(self, islands: list[Island]):
        """
        worst/best = I*Log(N)
        the outer loop is executed I times 
        the innerloop is simply adding a node to a bst which has complexity (CompK*D) where depth D is Log(N).

        for this i used a binary search tree again as my data structure with the ratio of island money/ island marines as the key
        this is so that i can use the del, setitem etc functions.
        as an example, if we were to add two islands [a,b]
        for each island, we find its ratio, a.money/a.marines and use it as a key, with the island as an item.
        with this key, item, we add it to a binary search tree with N nodes.
        """
        for island in islands:
            self.map[island.money/island.marines] = island

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        worst case = best case
        for every pirate: C times
            get max = Log(N)
            del = Log(N)
            insert updated island = Log(N)
        CLog(N)
        for each pirate, we would find the best island to invade, and deploy the max amount of 
        pirates for the best island. I assume the pirates are taking turns to invade islands in order,
        and during the picking process, each pirate is aware of the order.
        So, after a pirate makes their choice, we update the island with its new amounts of marines, and money.
        afterwards, the next pirate decides based on the updated version of the island.
        
        for example, if the island was 
        (a has 2 marines, b has 2 marines)
        a
        |\
        b None
        
        and there were 2 pirates with 2 in their crews.

        then the first pirate would raid island a for 100% its money, resulting in the map looking like
        b
        |\
        a None
        and we would append daylist with the tuple (island, No. of pirates deployed)
        the second pirate would raid island b for 100% of its money, resulting in the map to look like

        a
        |\
        None None
        and again we would append daylist with the tuple (island, No. of pirates deployed)
        afterwards the list daylist would have all the tuples from each pirate for one day.
        """
        daylist = []
        for pirate in range(self.pirates):
            best = self.map.get_maximal(self.map.root) #Log(N)
            deploy = min(crew, best.item.marines)
            cash = min(deploy*best.item.money/best.item.marines,best.item.money)
            newmoney = best.item.money - cash
            newmarines =  best.item.marines - deploy
            daylist.append((best.item,deploy))
            del self.map[best.key] #Log(N)
            self.map[newmoney/newmarines] = Island(best.item.name,newmoney,newmarines) #Log(N)

        return daylist
