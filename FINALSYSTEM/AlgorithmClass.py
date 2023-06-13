class Algorithm:
    """
    algorithm template
    """
    def __init__(self):
        self.Bx, self.By, self.Bz = 0,0,0
        self.alpha, self.gamma, self.freq = 0,0,0

    def run(self, robot_list):
        """
        inputs: the robot list from tracking
        outputs: actions list in the form of [Bx,By,Bz,alpha,gamma,freq]
        """
        #DO STUFF HERE
        

        actions = [self.Bx, self.By, self.Bz, self.alpha, self.gamma, self.freq]
        return actions