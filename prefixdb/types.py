import radix


class Database:
    def __init__(self):
        self.rtree = radix.Radix()

    def upsert_node(self, prefix):
        rnode = self.rtree.search_exact(prefix)
        if not rnode:
            rnode = self.rtree.add(prefix)
        return rnode

    def search_single(self, prefix):
        rnode = self.rtree.search_best(prefix)
        if not rnode:
            raise KeyError(prefix)
        return rnode.prefix, rnode.data['entry']

    def search_children(self, prefix):
        rnodes = self.rtree.search_covered(prefix)
        if not rnodes:
            raise KeyError(prefix)
        return {rnode.prefix: rnode.data for rnode in rnodes}

    def search_parents(self, prefix):
        prefix = prefix.split('/')[0] + '/0'
        return self.search_children(prefix)

    def __iter__(self):
        return iter(self.rtree)

    def delete(self, prefix):
        return self.rtree.delete(prefix)

    def upsert(self, prefix, data):
        rnode = self.upsert_node(prefix)
        rnode.data['entry'] = data
