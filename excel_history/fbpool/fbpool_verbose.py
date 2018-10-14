class FBPoolVerbose:

    def __init__(self,quiet=None):
        self.quiet = True if quiet == None else quiet

    def start(self,operation):
        if self.quiet:
            return
        print("")
        print(operation)

    def done(self,operation):
        if self.quiet:
            return
        print("%s done." % (operation))
        print("")

    def update(self,message):
        if self.quiet:
            return
        print(" : %s" % (message))

    def update_every(self,message,current_i,update_i,total_iterations):
        if self.quiet:
            return
        if ((current_i+1) % update_i) == 0:
            print(" : %s (%d of %d)" % (message,current_i+1,total_iterations))

