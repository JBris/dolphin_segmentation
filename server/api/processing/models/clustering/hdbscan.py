from hdbscan import HDBSCAN as HDBSCANBase

class HDBSCAN:
    def __init__(self):
        self.cluster = HDBSCANBase(
            algorithm ='best', 
            approx_min_span_tree = True,
            gen_min_span_tree = False, 
            leaf_size = 40, 
            metric='euclidean', 
            min_cluster_size = 15,
            min_samples = 15, 
            p = None
        ) 

    def fit(self, X, y = None):
        self.cluster.fit(X)