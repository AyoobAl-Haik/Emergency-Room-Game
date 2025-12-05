from game_manager import GameManager

def main():
    game = GameManager(num_bays=3)
    
    while True:
        print(f"\n--- TURN {game.turn} ---")
        game.process_turn()

        # Print waiting list
        print("\nWaiting List:")
        for i, p in enumerate(game.waiting_list):
            print(f"{i}: {p}")

        # Print bays
        print("\nBays:")
        for i, p in enumerate(game.bays.get_patients()):
            print(f"Bay {i}: {p}")

        # Critical check
        critical = game.check_for_critical()
        if critical:
            print("\n⚠️ CRITICAL PATIENTS! Game Over.")
            for c in critical:
                print(c)
            break

        # Player action
        print("\nActions:")
        print("1. Move patient from waiting list to bay")
        print("2. Apply treatment to bay patient")
        print("3. End turn")

        choice = input("Choose: ")

        if choice == "1":
            idx_w = int(input("Waiting index: "))
            idx_b = int(input("Bay index: "))
            p = game.waiting_list.pop(idx_w)
            if not game.bays.assign_patient(p, idx_b):
                print("Bay occupied.")
                game.waiting_list.append(p)

        elif choice == "2":
            idx_b = int(input("Bay index: "))
            tx = input("Treatment name (fluids/antibiotics/defibrillation): ")
            game.apply_treatment(idx_b, tx)

        elif choice == "3":
            continue

if __name__ == "__main__":
    main()
