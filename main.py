from direct.showbase.ShowBase import ShowBase


class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


game = Main()
game.run()
