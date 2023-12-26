import numpy as np

class AffinityProp(object):
    def __init__(self, similarity_matrix, max_iteration=200, alpha=0.5, verbose=False):
        """
            similarity_matrix: N * N matrix containing similarities
            max_iteration: The maximum number of iterations to perfrom for clustering
            that stops the algorithm
        """
        self.s = similarity_matrix
        self.max_iteration = max_iteration
        self.alpha = alpha
        self.verbose = verbose

        #  INIITALISE THE RESPONSIBILITY AND THE AVAILABILITY MATRICES
        N, N = self.s.shape
        self.r = np.zeros((N, N))
        self.a = np.zeros((N, N))

    def _step(self):
        """
            Return the new Availability and repsonsibility matrices for all the data points
        """
        N, N = self.s.shape
        old_r = self.r
        old_a = self.a

        #R UPDATE STEP
        a_plus_s = self.a + self.s
        first_max = np.max(a_plus_s, axis=1)
        first_max_indices = np.argmax(a_plus_s, axis=1)
        first_max = np.repeat(first_max, N).reshape(N, N)
        a_plus_s[range(N), first_max_indices] = -np.inf
        second_max =  np.max(a_plus_s, axis=1)
        r = self.s - first_max
        r[range(N), first_max_indices] = self.s[range(N), first_max_indices] - second_max[range(N)]
        r = self.alpha * old_r + (1 - self.alpha) * r

        # A UPDATE STEP
        rp = np.maximum(r, 0)
        np.fill_diagonal(rp, np.diag(r))
        a = np.repeat(np.sum(rp, axis=0), N).reshape(N,N).T - rp
        da = np.diag(a)
        a = np.minimum(a, 0)
        np.fill_diagonal(a, da)
        a = self.alpha * old_a + (1 - self.alpha) * a

        return r, a

    def solve(self):
        for i in range(self.max_iteration):
            if self.verbose:
                print("processing iteration %d" % (i, ))
            self.r, self.a = self._step()

        e = self.r + self.a
        I = np.where(np.diag(e) > 0)[0]
        K = len(I)

        c = self.s[:, I]
        c = np.argmax(c, axis=1)

        c[I] = np.arange(0, K)

        idx = I[c]

        exemplar_indices = I
        exemplar_assignments =  idx
        print(f"Affinity Propagation completed in {self.max_iteration} iterations.")
        return exemplar_indices, exemplar_assignments
