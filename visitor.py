

class BaseVisitor():
    def __init__(self, track_seg):
        self.track_seg = track_seg
    def visit(self):
        pass
        raise NotImplementedError



class Visitor(BaseVisitor):
    def visit(self, analyze):
        analyze.run(self.track_seg)





