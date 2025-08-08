
class OptimisticSmoothFicticiousPlayer():

    def __init__(self, p=0.1, e=0.3, c=10):
        # Init H = [].
        # Init 0 < p < 1, 0 < ξ < 1.
        # Init c > 0, count = 0.
        # Init the probability function f.
        self.history = []
        self.p = p
        self.e = e
        self.c = c
        self.count = 0


    def run(self):
        # Algorithm:
        # Optimistic Smooth Fictitious Play.

        # for LP = 0, 1, 2, ...do
        #   Init G = C = [0] * len(H).
        #   while LP not end do
        #       for each actor do
        #           if len(H) = 0 or Unif(0, 1) < p then
        #               Opponent player = current learner.
        #               Finish game.
        #           else
        #               Sample i ∼ f(..., (G[i], C[i]), ...).
        #               Opponent Player = H[i].
        #               Finish game and get g ∈ {+1, −1}.
        #               G[i] = G[i] + g, C[i] = C[i] + 1.
        #           end if
        #       endfor
        #   endwhile
        #   if (G[i] / C[i] > ξ, ∀ i) or (count > c) then
        #       Add current learner to H.
        #       count = 0.
        #   else
        #       count = count + 1.
        #   end if
        # endfor

        pass
