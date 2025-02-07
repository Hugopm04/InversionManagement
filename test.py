from Source import Controller, CMDView, InvestmentGroup


def main():
    view = CMDView()
    group = InvestmentGroup()
    controller = Controller(view, group)
    controller.run()
    

if __name__ == '__main__':
    main()