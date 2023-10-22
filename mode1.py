from island import Island
from data_structures.bst import BinarySearchTree

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        N is number of island of island list
        complexity worst case O(N*Log(N))
        since we are assuming the depth of all BST is Log(N), in intialisation,
        we would have to insert each item of the list of islands (N times), and each time we are inserting,
        in the worst case the node is added to the bottom of the tree (CompK *D, where D is Log(N)).
        best case O(N*log(N)) again, we are inserting an item into a bst for each island there is in the list (N),
        and so every time an item is inserted into the bst, it will cost a complexity of O(CompK *D), where Depth D
        is Log(N)
        for this i used a binary search tree as my data structure with the ratio of island money/ island marines as the key
        this is so that i can use the del, setitem etc functions.
        as an example, if we were to add two islands [a,b]
        for each island, we find its ratio, a.money/a.marines and use it as a key, with the island as an item.
        with this key, item, we add it to a binary search tree.

        """
        self.islands = islands
        self.crew = crew
        self.bst = BinarySearchTree()
        for island in self.islands:
            self.bst[island.money/island.marines] = island
    def select_islands(self) -> list[tuple[Island, int]]:
        """
        worst case O(Log N). Here we are finding the node with the largest key (best ratio),
        and using the maximum amount of crew possible to deploy on the island. After "attacking" the island
        and using some/all of your crew on the largest node, we delete that node and repeat until there is no more crew
        left.
        So, finding the max node would have complexity O(Log N), then after attacking the island, we would have to delete this node
        from the tree which would have worst case O(Log N)
        total complexity = O(Log (N) + Log (N))= O(Log(N))
        the best case would be the same = O(Log(N)). This is because since we assume the depth of the tree to be at most O(Log(N)),
        there is no case that would result in changing the complexity to find max, and delete the max.
        for example, with island list [a,b]
        finding max island would have O(Log[n])where n is 2
        deleting island would have O(Log[n]) where n is 2
        """

        crew = self.crew
        tree = self.bst
        root = tree.root
        island_list = []
        while crew > 0 :
            max_island = tree.get_maximal(root)
            deploy = min(max_island.item.marines,crew)
            crew -= deploy
            if deploy > 0:
                island_list.append((max_island.item,deploy))
            #del tree[max_island.key]
        return island_list

    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        worst case = best case , the outer loop is executed C times, where c is the length of crew_numbers
        initialisation of Mode1Navigator = O(NLog(N))
        select_islands function = Log(N)
        O(C *(NLog(N)+Log(N))) = O(C * NLog(N)) 
        the execution is the same for all cases (depth of bst is capped at Log(N))
        
        approach
        for each crew in the list, I set up a Mode1Navigator instance, in order to use
        the select_islands functions. The output of which (list of tuples = (island,crew number)) would be used to calculate
        the total cash for each amount of crew in crew_numbers
        
        as an small example, for crew numbers [1,2] and self.islands [a,b]
        in the first loop (crew number [0])
        if the output of using the function with crew number 1 and islands [a,b] is
        [(a,1),(b,0)] (where a has a better ratio than b)
        from this list we can calculate the the cash accumulated from attack island a with 1 pirate
        we then append this to the output list money.
        we then repeat the previous paragraph (lines 73,78) for each crew in crew_numbers.
        """
        money = []
        for crew in crew_numbers:
            cash = 0
            a = Mode1Navigator(self.islands,crew)
            alist = a.select_islands()
            for tuple in alist:
                islandmoney, islandmarines, deploy = tuple[0].money, tuple[0].marines, tuple[1]
                cash += min(islandmoney*deploy/islandmarines,islandmoney)
            money.append(cash)

        return money

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        worst case = best case
        deleting an item from self.bst would have a complexity Log(N) at best/worst
        adding an item to the self.bst would have a complexity log(N) at best/worst
        so O(Log N +Log N) = O(Log N)

        for bst we can't "update" in this case, since changing the island itself (marines and gold) would
        change its ratio that we use for the key. So, we would instead, delete the island node off the tree, update the island
        and add it back to the tree.

        with a tree
        a
        |\
        b  None
        if we updated the island a to have a worst ratio, we would delete node a resulting in the tree to be
        b
        |\
        None None
        and added island/node a with its updated key 
        b
        |\
        a None
        """
    
        ratio = island.money/island.marines
        del self.bst[ratio]
        island.money = new_money
        island.marines = new_marines
        self.bst[island.money/island.marines] = island
        return