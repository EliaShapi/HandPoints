import start_menu
import game
import end_screen

def main():
    while True:
        start_menu.show_start_menu()
        score = game.run_game()
        end_screen.show_end_screen(score)

if __name__ == '__main__':
    main()
